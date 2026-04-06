# OpenCode Model Configuration Fix

## Problem

The gemma-4 model was not appearing in the opencode model list even though it was running as a local llama.cpp server on port 8080.

## Root Cause

The opencode configuration file (`C:\Users\admin\.config\opencode\opencode.json`) did not have an entry for the gemma-4 model running on llama.cpp server.

## Solution

Added a new provider configuration for `gemma-4` in `opencode.json`:

```json
"gemma-4": {
  "models": {
    "google_gemma-4-E2B-it-Q4_K_M": {
      "_launch": false,
      "google_gemma-4-E2B-it-Q4_K_M": { "name": "google_gemma-4-E2B-it-Q4_K_M" }
    }
  },
  "name": "Gemma 4 (llama.cpp)",
  "npm": "@ai-sdk/openai-compatible",
  "options": {
    "baseURL": "http://127.0.0.1:8080/v1"
  }
}
```

## To Use

1. Start the llama.cpp server (if not already running):
   ```
   llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
   ```

2. Restart opencode or reload configuration

3. Select the `google_gemma-4-E2B-it-Q4_K_M` model from the model list

---

Fixed by: **minimax m2.5 free** (opencode)
