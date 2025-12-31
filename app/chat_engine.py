from app.cache import EVENT_CACHE, get_event_by_name
from app.rag_retriever import semantic_search
from app.llm import generate_answer
import re
import random
from difflib import SequenceMatcher
import gc

# ---------------- CONFIG ---------------- #

# Reduced response variations to save memory
BRAHMA_RESPONSES = [
    "Brahma '26 is the annual cultural festival of Adi Shankara Institute of Engineering and Technology (ASIET), celebrating music, dance, art, and creative expression.",
    "Brahma is ASIET's flagship cultural fest featuring competitive events, pro-shows, and workshops."
]

ASHWAMEDHA_RESPONSES = [
    "Ashwamedha is ASIET's national-level technical fest showcasing innovation and engineering excellence.",
    "Ashwamedha features coding contests, hackathons, robotics events, and technical competitions."
]

OUT_OF_CONTEXT_RESPONSES = [
    "I can help only with Brahma '26 and ASIET events.",
    "That's not related to the Brahma festival."
]

GREETING_RESPONSES = [
    "Hello! 👋 I'm the Brahma '26 assistant. Ask me about events, dates, venues, or anything related to ASIET's cultural fest!",
    "Hi there! 😊 I can help you with information about Brahma '26 and Ashwamedha events at ASIET. What would you like to know?",
    "Hey! 🎉 Welcome to Brahma '26 info bot. Ask me about cultural events, schedules, or festival details!",
    "Greetings! I'm here to help with Brahma '26 and ASIET events. What can I tell you about?",
]

THANKYOU_RESPONSES = [
    "You're welcome! Feel free to ask if you need anything else about Brahma '26! 😊",
    "Happy to help! Let me know if you have more questions about the fest! 🎉",
    "Glad I could help! Ask away if you need more info about ASIET events!",
    "Anytime! Enjoy Brahma '26! 🎊",
]

# ---------------- HELPERS ---------------- #

def tokenize(text: str) -> set:
    return set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))

def safe(val, fallback="not specified"):
    return val if val else fallback

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

FEST_ALIASES = {
    "brahma": ["brahma", "brama", "bhrahma", "brahama"],
    "ashwamedha": ["ashwamedha", "aswamedha", "ashwmedha"]
}

def fuzzy_fest_match(query: str, threshold: float = 0.72):
    """Check if any word in query matches fest names"""
    q_lower = query.lower()
    
    # Check each word in the query
    words = re.findall(r"\b[a-zA-Z]+\b", q_lower)
    
    for fest, variants in FEST_ALIASES.items():
        for v in variants:
            # Check if variant appears in query
            if v in q_lower:
                return fest
            # Check similarity of each word
            for word in words:
                if len(word) >= 4 and similarity(word, v) >= threshold:
                    return fest
    return None

def find_exact_event(query: str):
    """Find event with simplified matching"""
    q_tokens = tokenize(query)
    matched = []

    # Limit search to cached events
    for event in EVENT_CACHE[:50]:  # Check only first 50
        name = event.get("event_name", "")
        e_tokens = tokenize(name)

        if e_tokens and e_tokens.issubset(q_tokens):
            matched.append(event)

    if len(matched) == 1:
        return matched[0]
    
    return None

def is_greeting(query: str) -> bool:
    """Check if message is a greeting"""
    greetings = ["hi", "hello", "hey", "hai", "hii", "helo", "hola", "greetings", 
                 "good morning", "good afternoon", "good evening", "howdy", "yo"]
    q_lower = query.lower().strip()
    
    # Exact or close match
    if q_lower in greetings:
        return True
    
    # Check if any greeting word is in the message (for "hi there", "hello!")
    words = re.findall(r"\b[a-zA-Z]+\b", q_lower)
    return any(word in greetings for word in words) and len(words) <= 3

def is_thankyou(query: str) -> bool:
    """Check if message is a thank you"""
    thanks = ["thanks", "thank you", "thankyou", "thx", "ty", "appreciate"]
    q_lower = query.lower().strip()
    return any(t in q_lower for t in thanks)

