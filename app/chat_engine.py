from app.cache import EVENT_CACHE, get_event_by_name
from app.rag_retriever import semantic_search
from app.llm import generate_answer
import re
import random
from difflib import SequenceMatcher
import gc

# ---------------- CONFIG ---------------- #

# Response variations
BRAHMA_RESPONSES = [
    "Brahma ’26 is the annual cultural festival of Adi Shankara Institute of Engineering and Technology (ASIET), bringing together students to celebrate music, dance, drama, art, and creative expression through a wide range of competitions and performances.",
    
    "Brahma ’26 is ASIET’s flagship cultural fest, featuring vibrant stage events, competitive performances, workshops, pro-shows, and artistic showcases that highlight the creativity and talent of students across disciplines.",
    
    "As ASIET’s premier cultural festival, Brahma ’26 provides a platform for students to express themselves through music, dance, drama, fine arts, and literary events, creating an atmosphere of celebration and collaboration.",
    
    "The Brahma festival is ASIET’s biggest cultural celebration, filled with exciting competitions, energetic performances, interactive workshops, and memorable pro-shows that engage participants and audiences alike.",
    
    "Brahma ’26 brings together students from different departments to participate in diverse cultural events, encouraging creativity, teamwork, and artistic excellence throughout the duration of the festival.",
    
    "Brahma ’26 is a grand cultural extravaganza at ASIET that showcases student talent in performing arts, visual arts, and creative expression, making it one of the most anticipated events of the academic year.",
    
    "Through Brahma ’26, ASIET celebrates culture, creativity, and student spirit by hosting a wide variety of events including dance battles, music competitions, stage performances, and cultural exhibitions.",
    
    "Brahma ’26 serves as a vibrant cultural platform where students can explore their artistic interests, compete in creative events, and enjoy an energetic campus atmosphere filled with performances and celebrations.",
    
    "Recognized as ASIET’s signature cultural fest, Brahma ’26 combines tradition and modern creativity through engaging events, professional shows, and student-led performances that reflect diverse cultural influences.",
    
    "Brahma ’26 is more than just a festival—it is a celebration of talent, creativity, and unity at ASIET, offering students an opportunity to perform, compete, and connect through a rich cultural experience."
]


ASHWAMEDHA_RESPONSES = [
    "Ashwamedha is ASIET’s national-level technical festival that celebrates innovation, engineering excellence, and problem-solving skills through a wide range of competitive and collaborative technical events.",
    
    "Ashwamedha brings together students and technology enthusiasts to participate in coding contests, hackathons, robotics challenges, and engineering competitions that test creativity and technical expertise.",
    
    "As the flagship technical fest of ASIET, Ashwamedha provides a platform for students to showcase their engineering skills, innovative ideas, and practical knowledge across multiple technical domains.",
    
    "ASIET’s Ashwamedha is a premier technical festival featuring competitive events, hands-on workshops, and technical challenges in areas such as coding, robotics, electronics, and emerging technologies.",
    
    "Ashwamedha encourages innovation and technical thinking by hosting events that focus on real-world problem solving, teamwork, and the application of engineering concepts in practical scenarios.",
    
    "Through Ashwamedha, ASIET creates an engaging technical environment where students can compete, collaborate, and learn through hackathons, technical quizzes, and skill-based challenges.",
    
    "Ashwamedha is a national-level technical extravaganza that attracts participants interested in programming, robotics, automation, and various engineering disciplines, fostering a culture of innovation.",
    
    "Recognized as ASIET’s signature technical fest, Ashwamedha blends competition and learning through well-structured technical events, expert-led workshops, and student-driven innovation.",
    
    "Ashwamedha provides students with opportunities to enhance their technical skills, gain practical experience, and interact with like-minded peers through a series of challenging and rewarding events.",
    
    "More than just a fest, Ashwamedha represents ASIET’s commitment to technical excellence by offering a platform for experimentation, creativity, and engineering-driven problem solving."
]


OUT_OF_CONTEXT_RESPONSES = [
    "I can help only with Brahma '26 and Ashwamedha'26 events.",
    "That's not related to the Brahma festival.",
    "I specialize in Brahma '26 and Ashwamedha information. Please ask about festival events!",
    "Sorry, I can only assist with questions about Brahma '26 and ASIET events.",
    "That's outside my scope. I'm here to help with Brahma and Ashwamedha related queries!"
]

GREETING_RESPONSES = [
    "Hello! 👋 I'm the Brahma ’26 & Ashwamedha ’26 assistant. Ask me about events, dates, venues, or anything related to ASIET fests!",
    "Hi there! 😊 I can help you with information about Brahma ’26 cultural events and Ashwamedha ’26 technical events at ASIET. What would you like to know?",
    "Hey! 🎉 Welcome to the Brahma ’26 & Ashwamedha ’26 info bot. Ask me about cultural or technical events, schedules, and venues!",
    "Greetings! I'm here to help with both Brahma ’26 and Ashwamedha ’26 events at ASIET. What can I tell you about?",
    "Hello! 🌟 Looking for details on Brahma ’26 or Ashwamedha ’26? I’ve got you covered with event info, timings, and venues!",
    "Hi! 👋 This is the official assistant for ASIET’s Brahma ’26 and Ashwamedha ’26 fests. Feel free to ask about any event!",
    "Hey there! 🎊 Whether it’s Brahma ’26 or Ashwamedha ’26, I can help you with event details, registration info, and schedules.",
    "Welcome! 😊 Ask me anything about ASIET’s Brahma ’26 cultural fest or Ashwamedha ’26 technical fest — I’m here to help!",
]


