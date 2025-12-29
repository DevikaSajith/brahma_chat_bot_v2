#!/usr/bin/env python3
"""
Test chatbot responses for greetings and other conversational messages
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.json_store import load_events_from_json
from app.cache import load_event_cache
from app.chat_engine import chat

# Load minimal data
events = load_events_from_json()
load_event_cache(events)

print("🤖 Testing Chatbot Responses")
print("="*70 + "\n")

test_cases = [
    ("hi", "Should greet back"),
    ("hello", "Should greet back"),
    ("hey there", "Should greet back"),
    ("hai", "Should greet back"),
    ("thanks", "Should respond to thanks"),
    ("thank you", "Should respond to thanks"),
    ("what is brahma", "Should explain Brahma"),
    ("random question", "Should say out of context"),
    ("explain bhrahma", "Should explain Brahma (fuzzy match)"),
    ("when is theme show", "Should respond with event info"),
]

for query, expected in test_cases:
    print(f"📝 Q: '{query}'")
    print(f"   Expected: {expected}")
    response = chat(query)
    print(f"   ✅ R: {response[:100]}...")
    print()