def is_simple_fest_query(query: str) -> bool:
    """Check if it's a simple 'what is brahma/ashwamedha' query"""
    q_lower = query.lower().strip()
    
    # Just the fest name alone
    simple_patterns = [
        r"^(what is |what's |whats |tell me about |explain )?bh?rama$",
        r"^(what is |what's |whats |tell me about |explain )?ashwamedha$",
        r"^bh?rama\??$",
        r"^ashwamedha\??$",
    ]
    
    for pattern in simple_patterns:
        if re.match(pattern, q_lower):
            return True
    
    # Check for deep/complex question indicators
    deep_keywords = ["history", "when started", "why called", "origin", "background", 
                     "story", "past", "previous", "earlier", "evolution", "tradition",
                     "how many", "who founded", "who started", "details about"]
    
    if any(keyword in q_lower for keyword in deep_keywords):
        return False  # It's a deep question, needs semantic search
    
    # Simple "what is brahma" style
    words = q_lower.split()
    if len(words) <= 4 and any(w in ["what", "whats", "explain", "tell"] for w in words):
        return True
    
    return False

def is_relevant_query(query: str) -> bool:
    """Quick relevance check with fuzzy matching and event name detection"""
    keywords = ["event", "brahma", "ashwamedha", "fest", "festival", "college", 
                "when", "where", "what", "date", "time", "venue", "asiet", "registration",
                "participate", "team", "prize", "competition", "workshop"]
    q_lower = query.lower()
    q_tokens = tokenize(q_lower)
    
    # Direct keyword match
    if any(kw in q_lower for kw in keywords):
        return True
    
    # Check if query matches any event name from cache (even partially)
    for event in EVENT_CACHE[:50]:  # Check first 50 events
        event_name = event.get("event_name", "").lower()
        if event_name:
            event_tokens = tokenize(event_name)
            # If ANY meaningful word from event name is in query
            common_tokens = event_tokens.intersection(q_tokens)
            if common_tokens:
                # Filter out very short words (like "a", "of", "the")
                meaningful_matches = [t for t in common_tokens if len(t) >= 3]
                if meaningful_matches:
                    return True
            # Or if event name appears as substring
            if len(event_name) > 4 and event_name in q_lower:
                return True
    
    # Fuzzy match for common misspellings
    for word in re.findall(r"\b[a-zA-Z]{4,}\b", q_lower):  # Words 4+ chars
        for kw in ["brahma", "ashwamedha", "event", "festival"]:
            if similarity(word, kw) >= 0.7:
                return True
    
    return False

# ---------------- MAIN CHAT ---------------- #

def chat(user_message: str) -> str:
    """
    Lightweight chat function with memory optimization.
    """
    try:
        query = user_message.strip()
        if not query:
            return "Please ask a question."

        # Handle greetings
        if is_greeting(query):
            return random.choice(GREETING_RESPONSES)
        
        # Handle thank you
        if is_thankyou(query):
            return random.choice(THANKYOU_RESPONSES)

        # Quick fest detection - but only for simple queries
        fest = fuzzy_fest_match(query)
        if fest and is_simple_fest_query(query):
            if fest == "brahma":
                return random.choice(BRAHMA_RESPONSES)
            if fest == "ashwamedha":
                return random.choice(ASHWAMEDHA_RESPONSES)

        # Early exit for irrelevant queries
        if not is_relevant_query(query):
            return random.choice(OUT_OF_CONTEXT_RESPONSES)

        # Try exact event match first (fastest)
        event = find_exact_event(query)
        if event:
            return format_event_response(event)

        # Semantic search (more expensive)
        try:
            results = semantic_search(query, top_k=2)  # Reduced to 2
            
            if not results:
                return "I don't have specific information about that. Try asking about events or festival details."

            # Build concise context
            context_parts = []
            for r in results[:2]:  # Use max 2 results
                text = r["text"][:300]  # Truncate
                context_parts.append(text)
            
            context = "\n".join(context_parts)
            
            # Generate answer
            answer = generate_answer(context, query)
            
            # Cleanup
            gc.collect()
            
            return answer
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return "Sorry, I'm having trouble processing that request."

    except Exception as e:
        print(f"❌ Chat error: {e}")
        return "Sorry, something went wrong."

def format_event_response(event: dict) -> str:
    """Format event info concisely"""
    name = event.get("event_name", "Unknown")
    date = safe(event.get("date"))
    time = safe(event.get("time"))
    venue = safe(event.get("venue"))
    
    return f"{name} is on {date} at {time}, venue: {venue}."
