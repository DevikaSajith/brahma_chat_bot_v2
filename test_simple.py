#!/usr/bin/env python3
"""
Simple test for greetings without loading vector store
"""

import re
import random
from difflib import SequenceMatcher

# Copy the response lists
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

BRAHMA_RESPONSES = [
    "Brahma '26 is the annual cultural festival of Adi Shankara Institute of Engineering and Technology (ASIET), celebrating music, dance, art, and creative expression.",
    "Brahma is ASIET's flagship cultural fest featuring competitive events, pro-shows, and workshops."
]

OUT_OF_CONTEXT = [
    "I can help only with Brahma '26 and ASIET events.",
    "That's not related to the Brahma festival."
]

def is_greeting(query: str) -> bool:
    """Check if message is a greeting"""
    greetings = ["hi", "hello", "hey", "hai", "hii", "helo", "hola", "greetings", 
                 "good morning", "good afternoon", "good evening", "howdy", "yo"]
    q_lower = query.lower().strip()
    
    if q_lower in greetings:
        return True
    
    words = re.findall(r"\b[a-zA-Z]+\b", q_lower)
    return any(word in greetings for word in words) and len(words) <= 3

def is_thankyou(query: str) -> bool:
    """Check if message is a thank you"""
    thanks = ["thanks", "thank you", "thankyou", "thx", "ty", "appreciate"]
    q_lower = query.lower().strip()
    return any(t in q_lower for t in thanks)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def fuzzy_fest_match(query: str) -> str:
    """Check if query mentions Brahma"""
    q_lower = query.lower()
    brahma_variants = ["brahma", "brama", "bhrahma", "brahama"]
    
    for v in brahma_variants:
        if v in q_lower:
            return "brahma"
    
    words = re.findall(r"\b[a-zA-Z]+\b", q_lower)
    for word in words:
        if len(word) >= 4:
            for v in brahma_variants:
                if similarity(word, v) >= 0.72:
                    return "brahma"
    return None

def is_simple_fest_query(query: str) -> bool:
    """Check if it's a simple 'what is brahma' query"""
    q_lower = query.lower().strip()
    
    # Deep question indicators
    deep_keywords = ["history", "when started", "why called", "origin", "background", 
                     "story", "past", "previous", "details about", "more about"]
    
    if any(keyword in q_lower for keyword in deep_keywords):
        return False  # Deep question
    
    # Simple "what is brahma" style - short queries
    words = q_lower.split()
    if len(words) <= 4 and any(w in ["what", "whats", "explain", "tell", "brahma"] for w in words):
        return True
    
    # Just "brahma" alone
    if re.match(r"^bh?rama\??$", q_lower):
        return True
    
    return False

def simple_chat(query: str) -> str:
    """Simplified chat without vector store"""
    query = query.strip()
    
    # Greetings
    if is_greeting(query):
        return random.choice(GREETING_RESPONSES)
    
    # Thank you
    if is_thankyou(query):
        return random.choice(THANKYOU_RESPONSES)
    
    # Brahma - only simple queries
    fest = fuzzy_fest_match(query)
    if fest == "brahma" and is_simple_fest_query(query):
        return random.choice(BRAHMA_RESPONSES)
    
    # Deep questions need semantic search
    if fest == "brahma" and not is_simple_fest_query(query):
        return "[Would use semantic search for: " + query + "]"
    
    # Out of context
    return random.choice(OUT_OF_CONTEXT)

# Test
print("🤖 Testing Simple Responses (No Vector DB)")
print("="*70 + "\n")
thanks",
    "what is brahma",          # Simple - should return generic
    "explain bhrahma",         # Simple - should return generic
    "brahma",                  # Simple - should return generic
    "history of brahma",       # Deep - should use semantic search
    "tell me more about brahma history",  # Deep - needs search
    "when was brahma started", # Deep - needs search
    "background of brahma",    # Deep - needs search
    "what events in brahma",   # Deep - needs search
    "random question",         # Out of contexta",
    "explain bhrahma",
    "tell me about brama",
    "random question",
    "how are you",
]

for query in tests:
    response = simple_chat(query)
    print(f"Q: '{query}'")
    print(f"A: {response}\n")