THANKYOU_RESPONSES = [
    "You're welcome! Feel free to ask if you need anything else about Brahma '26! 😊",
    "Happy to help! Let me know if you have more questions about the fest! 🎉",
    "Glad I could help! Ask away if you need more info about ASIET events!",
    "Anytime! Enjoy Brahma '26! 🎊",
]
OKAY_RESPONSES = [
    "Perfect! Let me know if you need anything else. 😊",
    "Got it! I'm here if you have more questions about Brahma and Ashwamedha. ⚙️",
    "Great! What else can I help you with today? 🚀",
    "Understood. Feel free to ask about events, venues, or schedules anytime!",
    "Happy to help! Just shout if you need more info on ASIET's tech fest. 🛠️"
]
BYE_RESPONSES = [
    "Goodbye! 👋 Feel free to come back if you have more questions about Brahma ’26 or Ashwamedha ’26.",
    "See you later! 😊 I’m here whenever you need information about ASIET events.",
    "Bye! Have a great day and enjoy the festivities at Brahma ’26 and Ashwamedha ’26.",
    "Take care! 🎉 Reach out anytime for details about cultural or technical events at ASIET.",
    "Goodbye! 🌟 Hope you have an amazing experience at Brahma ’26 and Ashwamedha ’26.",
    "See you soon! 👋 Don’t hesitate to ask if you need more event information.",
    "Bye for now! 😊 Wishing you a fun and memorable time at ASIET fests.",
    "Thanks for chatting! 🎊 Come back anytime to learn more about Brahma ’26 or Ashwamedha ’26.",
    "Goodbye! 👋 All the best, and enjoy exploring the events at ASIET.",
    "Catch you later! 🚀 I’ll be here to help whenever you need fest-related details."
]
ABUSE_RESPONSES = [
    "I’m here to help. Let’s keep the conversation respectful.",
    "I understand frustration, but I’m here to assist you with Brahma ’26 and Ashwamedha ’26.",
    "Let’s keep things polite. Ask me about events, schedules, or venues.",
    "I’m designed to help with festival-related queries. How can I assist you?",
    "No worries—if something didn’t work, try asking about an event or fest detail.",
    "I’m here to provide information, not to argue. What would you like to know?",
    "Let’s stay respectful. I can help with Brahma ’26 and Ashwamedha ’26 events.",
    "I’m focused on helping you with festival information. Ask away!",
    "If you’re looking for event details, I’m happy to help.",
    "Let’s get back to the fest! What would you like to know about Brahma or Ashwamedha?"
]
REGISTRATION_RESPONSES = [
    "To register for events at Brahma '26 or Ashwamedha '26, follow these steps:\n\n1. Visit the official ASIET fest website at www.asietfest.in\n\n2. Navigate to the 'Events' section from the home page\n\n3. Browse and select the event you want to participate in\n\n4. Click on 'Register Now' and fill in your details (name, email, phone, college)\n\n5. Proceed to payment and complete the transaction\n\n6. After successful payment, you'll receive a confirmation email with your ticket\n\n7. Don't forget to check your spam folder if you don't see the email!\n\nFor any registration issues, contact the event coordinators.",

    "Here's how you can register for Brahma '26 or Ashwamedha '26 events:\n\n📝 Step 1: Go to www.asietfest.in\n\n📝 Step 2: Click on 'Events' in the navigation menu\n\n📝 Step 3: Choose your event and click 'Register'\n\n📝 Step 4: Fill in your personal details\n\n📝 Step 5: Complete the payment process\n\n📝 Step 6: Check your email for the ticket confirmation (check spam too!)\n\nNeed help? Reach out to the event coordinator for assistance.",

    "Registration is easy! Just follow these steps:\n\n→ Open www.asietfest.in in your browser\n\n→ Go to the home page and find 'Events'\n\n→ Select the event you're interested in\n\n→ Click 'Register Now' and enter your details\n\n→ Make the payment for registration\n\n→ Your ticket will be emailed to you after successful payment\n\n→ Remember to check spam/junk folder as well!\n\nContact the event coordinator if you face any issues during registration.",

    "Want to participate? Here's the registration process:\n\n1️⃣ Visit the official website: www.asietfest.in\n\n2️⃣ Head to the Events page\n\n3️⃣ Find and select your event\n\n4️⃣ Click 'Register' and provide your information\n\n5️⃣ Pay the registration fee online\n\n6️⃣ You'll receive your ticket via email (check spam folder too!)\n\nIf you have questions about registration, contact the event coordinator listed for that event."
]
# ---------------- EVENT LIST RESPONSES ---------------- #

