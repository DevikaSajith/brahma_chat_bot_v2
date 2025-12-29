# Load Testing Guide

## Prerequisites

Install Locust:
```bash
pip install locust
```

## Quick Start

### Option 1: Automated Script
```bash
./run_load_test.sh
```

Choose from preset scenarios:
1. **Light** - 10 users, good for initial testing
2. **Medium** - 50 users, moderate load
3. **Heavy** - 100 users, high load
4. **Stress** - 200 users, maximum stress
5. **Custom** - Define your own parameters

### Option 2: Manual Locust

#### Web UI Mode (Recommended for monitoring)
```bash
locust -f locustfile.py --host=http://localhost:4002
```
Then open: http://localhost:8089

#### Headless Mode (Automated)
```bash
locust -f locustfile.py \
    --host=http://localhost:4002 \
    --users=50 \
    --spawn-rate=5 \
    --run-time=3m \
    --headless \
    --html=report.html
```

## Test Scenarios

### Light Test (Smoke Test)
```bash
locust -f locustfile.py --host=http://localhost:4002 \
    --users=10 --spawn-rate=2 --run-time=2m --headless
```
**Purpose**: Verify basic functionality, no crashes

### Medium Test
```bash
locust -f locustfile.py --host=http://localhost:4002 \
    --users=50 --spawn-rate=5 --run-time=3m --headless
```
**Purpose**: Test under moderate load

### Heavy Test
```bash
locust -f locustfile.py --host=http://localhost:4002 \
    --users=100 --spawn-rate=10 --run-time=5m --headless
```
**Purpose**: Stress test, find breaking point

### Stress Test
```bash
locust -f locustfile.py --host=http://localhost:4002 \
    --users=200 --spawn-rate=20 --run-time=5m --headless
```
**Purpose**: Maximum stress, test crash resistance

## What Gets Tested

### Questions Tested
- "what is bhrahma"
- "what is aswamedha"
- "bhrahma"
- "hai" (out of context)
- Event-related questions
- Health checks
- Stats endpoint

### Task Distribution
- **50%** - Basic chat questions (bhrahma, aswamedha, hai)
- **30%** - Event-related questions
- **15%** - Health checks
- **5%** - Stats checks

## Monitoring During Test

### Terminal 1 - Server
```bash
cd brahma_lite
./start_safe.sh
```

### Terminal 2 - Server Stats
```bash
watch -n 2 'curl -s http://localhost:4002/stats | python3 -m json.tool'
```

### Terminal 3 - Memory Usage
```bash
watch -n 2 'free -h && echo "" && ps aux | grep uvicorn | head -3'
```

### Terminal 4 - Load Test
```bash
locust -f locustfile.py --host=http://localhost:4002
```

## Interpreting Results

### Success Indicators
- ✅ Response time < 2 seconds (95th percentile)
- ✅ 0% failure rate
- ✅ Server stays running throughout test
- ✅ Memory stays under 1.5GB
- ✅ No "Aborted (core dumped)" errors

### Warning Signs
- ⚠️ Response time > 5 seconds
- ⚠️ Failure rate > 5%
- ⚠️ Memory keeps growing
- ⚠️ Error responses increase over time

### Failure Indicators
- ❌ Server crashes
- ❌ Failure rate > 20%
- ❌ Response timeout
- ❌ Out of memory errors

## Output Files

After test completes:
- `load_test_report.html` - Visual report
- `load_test_results_stats.csv` - Statistics
- `load_test_results_failures.csv` - Failures
- `load_test_results_exceptions.csv` - Exceptions

## Custom Test Users

### Using BrahmaChatUser (Default)
Normal paced testing with realistic wait times
```bash
locust -f locustfile.py BrahmaChatUser --host=http://localhost:4002
```

### Using StressTestUser
Aggressive rapid-fire testing
```bash
locust -f locustfile.py StressTestUser --host=http://localhost:4002
```

## Comparing with Full Version

To test if lite version is more stable:

### Test Full Version
```bash
cd ../  # Go to full version
# Start full version server
./start.sh

# In another terminal
cd brahma_lite
locust -f locustfile.py --host=http://localhost:8000 \
    --users=100 --spawn-rate=10 --run-time=5m --headless \
    --html=full_version_report.html
```

### Test Lite Version
```bash
cd brahma_lite
./start_safe.sh

# In another terminal
locust -f locustfile.py --host=http://localhost:4002 \
    --users=100 --spawn-rate=10 --run-time=5m --headless \
    --html=lite_version_report.html
```

### Compare
- Check if lite version has lower memory usage
- Check if lite version stays stable longer
- Compare response times and failure rates

## Advanced Options

### Distributed Load Testing
Run on multiple machines:

**Master:**
```bash
locust -f locustfile.py --master --host=http://localhost:4002
```

**Workers:**
```bash
locust -f locustfile.py --worker --master-host=<master-ip>
```

### Step Load Testing
Gradually increase load:
```bash
locust -f locustfile.py --host=http://localhost:4002 \
    --users=100 --spawn-rate=1 --run-time=10m --headless
```

## Troubleshooting

### Server Crashes During Test
- Reduce number of users
- Decrease spawn rate
- Check memory usage
- Review server logs
- Try `./start_safe.sh` instead of `./start.sh`

### High Failure Rate
- Check server is responsive: `curl http://localhost:4002/`
- Review server logs
- Test with fewer users first
- Check `.env` file has valid API key

### Slow Response Times
- Normal for lite version under heavy load
- Memory constraints affect performance
- Try reducing concurrent users
- Check if vector search is the bottleneck

---

**Goal**: Verify lite version can handle load without crashing like full version did!
