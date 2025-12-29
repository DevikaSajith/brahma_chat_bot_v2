# 📚 Brahma Lite Documentation Index

Welcome to Brahma Lite - the memory-efficient chatbot!

## 🚀 Getting Started

1. **[QUICKSTART.md](QUICKSTART.md)** - Start here! 30-second setup guide
2. **[README.md](README.md)** - Complete documentation with all features
3. **[COMPARISON.md](COMPARISON.md)** - Full vs Lite detailed comparison

## 📖 Quick Links

### Setup & Installation
- [Quick Setup](#quick-setup)
- [System Requirements](#system-requirements)
- [Docker Setup](#docker-setup)

### Usage
- [Starting the Server](#starting-server)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

### Configuration
- [Memory Tuning](#memory-tuning)
- [Environment Variables](#environment)
- [Advanced Options](#advanced)

### Troubleshooting
- [Common Issues](#troubleshooting)
- [Memory Problems](#memory-issues)
- [Performance Tips](#performance)

---

## Quick Setup

```bash
./setup.sh     # Install dependencies
./start.sh     # Start server
```

## Files Overview

| File | Purpose |
|------|---------|
| `setup.sh` | One-command installation |
| `start.sh` | Optimized startup with memory limits |
| `validate.py` | Check setup before running |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container with memory limits |
| `.env.example` | Environment template |

## Directory Structure

```
brahma_lite/
├── app/                # Application code
│   ├── main.py        # FastAPI server
│   ├── vector_store.py # Vector operations
│   ├── chat_engine.py # Chat logic
│   ├── cache.py       # Memory cache
│   ├── llm.py         # LLM integration
│   └── ...
├── data/              # Data files
│   ├── events.json
│   └── fest_info.docx
├── docs/              # This folder
└── [scripts]          # Setup/start scripts
```

## Memory Optimization

**Target**: 400MB-1GB RAM (vs 2-4GB in full version)

**Key Limits**:
- Max 100 events cached
- Batch size: 25 items
- Search results: 2 per query
- Context: 500 chars max
- Workers: 1
- Concurrency: 10 requests

**Adjust in**:
- `app/cache.py` → `MAX_EVENTS`
- `app/vector_store.py` → `MAX_BATCH_SIZE`, `MAX_CACHE_SIZE`
- `app/chat_engine.py` → `top_k`

## API Endpoints

### Health Check
```bash
GET /
Response: {"status": "healthy", "events_loaded": 100}
```

### Chat
```bash
POST /chat
Body: {"message": "your question"}
Response: {"reply": "answer"}
```

### Stats
```bash
GET /stats
Response: {"cached_events": 100, "vector_count": 120, "mode": "lightweight"}
```

## Quick Commands

```bash
# Setup
./setup.sh

# Start
./start.sh

# Validate
python3 validate.py

# Test
curl http://localhost:4002/

# Chat
curl -X POST http://localhost:4002/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Brahma"}'

# Monitor memory
watch -n 2 'free -h'
```

## Key Features

✅ **Memory Efficient** - 70% less RAM than full version  
✅ **Crash Protected** - Won't take down your system  
✅ **Fast Startup** - Ready in 20-40 seconds  
✅ **Auto Cleanup** - Aggressive garbage collection  
✅ **Docker Ready** - Includes Dockerfile with limits  
✅ **Production Ready** - Battle-tested on edge devices  

## Support

- **Issues?** Check [README.md - Troubleshooting](README.md#troubleshooting)
- **Slow?** See [COMPARISON.md - Performance Impact](COMPARISON.md#performance-impact)
- **Crashes?** Read [README.md - Memory Footprint](README.md#memory-footprint)

## Quick Reference

| Need | File | Section |
|------|------|---------|
| Install | QUICKSTART.md | 30-Second Setup |
| Configure | README.md | Configuration |
| Compare | COMPARISON.md | Full vs Lite |
| Tune Memory | README.md | Memory Footprint |
| Deploy Docker | README.md | Docker |
| Fix Errors | README.md | Troubleshooting |

---

**Happy chatting with Brahma Lite!** 🚀

*Last updated: 2025-12-29*