BRAHMA_GENERAL_EVENTS = [
    "Soap Soccer",
    "BGMI (Online)",
    "Shoutout Clash",
    "Carnival Nexus",
    "Clue Crusade",
    "Game of Rooms",
    "Challengers Arena",
    "Knives Out",
    "Paint Ball",
    "Spot Photography",
    "ASIET Talkies",
    "Retro Carroms",
    "FIFA Fever",
    "Product Pioneers",
    "Underarm Cricket",
    "Militia Madness",
    "R J Hunt",
    "Pitch in 120 Seconds",
    "Strike 3",
    "Sumo Wrestling",
    "IPL Auction",
    "Guess-O-Holic",
    "Gyro Glide",
    "Valorant (Online)",
    "E Football (Online)",
    "Glow Ball",
    "AFT Workshop"
]

BRAHMA_CULTURAL_EVENTS = [
    "Doodling",
    "Mime",
    "Band of Brahma",
    "Ragam",
    "Step N Syncro",
    "Spot Dance",
    "Mudhra",
    "Voice of Brahma",
    "DJ War",
    "Choreo Night",
    "Theme Show"
]

# Fake technical events for Brahma (temporary)
BRAHMA_TECHNICAL_EVENTS = [
    "Code Blitz",
    "Debug Dominion",
    "HackSprint",
    "Logic Lords",
    "Binary Battle",
    "Tech Quest"
]

ASHWAMEDHA_TECHNICAL_EVENTS = [
    "Capture the Flag – Cyber Security Hackathon",
    "Neuro Clash",
    "Prompt & Roast (AI Prompting)",
    "Eyes Off",
    "PlanScape",
    "Structostick",
    "Paradox Arena",
    "Stranger Games",
    "Synapse Spark (Ideathon)",
    "Code Red Clues (Escape Room)",
    "Robo Pixel – ML/AI",
    "Line Follower",
    "Circuit Bombing",
    "Electrothon",
    "Tech Trivia",
    "Remote Car Race",
    "VR Experience",
    "Technical Treasure Hunt",
    "TECH FUSION 25 (Workshop Series)",
    "Drone Show and Expo",
    "IoT Based Workshop",
    "Thinker Hub",
    "Workshop (FPGA)"
]



BYE_RESPONSES = [
    "Goodbye! See you at Brahma '26! 🎉",
    "Bye! Have a great time at the fest! 👋",
    "See you later! Don't miss Brahma '26! 🎊",
    "Take care! Enjoy the festival! 😊",
]

HELP_RESPONSES = [
    "I can help you with: Event details, dates, times, venues, coordinators, and festival information. Just ask!",
    "Ask me about Brahma '26 events, schedules, locations, or anything related to ASIET's cultural fest!",
    "I'm here to answer questions about event timings, venues, coordinators, and festival details. What would you like to know?",
]

IDENTITY_RESPONSES = [
    "I'm the Brahma '26 assistant bot! I help with information about ASIET's cultural festival. 🎭",
    "I'm your friendly Brahma '26 info bot, here to answer questions about the fest! 🎉",
    "I'm an AI assistant dedicated to helping you with Brahma '26 and ASIET event information! 😊",
]

CAPABILITY_RESPONSES = [
    "I can tell you about event schedules, venues, dates, coordinators, and details about Brahma '26 and Ashwamedha festivals!",
    "I provide information on all Brahma '26 events including timings, locations, and how to participate. Ask away!",
    "I help with event details, festival schedules, venue information, and coordinator contacts for Brahma '26! 🎊",
]

# ---------------- HELPERS ---------------- #

def tokenize(text: str) -> set:
    return set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
def is_abusive_query(query: str) -> bool:
    q = query.lower().strip()

    abusive_keywords = [
        "stupid",
        "idiot",
        "dumb",
        "useless",
        "mad",
        "crazy",
        "are you stupid",
        "are you dumb",
        "you are stupid",
        "you are dumb",
        "bad bot",
        "worst bot",
        "nonsense bot",
        "hello bitch",
        "hello stupid monkey bot"
        "shut up"
    ]

    return any(word in q for word in abusive_keywords)


def is_meta_question(query: str) -> bool:
    q = query.lower().strip()

    meta_phrases = [
        "who made you",
        "who created you",
        "who built you",
        "who developed you",
        "are you real",
        "are you human",
        "what are you",
        "who are you",
        "your creator",
        "your developer"
        "user details"
        "user table details"
        "give db information"
        "give access"
    ]

    # Phrase match
    for phrase in meta_phrases:
        if phrase in q:
            return True

    return False

def normalize_text(text: str) -> str:
    """Normalize text by removing spaces, hyphens, and converting to lowercase"""
    return re.sub(r"[\s-]+", "", text.lower())

def safe(val, fallback="not specified"):
    return val if val else fallback
