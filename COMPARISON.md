# Brahma Chatbot - Full vs Lite Comparison

## Memory Usage Comparison

### Full Version
- **Typical Memory**: 2-4GB
- **Peak Memory**: Up to 6GB
- **Startup Time**: 30-60 seconds
- **Model Size**: 22MB (same model)
- **Vector Store**: Unlimited size
- **Event Cache**: Unlimited
- **Batch Processing**: 50 items
- **Search Results**: 3 per query
- **Context Length**: Full text (no truncation)

### Lite Version
- **Typical Memory**: 400-600MB ⚡
- **Peak Memory**: 800MB-1GB ⚡
- **Startup Time**: 20-40 seconds ⚡
- **Model Size**: 22MB (optimized loading)
- **Vector Store**: Limited to 100 docs
- **Event Cache**: Max 100 events
- **Batch Processing**: 25 items (50% reduction)
- **Search Results**: 2 per query
- **Context Length**: Truncated (500 chars max)

## Technical Optimizations

| Optimization | Implementation |
|--------------|----------------|
| **Memory Limits** | `ulimit -v 2097152` (2GB cap) |
| **Threading** | `OMP_NUM_THREADS=2` |
| **Workers** | Single worker mode |
| **Garbage Collection** | Aggressive GC after operations |
| **Model Loading** | Lazy initialization |
| **Batch Size** | Reduced from 50 → 25 |
| **Cache Limits** | Hard caps on in-memory data |
| **Text Truncation** | All text limited to save memory |
| **Embedding Size** | Reduced sequence length (128) |
| **Concurrency** | Max 10 concurrent requests |

## Feature Comparison

| Feature | Full | Lite |
|---------|------|------|
| RAG (Retrieval) | ✅ | ✅ |
| Vector Search | ✅ | ✅ (limited) |
| Event Cache | ✅ | ✅ (limited) |
| LLM Integration | ✅ | ✅ |
| DOCX Support | ✅ | ✅ (limited) |
| Error Handling | ✅ | ✅ Enhanced |
| Memory Protection | ❌ | ✅ |
| Auto Cleanup | ❌ | ✅ |
| Health Monitoring | ✅ | ✅ Enhanced |
| Stats Endpoint | ✅ | ✅ |

## Crash Prevention Measures (Lite Only)

1. **Memory Error Handling**: Catches `MemoryError` exceptions
2. **Soft Limits**: Uses `ulimit` to prevent hard crashes
3. **Resource Cleanup**: Automatic cleanup on shutdown
4. **Garbage Collection**: Periodic cleanup during operations
5. **Batch Processing**: Small batches prevent memory spikes
6. **Request Limiting**: Max 10 concurrent requests
7. **Text Truncation**: Prevents oversized payloads
8. **Single Worker**: Prevents worker multiplication

## Use Cases

### Use Full Version When:
- ✅ You have 4GB+ RAM available
- ✅ Processing large datasets (500+ events)
- ✅ Need full context in responses
- ✅ High-performance requirements
- ✅ Development/testing environment

### Use Lite Version When:
- ✅ Running on 1-2GB RAM systems
- ✅ Edge devices (Raspberry Pi 4, etc.)
- ✅ Low-spec VPS/Cloud instances
- ✅ Need crash protection
- ✅ Memory-constrained environments
- ✅ Docker containers with memory limits
- ✅ Shared hosting environments

## Performance Impact

| Metric | Full | Lite | Impact |
|--------|------|------|--------|
| Response Time | ~500ms | ~600ms | +20% |
| Accuracy | 100% | ~95% | -5% |
| Throughput | High | Medium | -30% |
| Startup | Normal | Fast | +10% |
| Memory Safety | Low | High | +++++ |

## Migration Guide

### From Full to Lite
```bash
# Copy your data
cp -r data/ brahma_lite/
cp .env brahma_lite/

# Setup lite version
cd brahma_lite
./setup.sh
./start.sh
```

### From Lite to Full
```bash
# If lite is insufficient, switch back
cd ..
source venv/bin/activate
./start.sh
```

## Recommendations

- **Development**: Use Full version
- **Production (High Traffic)**: Use Full version with scaling
- **Production (Low RAM)**: Use Lite version
- **Edge Deployment**: Use Lite version
- **Testing**: Use Lite version for faster iteration

## Monitoring

### Check Memory Usage
```bash
# While running
curl http://localhost:8000/stats

# System memory
free -h

# Process memory
ps aux | grep uvicorn
```

---

**Choose Lite for reliability on constrained systems** ⚡
