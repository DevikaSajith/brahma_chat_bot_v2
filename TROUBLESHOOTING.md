# Troubleshooting Core Dump / Crash Issues

## Problem: "Aborted (core dumped)" after startup

This can happen due to several reasons:

### Solution 1: Use Safe Mode Startup (Recommended)

```bash
./start_safe.sh
```

This removes aggressive memory limits that can cause crashes.

### Solution 2: Debug Mode

```bash
python3 run_debug.py
```

This provides better error messages.

### Solution 3: Check ChromaDB

The crash might be ChromaDB-related. Try clearing the vector store:

```bash
rm -rf vector_store_lite/
./start_safe.sh
```

### Solution 4: Reduce Batch Size

Edit `app/vector_store.py`:
```python
MAX_BATCH_SIZE = 10  # Change from 25 to 10
```

### Solution 5: Skip Vector Store (Testing Only)

Temporarily comment out vector store in `app/main.py`:

```python
# build_vector_store(events)  # Comment this line
```

### Solution 6: Check Dependencies

```bash
# Reinstall ChromaDB
pip uninstall chromadb -y
pip install chromadb==0.4.24  # Use older stable version

# Or try newer version
pip install --upgrade chromadb
```

### Solution 7: Check System Limits

```bash
# Check core dump settings
ulimit -c

# Disable core dumps
ulimit -c 0

# Then start
./start_safe.sh
```

### Solution 8: Use Python Directly

```bash
python3 -c "from app.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=4002)"
```

## Common Causes

1. **Memory corruption** - ChromaDB or Sentence Transformers issue
2. **Thread conflicts** - OMP threads conflicting
3. **Aggressive ulimit** - Hard memory limits causing abort
4. **Signal handling** - Trap in start.sh interfering

## Quick Fixes

### Minimal Startup
```bash
cd brahma_lite
source venv/bin/activate
export OMP_NUM_THREADS=2
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 4002
```

### Without Vector Store
Edit `app/main.py` and comment out:
```python
# build_vector_store(events)
```

This will still allow basic chat functionality.

## Getting More Info

```bash
# Enable core dumps to see what crashed
ulimit -c unlimited
./start.sh

# Check the core dump
gdb python3 core
# Type: bt (for backtrace)
```

## Still Crashing?

Try the absolute minimal version:

```bash
# Start without any optimizations
python3 -c "
import os
os.environ['OMP_NUM_THREADS'] = '1'
from app.main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=4002)
"
```