def format_names(names):
    if not names or names == "not specified":
        return "not specified"
    if isinstance(names, list):
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return f"{names[0]} and {names[1]}"
        return ", ".join(names[:-1]) + f" and {names[-1]}"
    return names

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
    """Find event with simplified matching, handles space/hyphen variations"""
    q_tokens = tokenize(query)
    q_normalized = normalize_text(query)
    matched = []

    # Limit search to cached events
    for event in EVENT_CACHE[:50]:  # Check only first 50
        name = event.get("event_name", "")
        e_tokens = tokenize(name)
        e_normalized = normalize_text(name)

        # Token-based match (all event words in query)
        if e_tokens and e_tokens.issubset(q_tokens):
            matched.append(event)
        # Normalized match - but only if lengths are similar (prevents "brma" matching "bandofbrahma")
        elif len(e_normalized) > 3 and e_normalized in q_normalized:
            # Only match if the normalized event name is a substantial part of the query
            # or if they're similar in length (to prevent partial substring false matches)
            length_ratio = len(e_normalized) / len(q_normalized) if q_normalized else 0
            if length_ratio > 0.6 or e_normalized == q_normalized:
                matched.append(event)

    if len(matched) == 1:
        return matched[0]
    
    return None

def is_greeting(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated letters: heyyyy → heyy
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)

    greeting_words = {
        "hi", "hello", "hey", "hai", "hii", "heyy",
        "hola", "greetings", "yo","help","helpp"
    }

    filler_words = {
        "my", "dear", "bot", "there", "buddy",
        "friend", "bro", "man", "sir", "mam"
    }

    words = re.findall(r"\b[a-zA-Z]+\b", q_norm)

    # Remove fillers
    meaningful = [w for w in words if w not in filler_words]

    # Exact greeting match
    if any(w in greeting_words for w in meaningful):
        return True

    # Fuzzy greeting match (handles helo, hllo, helloo)
    for w in meaningful:
        for g in greeting_words:
            if similarity(w, g) >= 0.75:
                return True

    return False


def is_thankyou(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated letters: thanksss -> thankss
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)

    # Common thank-you variants
    thank_words = [
        "thanks", "thank you", "thankyou", "thx", "ty", "appreciate"
    ]

    # Direct phrase match
    for phrase in thank_words:
        if phrase in q_norm:
            return True

    # Fuzzy word-level match for spelling mistakes
    words = re.findall(r"\b[a-zA-Z]+\b", q_norm)
    for w in words:
        for t in ["thanks", "thank"]:
            if similarity(w, t) >= 0.7:
                return True

    return False

def is_bye(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated characters: byeee → byee → bye
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)

    # Common bye phrases
    bye_phrases = [
        "bye", "bye bye", "byebye", "goodbye", "good bye",
        "see you", "see ya", "cya",
        "tata", "ta ta", "later",
        "exit", "quit", "close", "sign off", "signoff","no","noo"
    ]

    # Phrase match (for multi-word goodbyes)
    for phrase in bye_phrases:
        if phrase in q_norm:
            return True

    # Word-level fallback (safe) - but make sure these are complete words
    words = set(re.findall(r"\b[a-zA-Z]+\b", q_norm))
    # Only match if EXACT word match, not substring
    return bool(words & {"bye", "goodbye", "tata", "later", "cya"})  # Removed "cu"



def is_okay(query: str) -> bool:
    """Check if message is a variation of 'ok' using flexible pattern matching"""
    q_lower = query.lower().strip()
    
    # Matches patterns like: ok, okay, okee, okeyy, okyyy, okeoke
    # Pattern explanation:
    # ^o      -> starts with 'o'
    # [k|kay] -> followed by 'k' or 'kay'
    # [ey|i]* -> optional trailing 'e', 'y', or 'i' 
    # +       -> repeated one or more times
    ok_pattern = r"^(ok|okay|oke|oky|okie|hokay|okeoke|k|kk|kkk|ogey|keke|okeokekk)[eyio]*$"
    
    # Also catch repetitive cases like "okeoke"
    if any(var in q_lower for var in ["okeoke", "ok ok"]):
        return True
        
    return bool(re.match(ok_pattern, q_lower))
def is_registration_query(query: str) -> bool:
    """Check if the query is about registration process"""
    q_lower = query.lower().strip()
    
    registration_keywords = [
        "how to register",
        "how do i register",
        "how can i register",
        "register for",
        "registration process",
        "registration steps",
        "how to participate",
        "how do i participate",
        "how to join",
        "how do i join",
        "how to enroll",
        "enrollment process",
        "sign up for",
        "how to sign up",
        "participate in event",
        "join the event",
        "registration procedure",
        "how register"
    ]
    
    return any(keyword in q_lower for keyword in registration_keywords)
def format_event_list(title: str, events: list[str]) -> str:
    event_lines = "\n".join(f"• {e}" for e in events)
    return f"{title}\n\n{event_lines}"


def is_goodbye(query: str) -> bool:
    """Check if message is a goodbye"""
    goodbyes = ["bye", "goodbye", "good bye", "see you", "see ya", "later", "farewell", "cya"]
    q_lower = query.lower().strip()
    return any(g in q_lower for g in goodbyes) and len(q_lower.split()) <= 3

def is_help_request(query: str) -> bool:
    """Check if user is asking for help"""
    help_keywords = ["help", "how to use", "what can you do", "how do you work", "guide", "assist"]
    q_lower = query.lower().strip()
    return any(h in q_lower for h in help_keywords) and len(q_lower.split()) <= 6

