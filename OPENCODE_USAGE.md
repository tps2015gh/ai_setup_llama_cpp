# How to Call Local AI from OpenCode

> **Guide for: tps2015gh (Thitipong Samranvanich)**

---

## Overview

OpenCode can use your local **llama.cpp + Gemma 4** as its AI backend instead of cloud APIs. This means:
- **No API keys needed**
- **No internet required**
- **Full privacy** — code never leaves your machine
- **No usage limits** — run as much as you want

---

## Step 1: Start llama.cpp Server

Open PowerShell and run:

```powershell
cd C:\dev\ai_setup_llama_cpp

llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```

Wait until you see:
```
llama server listening at http://127.0.0.1:8080
```

**Keep this window open** — the server must stay running while using OpenCode.

---

## Step 2: Configure OpenCode

### Method A: Environment Variables (Temporary)

In PowerShell, before launching OpenCode:

```powershell
$env:OPENAI_BASE_URL = "http://127.0.0.1:8080/v1"
$env:OPENAI_API_KEY = "local"

# Now start OpenCode
opencode
```

### Method B: Project Config File (Recommended)

Create `opencode.json` in your project folder:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local-gemma4": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Gemma 4 Local",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1"
      },
      "models": {
        "gemma4": {
          "name": "Gemma 4 E2B Q4_K_M (local)"
        }
      }
    }
  },
  "model": "local-gemma4/gemma4"
}
```

Then just run `opencode` — it will auto-connect to your local server.

### Method C: OpenCode Settings (If Available)

If OpenCode has a settings UI:

1. Open **Settings** → **AI Provider**
2. Select **OpenAI Compatible** or **Custom**
3. Set **Base URL:** `http://127.0.0.1:8080/v1`
4. Set **API Key:** `local` (any value works)
5. Set **Model:** `gemma4`
6. Save and restart OpenCode

---

## Step 3: Verify Connection

In OpenCode, ask a simple question:

```
What is 2+2?
```

If you get a response, the connection is working.

You can also check the server window — you should see incoming requests:

```
POST /v1/chat/completions 200
```

---

## Step 4: Use OpenCode with Local AI

### Chat with AI
Just type normally in OpenCode. All requests go to your local Gemma 4.

### Code Review
```
Review this code for bugs:
[paste code]
```

### Fix Errors
```
Fix this error:
[paste error message]
```

### Explain Code
```
Explain what this function does:
[paste function]
```

### Generate Code
```
Write a Python function that reads a CSV file and returns a list of dictionaries.
```

---

## Step 5: Server Options

### Default (8GB RAM)
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```

### Low RAM (if running out of memory)
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 2048 -t 4 -b 512 --port 8080
```

### Higher Context (if you have 16GB+ RAM)
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 8192 --port 8080
```

### Parameter Reference

| Flag | Description | Recommended |
|------|-------------|-------------|
| `-m` | Model path | `llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf` |
| `-c` | Context size | `2048` (8GB) / `4096` (16GB) |
| `-t` | CPU threads | `4` (match your cores) |
| `-b` | Batch size | `512` (8GB) / `1024` (16GB) |
| `--port` | Server port | `8080` |
| `--host` | Bind address | `127.0.0.1` (localhost only) |

---

## Troubleshooting

### OpenCode Can't Connect

**Check server is running:**
```powershell
curl http://127.0.0.1:8080/health
```
Should return: `{"status":"ok"}`

**If not running:** Start the server (Step 1)

### "Model Not Found" Error

OpenCode may send a model name that doesn't match. The server accepts any model name since it's local, but if there's an issue:

1. Check OpenCode config — set model to `gemma4`
2. Or start server with `--alias gemma4`

### Slow Responses

Gemma 4 E2B on CPU runs at ~10 tokens/sec. This is normal.

**To speed up:**
- Close other applications
- Reduce context: `-c 2048`
- Set threads: `-t 4`

### Server Crashes

**Out of memory:** Reduce `-c` to 1024 or 2048

**Restart command:**
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 2048 --port 8080
```

---

## Quick Start Script

Create `start-opencode.ps1` in your project folder:

```powershell
# Start llama.cpp server in background
Start-Process -FilePath "llama-cpp\llama-server.exe" -ArgumentList "-m", "llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf", "-c", "4096", "--port", "8080" -WindowStyle Normal

# Wait for server to start
Write-Host "Waiting for llama.cpp server..."
Start-Sleep -Seconds 10

# Set environment variables
$env:OPENAI_BASE_URL = "http://127.0.0.1:8080/v1"
$env:OPENAI_API_KEY = "local"

Write-Host "Server ready. Starting OpenCode..."

# Start OpenCode
opencode
```

Run with:
```powershell
.\start-opencode.ps1
```

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  1. Start llama-server                                      │
│     llama-cpp\llama-server.exe -m model.gguf -c 4096        │
│                                                             │
│  2. Set environment (or use config file)                    │
│     $env:OPENAI_BASE_URL = "http://127.0.0.1:8080/v1"       │
│     $env:OPENAI_API_KEY = "local"                           │
│                                                             │
│  3. Start OpenCode                                          │
│     opencode                                                │
│                                                             │
│  4. Use normally — all AI runs locally!                     │
│                                                             │
│  5. When done — Ctrl+C in server window to stop             │
└─────────────────────────────────────────────────────────────┘
```

---

## What OpenCode Can Do with Local AI

| Task | Example Prompt |
|------|----------------|
| **Code generation** | "Write a Python function to sort a list" |
| **Bug fixing** | "Fix this error: [paste error]" |
| **Code review** | "Review this code: [paste code]" |
| **Explanation** | "Explain this function: [paste code]" |
| **Refactoring** | "Refactor this to be cleaner: [paste code]" |
| **Documentation** | "Write docstring for this: [paste code]" |
| **Testing** | "Write unit tests for: [paste code]" |
| **Architecture** | "How should I structure a REST API in Go?" |

---

## Notes

- **Gemma 4 E2B** is a 2B parameter model — good for simple tasks, may struggle with complex reasoning
- **Context limit:** 4096 tokens on 8GB RAM (~3000 words)
- **Speed:** ~10 tokens/sec on CPU
- **Memory:** ~4.8GB RAM while server is running
- **No authentication** needed — server is localhost only by default
