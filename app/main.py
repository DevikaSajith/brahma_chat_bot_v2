from fastapi import FastAPI
from pydantic import BaseModel
from app.chat_engine import chat
from app.json_store import load_events_from_json
from app.cache import load_event_cache
from app.vector_store import build_vector_store, cleanup_resources
import traceback
import gc
import os
import signal
import sys

# ⚡ LIGHTWEIGHT: Limit worker threads
os.environ['UVICORN_WORKERS'] = '1'
os.environ['OMP_NUM_THREADS'] = '2'

# Handle signals gracefully
def signal_handler(sig, frame):
    print("\n⚠️ Received shutdown signal")
    cleanup_resources()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app = FastAPI(
    title="Brahma Lite Chatbot",
    description="Memory-efficient version (1-2GB RAM)",
    version="1.0-lite"
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class HealthResponse(BaseModel):
    status: str
    events_loaded: int


@app.on_event("startup")
def startup_event():
    """Initialize with memory constraints"""
    print("🚀 Starting Brahma Lite Chatbot...")
    print("⚡ Memory-efficient mode enabled")
    
    try:
        # Load events
        events = load_events_from_json()
        if not events:
            print("⚠️ No events loaded")
            return

        # Load into memory cache (limited)
        load_event_cache(events)

        # Build vector store (batch processing)
        build_vector_store(events)

        # Don't cleanup model immediately - keep it loaded
        # gc.collect()
        
        print(f"✅ Lite mode ready with {len(events)} events")
        print(f"💾 Memory footprint minimized")
        print("📡 Server ready to accept requests")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        traceback.print_exc()
        # Don't crash the whole app
        import sys
        sys.exit(1)


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    print("🧹 Cleaning up resources...")
    cleanup_resources()
    gc.collect()


@app.get("/", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    from app.cache import EVENT_CACHE
    return {
        "status": "healthy",
        "events_loaded": len(EVENT_CACHE)
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Chat endpoint with error handling"""
    try:
        # Truncate very long messages
        message = req.message[:500] if len(req.message) > 500 else req.message
        
        answer = chat(message)
        
        # Periodic garbage collection
        gc.collect()
        
        return {"reply": answer}

    except MemoryError:
        print("❌ MEMORY ERROR - System under pressure")
        gc.collect()
        return {
            "reply": "System is under memory pressure. Please try again."
        }
    
    except Exception as e:
        print(f"❌ CHAT ERROR: {e}")
        traceback.print_exc()
        return {
            "reply": "Sorry, something went wrong. Please try again."
        }


@app.get("/stats")
def stats():
    """System stats endpoint"""
    from app.cache import EVENT_CACHE
    from app.vector_store import _collection
    
    return {
        "cached_events": len(EVENT_CACHE),
        "vector_count": _collection.count() if _collection else 0,
        "mode": "lightweight"
    }