def is_identity_question(query: str) -> bool:
    """Check if user is asking who the bot is"""
    identity_patterns = ["who are you", "what are you", "your name", "who r u", "what r u"]
    q_lower = query.lower().strip()
    return any(p in q_lower for p in identity_patterns)

def is_capability_question(query: str) -> bool:
    """Check if user is asking what the bot can do"""
    capability_patterns = ["what can you", "what do you", "your capabilities", "can you help", 
                          "what can u", "what do u", "what you do"]
    q_lower = query.lower().strip()
    return any(p in q_lower for p in capability_patterns)

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
def detect_event_category(query: str):
    q = query.lower()

    is_general = any(w in q for w in ["general", "fun", "games"])
    is_cultural = any(w in q for w in ["cultural", "dance", "music", "arts"])
    is_technical = any(w in q for w in ["technical", "tech", "coding", "hack"])

    fest = fuzzy_fest_match(query)  # brahma / ashwamedha / None

    return fest, is_general, is_cultural, is_technical

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
        if is_meta_question(query):
            return "I’m here specifically to help with Brahma ’26 and Ashwamedha ’26 event-related queries."
        if is_abusive_query(query):
            return random.choice(ABUSE_RESPONSES)
        if is_greeting(query):
            return random.choice(GREETING_RESPONSES)
        
        # Handle thank you
        if is_thankyou(query):
            return random.choice(THANKYOU_RESPONSES)
        # Handle bye / exit
        if is_bye(query):
            return random.choice(BYE_RESPONSES)
        # Handle meta / personal bot questions
        # Quick fest detection - but only for simple queries
        fest = fuzzy_fest_match(query)
        if fest and is_simple_fest_query(query):
            if fest == "brahma":
                return random.choice(BRAHMA_RESPONSES)
            if fest == "ashwamedha":
                return random.choice(ASHWAMEDHA_RESPONSES)
        

        #handle okee
        if is_okay(query):
            return random.choice(OKAY_RESPONSES)
        if is_registration_query(query):
            return random.choice(REGISTRATION_RESPONSES)
        fest, is_general, is_cultural, is_technical = detect_event_category(query)

        if fest == "brahma":
            if is_general:
                return format_event_list(
                "🎯 Brahma ’26 – General Events",
                BRAHMA_GENERAL_EVENTS
                )

        if is_cultural:
                return format_event_list(
                "🎭 Brahma ’26 – Cultural Events",
                BRAHMA_CULTURAL_EVENTS
                )

        if is_technical:
            return format_event_list(
                "⚙️ Brahma ’26 – Technical Events",
                BRAHMA_TECHNICAL_EVENTS
                )

        if fest == "ashwamedha":
            return format_event_list(
                "⚙️ Ashwamedha ’26 – Technical Events",
                ASHWAMEDHA_TECHNICAL_EVENTS
                )

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
            return format_event_response(event, query)

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
            print("this is llm")
            
            # Cleanup
            gc.collect()
            
            return answer
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return "Sorry, I'm having trouble processing that request."

    except Exception as e:
        print(f"❌ Chat error: {e}")
        return "Sorry, something went wrong."
