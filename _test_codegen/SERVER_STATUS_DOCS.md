# Server Status Feature Documentation

> **Enhanced AI Server Status Checking**

---

## Overview

Menu 3 now provides **comprehensive server status** with detailed information about:
- Process status
- API health
- Performance metrics
- Configuration details
- Server uptime

---

## Usage

From the main menu:
```
Select [0-11]: 3
```

### Example Output

```
============================================================
  AI Server Status
============================================================

  Process:    Running ✓
  PID:        12345
  Uptime:     5 minutes 23 seconds

  API:        Responding ✓
  Response:   45ms
  Models:     1 available
  Speed:      Fast ✓

  Configuration:
    Port:       8080
    Host:       127.0.0.1
    Model:      google_gemma-4-E2B-it-Q4_K_M.gguf
    Context:    4096
    Threads:    4
    Batch Size: 512

  API Endpoint: http://127.0.0.1:8080/v1
  Chat API:     http://127.0.0.1:8080/v1/chat/completions

============================================================
```

---

## Status Indicators

### Process Status
- 🟢 **Running ✓** - Server process is active
- 🔴 **Not running ✗** - Server process has stopped

### API Health
- 🟢 **Responding ✓** - API endpoints working
- 🔴 **Not responding ✗** - API not accessible

### Performance
- 🟢 **Fast ✓** - Response time < 100ms
- 🟡 **Moderate ⚠** - Response time 100-500ms
- 🔴 **Slow ✗** - Response time > 500ms

---

## New Methods Added

### 1. `get_server_status()`
Returns comprehensive status dictionary:

```python
status = coder.get_server_status()

# Returns:
{
    'running': True,              # Internal flag
    'process_alive': True,        # Process is running
    'pid': 12345,                 # Process ID
    'uptime': '5 minutes 23 seconds',
    'api_health': {...},          # API health dict
    'config': {...},              # Server configuration
    'model_name': 'google_gemma-4-E2B-it-Q4_K_M.gguf'
}
```

### 2. `get_server_uptime()`
Calculates server uptime:

```python
uptime = coder.get_server_uptime()
# Returns: "5 minutes 23 seconds"
# Returns: "N/A" if not running
```

### 3. `get_api_health()`
Tests API endpoint health:

```python
health = coder.get_api_health()

# Returns:
{
    'api_responsive': True,
    'models_endpoint': True,
    'models_count': 1,
    'response_time_ms': 45,
    'error': None
}
```

### 4. `check_server_status()` (Menu 3)
Displays full status to user:

```python
is_running = coder.check_server_status()
# Prints formatted status to console
# Returns True if server is running
```

---

## What Menu 3 Shows

### 1. Process Information
```
Process:    Running ✓
PID:        12345
Uptime:     5 minutes 23 seconds
```

- **Process**: Whether llama-server.exe is running
- **PID**: Process ID (useful for task manager)
- **Uptime**: How long server has been running

### 2. API Health
```
API:        Responding ✓
Response:   45ms
Models:     1 available
Speed:      Fast ✓
```

- **API**: Can reach /v1/models endpoint
- **Response**: Round-trip time in milliseconds
- **Models**: Number of models loaded
- **Speed**: Performance indicator

### 3. Configuration
```
Configuration:
  Port:       8080
  Host:       127.0.0.1
  Model:      google_gemma-4-E2B-it-Q4_K_M.gguf
  Context:    4096
  Threads:    4
  Batch Size: 512
```

Current server settings from config file.

### 4. API Endpoints
```
API Endpoint: http://127.0.0.1:8080/v1
Chat API:     http://127.0.0.1:8080/v1/chat/completions
```

Useful URLs for API access.

---

## Error Messages

### Server Not Running
```
Process:    Not running ✗
```

**Solution:** Start server with Menu 1

### API Not Responding
```
API:        Not responding ✗
Error:      Timeout (>3s)
```

**Possible causes:**
- Server still loading model
- Server is busy processing
- Port conflict

**Solutions:**
- Wait a few seconds and try again
- Check if model is still loading
- Restart server (Menu 2, then Menu 1)

### Connection Refused
```
API:        Not responding ✗
Error:      Connection refused
```

**Cause:** Server process died or wrong port

**Solution:** Restart server with Menu 1

---

## Performance Guidelines

| Response Time | Status | Action |
|---------------|--------|--------|
| < 100ms | 🟢 Fast | Ideal |
| 100-500ms | 🟡 Moderate | Acceptable |
| > 500ms | 🔴 Slow | Consider reducing context size |

---

## Testing

Run the test suite:

```powershell
python test_server_status.py
```

Tests verify:
- ✅ Status methods work when server not running
- ✅ Uptime calculation correct
- ✅ API health check functional
- ✅ Live server status display

---

## Use Cases

### 1. Quick Check
Before using AI tools, check Menu 3 to ensure server is ready.

### 2. Performance Monitoring
If AI responses seem slow, use Menu 3 to check response time.

### 3. Troubleshooting
If AI tools fail, check Menu 3 to diagnose:
- Is server running?
- Is API responding?
- What's the error message?

### 4. API Integration
Menu 3 shows the exact API endpoints for external tools.

---

## Implementation Details

### Dependencies
- Uses `psutil` for process uptime (optional)
- Falls back gracefully if psutil not installed

### Error Handling
- All methods catch and report errors
- No crashes on connection failures
- Graceful degradation

### Performance
- API health check has 3-second timeout
- Non-blocking status checks
- Minimal overhead

---

**Menu 3 now gives you complete visibility into AI server health! 🚀**
