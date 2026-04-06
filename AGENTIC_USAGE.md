# Using llama.cpp as Agentic AI

## Overview
llama.cpp can serve as a local AI agent for coding assistants, research, and automation tasks.

---

## 1. OpenCode Integration

OpenCode can use llama.cpp as its AI backend via OpenAI-compatible API.

### Start the Server
```
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --host 127.0.0.1 --port 8080
```

### Configure OpenCode
Set the API endpoint to your local server:
```
OPENAI_BASE_URL=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
```

Then OpenCode will route all AI requests to your local Gemma 4.

---

## 2. Qwen Code (This CLI)

Qwen Code can be configured to use local llama.cpp:

### Method: Environment Variables
```powershell
$env:OPENAI_BASE_URL = "http://127.0.0.1:8080/v1"
$env:OPENAI_API_KEY = "local"
qwen
```

### Method: Config File
Create `.qwen/config.json`:
```json
{
  "api": {
    "baseUrl": "http://127.0.0.1:8080/v1",
    "apiKey": "local"
  }
}
```

---

## 3. HTTP API Usage

llama.cpp server provides OpenAI-compatible endpoints.

### Start Server
```
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```

### Chat Completion (curl)
```powershell
curl http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"gemma4\",\"messages\":[{\"role\":\"user\",\"content\":\"What is 2+2?\"}]}"
```

### Completion (curl)
```powershell
curl http://127.0.0.1:8080/v1/completions -H "Content-Type: application/json" -d "{\"model\":\"gemma4\",\"prompt\":\"Write a Python function to\",\"n_predict\":100}"
```

### Web UI
Open browser: `http://127.0.0.1:8080`

---

## 4. Agentic Workflow Examples

### Code Assistant
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 4096 -p "You are a Python coding assistant. Write clean, efficient code."
```

### Research Agent
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 4096 -p "You are a research assistant. Analyze and summarize technical topics."
```

### QA Agent
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 4096 -p "You are a QA engineer. Review code for bugs and suggest improvements."
```

---

## 5. Integration with Other Tools

### Continue (VS Code Extension)
Add to `~/.continue/config.json`:
```json
{
  "models": [{
    "title": "Gemma 4 Local",
    "provider": "openai",
    "model": "gemma4",
    "apiBase": "http://127.0.0.1:8080/v1"
  }]
}
```

### AnythingLLM
1. Start llama.cpp server on port 8080
2. In AnythingLLM settings, add "OpenAI Compatible" provider
3. URL: `http://127.0.0.1:8080/v1`
4. API Key: `local`

### Text Generation WebUI (oobabooga)
Use the "OpenAI API" extension mode pointing to `http://127.0.0.1:8080`

---

## 6. Server Options Reference

| Flag | Description | Default |
|------|-------------|---------|
| `-m` | Model path | required |
| `-c` | Context size | 4096 |
| `--host` | Bind address | 127.0.0.1 |
| `--port` | Port number | 8080 |
| `-t` | Threads | auto |
| `--threads-batch` | Batch threads | auto |
| `-b` | Batch size | 2048 |
| `-ub` | Ubatch size | 512 |
| `--cache-type-k` | KV cache type | f16 |

### Low RAM Server (8GB)
```
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 2048 -t 4 -b 512
```

---

## 7. Performance Tips

### For 8GB RAM
- Context: `-c 2048` (lower = less RAM)
- Threads: `-t 4` (match your CPU cores)
- Close other apps before running

### Speed Expectations
- **CPU only:** 5-15 tokens/sec
- **With GPU:** 20-50+ tokens/sec
- Gemma 4 E2B is optimized for speed

### Batch Processing
For faster responses, increase batch size if RAM allows:
```
llama-server.exe -m model.gguf -b 1024 -ub 256
```

---

## 8. Security Notes

- Server binds to `127.0.0.1` by default (localhost only)
- No authentication by default (add your own proxy if exposing)
- API key is not validated (set any value in clients)
- For network access, use `--host 0.0.0.0` (caution: exposes to LAN)
