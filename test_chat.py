#!/usr/bin/env python3
"""
Test chat logic without running the full server
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.json_store import load_events_from_json
from app.cache import load_event_cache
from app.chat_engine import chat, fuzzy_fest_match, is_relevant_query

print("🧪 Testing Chat Logic\n")

# Load data
events = load_events_from_json()
load_event_cache(events)

# Test cases
test_queries = [
    "explain bhrahma",
    "what is brahma",
    "tell me about brama",
    "when is theme show",
    "random unrelated question",
]

print("="*60)
for query in test_queries:
    print(f"\n📝 Query: '{query}'")
    
    # Check fuzzy match
    fest = fuzzy_fest_match(query)
    print(f"   Fest Match: {fest}")
    
    # Check relevance
    relevant = is_relevant_query(query)
    print(f"   Is Relevant: {relevant}")
    
    # Get response (without vector store/LLM)
    try:
        # Just test the routing logic
        if fest:
            print(f"   ✅ Would return: {fest.upper()} response")
        elif relevant:
            print(f"   ✅ Would proceed to semantic search")
        else:
            print(f"   ❌ Would return: Out of context")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("-"*60)

print("\n✅ Test complete")