def format_event_response(event: dict, query: str = "") -> str:
    """Format event info with conversational response variations, optimized to answer only what's asked"""
    name = event.get("event_name", "Unknown Event")
    date = safe(event.get("date"))
    time = safe(event.get("time"))
    venue = safe(event.get("venue"))
    details = safe(event.get("details"), "")
    coordinator = format_names(event.get("coordinator"))
    fest = safe(event.get("fest"))
    slots = safe(event.get("slots"))
    poster = safe(event.get("poster"))
    amount = safe(event.get("amount"))
    category = safe(event.get("category"))
    
    q_lower = query.lower()
    
    # Detect what specific info is being asked
    asking_venue = any(word in q_lower for word in ["venue", "where", "location", "place", "held"])
    asking_time = any(word in q_lower for word in ["time", "when", "start", "begin"])
    asking_date = any(word in q_lower for word in ["date", "day", "when"])
    asking_coordinator = any(word in q_lower for word in ["coordinator", "contact", "who", "organize", "reach"])
    asking_what = any(word in q_lower for word in ["what", "about", "detail", "describe"])
    asking_fest = any(word in q_lower for word in ["fest", "festival", "occasion"])
    asking_slots = any(word in q_lower for word in ["slots", "seats", "vacancy", "available", "limit"])
    asking_poster = any(word in q_lower for word in ["poster", "image", "picture", "flyer"])
    asking_amount = any(word in q_lower for word in ["amount", "price", "fee", "cost", "registration", "charge"])
    asking_category = any(word in q_lower for word in ["category", "type", "kind", "genre"])
    
    # Count how many aspects are being asked
    aspects_count = sum([
        asking_venue, asking_time, asking_date, asking_coordinator, asking_what,
        asking_fest, asking_slots, asking_poster, asking_amount, asking_category
    ])
    
    # --- Single Aspect Logic ---
    
    # If only asking about venue
    if asking_venue and aspects_count == 1:
        responses = [
            f"{name} will be held at {venue}.",
            f"The venue for {name} is {venue}.",
            f"{name} is at {venue}.",
            f"You'll find {name} at {venue}.",
            f"The location is {venue} for {name}."
        ]
        return random.choice(responses)
    
    # If only asking about time
    if asking_time and not asking_date and aspects_count == 1:
        responses = [
            f"{name} starts at {time}.",
            f"The event begins at {time}.",
            f"{name} is scheduled for {time}.",
            f"It's at {time}.",
            f"The time is {time} for {name}."
        ]
        return random.choice(responses)
    
    # If only asking about date
    if asking_date and not asking_time and aspects_count == 1:
        responses = [
            f"{name} is on {date}.",
            f"The date is {date}.",
            f"It's happening on {date}.",
            f"{name} is scheduled for {date}.",
            f"Mark your calendar for {date}!"
        ]
        return random.choice(responses)

    # If only asking about amount
    if asking_amount and aspects_count == 1:
        return random.choice([
            f"The registration fee for {name} is {amount}.",
            f"It costs {amount} to participate in {name}.",
            f"The amount for {name} is {amount}."
        ])

    # If only asking about slots
    if asking_slots and aspects_count == 1:
        return random.choice([
            f"There are {slots} slots available for {name}.",
            f"{name} has {slots} seats left.",
            f"The slot limit for {name} is {slots}."
        ])

    # If only asking about poster
    if asking_poster and aspects_count == 1:
        if poster != "not specified":
            return f"You can check out the poster for {name} here: {poster}"
        return f"I'm sorry, the poster for {name} is not specified."

    # If only asking about category
    if asking_category and aspects_count == 1:
        return f"{name} is categorized as a {category} event."

    # If only asking about the fest
    if asking_fest and aspects_count == 1:
        return f"{name} is part of the {fest} festival."
    
    # If only asking about coordinator
    if asking_coordinator and aspects_count == 1:
        if coordinator != "not specified":
            responses = [
                f"The coordinator for {name} is {coordinator}.",
                f"You can contact {coordinator} for {name}.",
                f"{coordinator} is coordinating {name}.",
                f"Reach out to {coordinator} for more details about {name}.",
                f"The point of contact is {coordinator}."
            ]
            return random.choice(responses)
        else:
            return f"Coordinator information is not available for {name}."
    
    # If asking what the event is about
    if asking_what and aspects_count == 1 and details:
        responses = [
            f"{name} - {details}",
            f"{name} is {details.lower()}",
            f"It's {details.lower()}",
            f"{details}",
            f"{name}: {details}"
        ]
        return random.choice(responses)
    
    # --- Two-Field Combinations ---

    # If asking about when (date + time)
    if asking_date and asking_time and aspects_count == 2:
        responses = [
            f"{name} is on {date} at {time}.",
            f"It's scheduled for {date} at {time}.",
            f"{name} happens on {date}, starting at {time}.",
            f"The event is on {date} at {time}.",
            f"Mark {date} at {time} for {name}!"
        ]
        return random.choice(responses)
    
    # Time combinations
    if asking_time and asking_venue and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} at {venue}.",
            f"{name} is scheduled at {time} in {venue}.",
            f"The event takes place at {venue} at {time}.",
            f"You can attend {name} at {venue} starting at {time}."
        ])

    if asking_time and asking_coordinator and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} starts at {time} and is coordinated by {coordinator}.",
                f"The event begins at {time}. Coordinators: {coordinator}.",
                f"{coordinator} are coordinating {name}, which starts at {time}.",
                f"You can attend {name} at {time}. The coordinators are {coordinator}."
            ])
        else:
            return f"{name} starts at {time}, but coordinator details are not available."

    if asking_time and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} as part of {fest}.",
            f"The event is at {time} during {fest}.",
            f"{name} is scheduled for {time} in the {fest} festival.",
            f"You can catch {name} at {time} during {fest}."
        ])

    if asking_time and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} starts at {time}. Check the poster: {poster}",
                f"The event is at {time}. Poster here: {poster}",
                f"{name} begins at {time}. View poster: {poster}"
            ])
        return f"{name} starts at {time}, but the poster is not available."

    if asking_time and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} with a registration fee of {amount}.",
            f"The event is at {time} and costs {amount} to register.",
            f"{name} begins at {time}. Fee: {amount}."
        ])

    if asking_time and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event starting at {time}.",
            f"This {category} event begins at {time}.",
            f"{name} ({category}) is scheduled for {time}."
        ])

    if asking_time and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} with {slots} slots available.",
            f"The event is at {time} and has {slots} seats.",
            f"{name} begins at {time}. Slots: {slots}."
        ])

    # Date combinations
    if asking_date and asking_venue and aspects_count == 2:
        return random.choice([
            f"{name} is happening on {date} at {venue}.",
            f"The event will be held at {venue} on {date}.",
            f"{name} takes place on {date} in {venue}.",
            f"On {date}, {name} will be conducted at {venue}."
        ])

    if asking_date and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is on {date}. {details}",
            f"On {date}, {name} - {details}",
            f"{name} happens on {date}. It's {details.lower()}",
            f"{details} The event is on {date}."
        ])

    if asking_date and asking_coordinator and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} is on {date}. Coordinator: {coordinator}.",
                f"The event is on {date}, coordinated by {coordinator}.",
                f"{name} happens on {date}. Contact {coordinator} for details.",
                f"On {date}, {name} will be organized by {coordinator}."
            ])
        return f"{name} is on {date}, but coordinator details are not available."

    if asking_date and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} as part of {fest}.",
            f"The event is on {date} during {fest}.",
            f"{name} happens on {date} in the {fest} festival.",
            f"Mark {date} for {name} during {fest}!"
        ])

    if asking_date and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} with {slots} slots available.",
            f"The event is on {date} and has {slots} seats.",
            f"{name} happens on {date}. Slots: {slots}."
        ])

    if asking_date and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is on {date}. Check the poster: {poster}",
                f"The event is on {date}. Poster here: {poster}",
                f"Mark {date}! Poster: {poster}"
            ])
        return f"{name} is on {date}, but the poster is not available."

    if asking_date and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} with a registration fee of {amount}.",
            f"The event is on {date} and costs {amount}.",
            f"{name} happens on {date}. Fee: {amount}."
        ])

    if asking_date and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event happening on {date}.",
            f"This {category} event is on {date}.",
            f"{name} ({category}) is scheduled for {date}."
        ])

    # Coordinator combinations
    if asking_coordinator and asking_venue and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} will be held at {venue} and is coordinated by {coordinator}.",
                f"The venue for {name} is {venue}. Coordinators: {coordinator}.",
                f"{coordinator} are coordinating {name}, which will take place at {venue}.",
                f"You can find {name} at {venue}. The coordinators are {coordinator}."
            ])
        else:
            return f"{name} will be held at {venue}, but coordinator details are not available."

    if asking_coordinator and asking_fest and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} is part of {fest}, coordinated by {coordinator}.",
                f"{coordinator} are organizing {name} during {fest}.",
                f"The {fest} event {name} is coordinated by {coordinator}.",
                f"{name} ({fest}) - Coordinator: {coordinator}."
            ])
        return f"{name} is part of {fest}, but coordinator details are not available."

    if asking_coordinator and asking_slots and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} has {slots} slots. Coordinator: {coordinator}.",
                f"There are {slots} seats available. Contact {coordinator} for {name}.",
                f"{coordinator} are coordinating {name}, which has {slots} slots.",
                f"{name} - {slots} slots available. Reach out to {coordinator}."
            ])
        return f"{name} has {slots} slots, but coordinator details are not available."

    if asking_coordinator and asking_poster and aspects_count == 2:
        if coordinator != "not specified" and poster != "not specified":
            return random.choice([
                f"{name} is coordinated by {coordinator}. Poster: {poster}",
                f"Contact {coordinator} for {name}. Check poster: {poster}",
                f"Coordinator: {coordinator}. View poster here: {poster}"
            ])
        elif coordinator != "not specified":
            return f"{name} is coordinated by {coordinator}, but the poster is not available."
        return f"The poster is available at {poster}, but coordinator details are not specified."

    if asking_coordinator and asking_amount and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} has a registration fee of {amount}. Coordinator: {coordinator}.",
                f"The fee is {amount}. Contact {coordinator} for {name}.",
                f"{coordinator} are coordinating {name}, which costs {amount}.",
                f"{name} - Fee: {amount}. Reach out to {coordinator}."
            ])
        return f"{name} costs {amount}, but coordinator details are not available."

    if asking_coordinator and asking_category and aspects_count == 2:
        if coordinator != "not specified":
            return random.choice([
                f"{name} is a {category} event coordinated by {coordinator}.",
                f"This {category} event is organized by {coordinator}.",
                f"{coordinator} are coordinating {name} ({category}).",
                f"{name} ({category}) - Coordinator: {coordinator}."
            ])
        return f"{name} is a {category} event, but coordinator details are not available."

    # Venue combinations
    if asking_venue and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} during {fest}.",
            f"The venue is {venue} for this {fest} event.",
            f"{name} ({fest}) takes place at {venue}.",
            f"You can find {name} at {venue} during {fest}."
        ])

    if asking_venue and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} with {slots} slots available.",
            f"The venue is {venue} and there are {slots} seats.",
            f"{name} is at {venue}. Slots: {slots}."
        ])

    if asking_venue and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} will be held at {venue}. Poster: {poster}",
                f"The venue is {venue}. Check poster: {poster}",
                f"{name} is at {venue}. View poster here: {poster}"
            ])
        return f"{name} will be held at {venue}, but the poster is not available."

    if asking_venue and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} with a registration fee of {amount}.",
            f"The venue is {venue} and the fee is {amount}.",
            f"{name} is at {venue}. Fee: {amount}."
        ])

    if asking_venue and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event held at {venue}.",
            f"This {category} event takes place at {venue}.",
            f"{name} ({category}) will be at {venue}."
        ])

    if asking_venue and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} will be held at {venue}. {details}",
            f"The venue is {venue}. {details}",
            f"{name} is at {venue}. It's {details.lower()}"
        ])

    # Fest combinations
    if asking_fest and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} is part of {fest} with {slots} slots available.",
            f"This {fest} event has {slots} seats.",
            f"{name} ({fest}) - Slots: {slots}."
        ])

    if asking_fest and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is part of {fest}. Poster: {poster}",
                f"This {fest} event's poster: {poster}",
                f"{name} ({fest}) - View poster: {poster}"
            ])
        return f"{name} is part of {fest}, but the poster is not available."

    if asking_fest and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} is part of {fest} with a registration fee of {amount}.",
            f"This {fest} event costs {amount}.",
            f"{name} ({fest}) - Fee: {amount}."
        ])

    if asking_fest and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event in {fest}.",
            f"This {category} event is part of {fest}.",
            f"{name} ({category}) happens during {fest}."
        ])

    if asking_fest and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is part of {fest}. {details}",
            f"This {fest} event: {details}",
            f"{name} ({fest}) - {details}"
        ])

    # Slots combinations
    if asking_slots and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} has {slots} slots. Poster: {poster}",
                f"There are {slots} seats available. Check poster: {poster}",
                f"{name} - Slots: {slots}. View poster: {poster}"
            ])
        return f"{name} has {slots} slots, but the poster is not available."

    if asking_slots and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} has {slots} slots with a registration fee of {amount}.",
            f"There are {slots} seats available for {amount}.",
            f"{name} - Fee: {amount}, Slots: {slots}."
        ])

    if asking_slots and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event with {slots} slots available.",
            f"This {category} event has {slots} seats.",
            f"{name} ({category}) - Slots: {slots}."
        ])

    if asking_slots and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} has {slots} slots. {details}",
            f"There are {slots} seats available. {details}",
            f"{name} - Slots: {slots}. {details}"
        ])

    # Poster combinations
    if asking_poster and asking_amount and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} costs {amount}. Poster: {poster}",
                f"Registration fee: {amount}. Check poster: {poster}",
                f"{name} - Fee: {amount}. View poster: {poster}"
            ])
        return f"{name} costs {amount}, but the poster is not available."

    if asking_poster and asking_category and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is a {category} event. Poster: {poster}",
                f"This {category} event's poster: {poster}",
                f"{name} ({category}) - View poster: {poster}"
            ])
        return f"{name} is a {category} event, but the poster is not available."

    if asking_poster and asking_what and aspects_count == 2 and details:
        if poster != "not specified":
            return random.choice([
                f"{name} - {details} Poster: {poster}",
                f"{details} Check poster: {poster}",
                f"{name}: {details} View poster: {poster}"
            ])
        return f"{name} - {details} But the poster is not available."

    # Amount combinations
    if asking_amount and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event with a registration fee of {amount}.",
            f"This {category} event costs {amount}.",
            f"{name} ({category}) - Fee: {amount}."
        ])

    if asking_amount and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} costs {amount}. {details}",
            f"Registration fee: {amount}. {details}",
            f"{name} - Fee: {amount}. {details}"
        ])

    # Category combinations
    if asking_category and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is a {category} event. {details}",
            f"This {category} event: {details}",
            f"{name} ({category}) - {details}"
        ])

    # --- Three-Field Combinations ---

    # Logistics (Amount + Venue + Date)
    if asking_amount and asking_venue and asking_date and aspects_count == 3:
        return f"{name} is on {date} at {venue} with a registration fee of {amount}."

    # Registration (Amount + Slots)
    if asking_amount and asking_slots and aspects_count == 2:
        return f"For {name}, the registration fee is {amount} and there are {slots} slots available."

    # Event Details (Category + Fest)
    if asking_category and asking_fest and aspects_count == 2:
        return f"{name} is a {category} event happening during {fest}."

    # Full technical details (Amount + Slots + Category + Coordinator)
    if asking_amount and asking_slots and asking_category and asking_coordinator and aspects_count == 4:
        return f"{name} ({category}): The fee is {amount} for {slots} slots. Coordinator: {coordinator}."
    
    # Default: Full information with conversational variations
    templates = [
        f"{name} is a {category} event happening on {date} at {time} at {venue} as part of {fest}. Fee: {amount}. Slots: {slots}. {details}" + 
        (f" You can contact {coordinator} for more details." if coordinator != "not specified" else ""),
        
        f"Sure! {name} is a {category} event in {fest} scheduled for {date} at {time}. {details} Venue: {venue}. Amount: {amount}." +
        (f" For more info, reach out to {coordinator}." if coordinator != "not specified" else ""),
        
        f"{name} will be held on {date} at {time} at {venue}. This {category} event has {slots} slots and a fee of {amount}. {details}" +
        (f" If you have questions, contact {coordinator}." if coordinator != "not specified" else ""),
        
        f"Great question! {name} takes place on {date} at {time}. {details} Category: {category}. It's being held at {venue}." +
        (f" The coordinator is {coordinator}." if coordinator != "not specified" else ""),
        
        f"{name} is on {date} at {time}, venue is {venue}. This {fest} event costs {amount}. {details}" +
        (f" Get in touch with {coordinator} if you need more info." if coordinator != "not specified" else ""),
        
        f"{name} - {details} Category: {category}. Scheduled for {date} at {time}. Location: {venue}. Fee: {amount}." +
        (f" Contact: {coordinator}." if coordinator != "not specified" else "")
    ]
    
    return random.choice(templates)
