#!/usr/bin/env python3
"""
Quick load test - Tests the exact questions you specified
"""

import requests
import time
import concurrent.futures
import sys

BASE_URL = "http://localhost:4002"
QUESTIONS = [
    "what is bhrahma",
    "what is aswamedha", 
    "bhrahma",
    "hai"
]

def test_question(question, iteration):
    """Test a single question"""
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": question},
            timeout=10
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            reply = response.json().get("reply", "")
            status = "✅" if "something went wrong" not in reply.lower() else "❌"
            print(f"{status} [{elapsed:.2f}s] Q: '{question}' | R: {reply[:60]}...")
            return True
        else:
            print(f"❌ [{elapsed:.2f}s] Q: '{question}' | Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Q: '{question}' | Error: {e}")
        return False

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🧪 Quick Load Test for Brahma Lite")
    print("="*70)
    
    # Check server
    if not check_server():
        print("❌ Server not running on http://localhost:4002")
        print("   Start it with: ./start_safe.sh")
        sys.exit(1)
    
    print("✅ Server is running\n")
    
    # Get parameters
    num_requests = int(input("Number of requests per question [10]: ") or "10")
    concurrent = int(input("Concurrent users [5]: ") or "5")
    
    print(f"\n🚀 Testing with {num_requests} requests per question, {concurrent} concurrent users")
    print(f"   Total requests: {num_requests * len(QUESTIONS)}")
    print(f"   Questions: {', '.join(QUESTIONS)}")
    print("\n" + "="*70 + "\n")
    
    # Create test tasks
    tasks = []
    for i in range(num_requests):
        for question in QUESTIONS:
            tasks.append((question, i))
    
    # Run tests
    success_count = 0
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
        results = list(executor.map(lambda t: test_question(t[0], t[1]), tasks))
        success_count = sum(results)
    
    elapsed = time.time() - start_time
    
    # Results
    print("\n" + "="*70)
    print(f"\n📊 Results:")
    print(f"   Total requests: {len(tasks)}")
    print(f"   Successful: {success_count}")
    print(f"   Failed: {len(tasks) - success_count}")
    print(f"   Success rate: {success_count/len(tasks)*100:.1f}%")
    print(f"   Total time: {elapsed:.2f}s")
    print(f"   Avg time/request: {elapsed/len(tasks):.2f}s")
    print(f"   Requests/second: {len(tasks)/elapsed:.2f}")
    
    # Check server still alive
    print("\n🔍 Checking server status...")
    if check_server():
        print("✅ Server still running - No crash!\n")
        try:
            stats = requests.get(f"{BASE_URL}/stats", timeout=5).json()
            print(f"📊 Server stats:")
            print(f"   Cached events: {stats.get('cached_events', 'N/A')}")
            print(f"   Vector count: {stats.get('vector_count', 'N/A')}")
            print(f"   Mode: {stats.get('mode', 'N/A')}")
        except:
            pass
    else:
        print("❌ Server crashed or stopped!\n")

if __name__ == "__main__":
    main()
