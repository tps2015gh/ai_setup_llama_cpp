# How to Use Local AI (Gemma 4) to Fix Your Program

> **Guide for: tps2015gh (Thitipong Samranvanich)**

---

## Overview

This guide shows you how to use your local **llama.cpp + Gemma 4** AI to read, understand, and fix your program code — all offline, no API keys needed.

---

## Step 1: Start the AI Server

Open PowerShell and run:

```powershell
cd C:\dev\ai_setup_llama_cpp

llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```

**What this does:**
- Loads Gemma 4 model into memory (~30 seconds)
- Starts HTTP server on `http://127.0.0.1:8080`
- Provides OpenAI-compatible API for any tool to connect

**Keep this window open** — the server must stay running while you work.

---

## Step 2: Prepare Your Program Files

Before asking AI to fix code, gather these:

### What to Collect
1. **Error messages** — Copy the exact error output
2. **File paths** — Which files have the problem
3. **Relevant code** — The specific functions/lines
4. **Expected behavior** — What should happen vs what happens

### Example Preparation
```
Problem: Program crashes on login
Files: src/auth.py, src/database.py
Error: "ConnectionError: Cannot connect to database"
Expected: User should be able to login successfully
```

---

## Step 3: Ask AI to Fix Code

### Method A: Direct Chat (Simple)

```powershell
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 4096 -p "You are an expert programmer. I will show you my code and error messages. Help me fix them."
```

Then paste your code and error:

```
> Here is my code:
[Paste code here]

The error is:
[Paste error here]

Please fix it.
```

### Method B: Via API (For Tools/IDEs)

If using OpenCode, Continue, or other IDE tools:

1. **Start server** (Step 1)
2. **Configure your tool** to use `http://127.0.0.1:8080/v1`
3. **Open your code** in the IDE
4. **Select the problematic code** and ask the AI to fix it

### Method C: File-Based Analysis (Large Programs)

For programs with many files:

```powershell
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 4096 -p "You are a senior code reviewer. I will show you my project structure and files one by one. Analyze the architecture, find bugs, and suggest fixes."
```

Then provide:

```
> My project structure:
[Paste output of: tree /F or dir /S]

Here is the main file (main.py):
[Paste code]

Here is the config file:
[Paste code]

The problem is: [describe]
```

---

## Step 4: Effective Prompt Templates

### Fix a Bug
```
I have a bug in my [language] program.

File: [filename]
Line: [line number]

Code:
```[language]
[paste code]
```

Error message:
[paste error]

What I expected: [describe]
What actually happens: [describe]

Please:
1. Explain the bug
2. Show the fixed code
3. Explain why the fix works
```

### Review Code
```
Please review this [language] code for:
- Bugs and errors
- Performance issues
- Security problems
- Code style

Code:
```[language]
[paste code]
```

List all issues found with line numbers and suggested fixes.
```

### Refactor
```
Refactor this code to be:
- More readable
- More efficient
- Follow best practices

Current code:
```[language]
[paste code]
```

Show the improved version with explanations.
```

### Add Feature
```
I need to add [feature] to my existing code.

Current code:
```[language]
[paste code]
```

Requirements:
- [requirement 1]
- [requirement 2]

Show me the updated code with the new feature.
```

---

## Step 5: Working with Large Programs

Gemma 4 E2B has a **context limit**. On 8GB RAM, use `-c 2048` to `-c 4096`.

### Strategy for Large Codebases

**Don't paste everything at once.** Instead:

1. **Start with structure**
   ```
   Here is my project structure:
   [tree output]
   
   The main entry point is: main.py
   The config is: config.json
   The problem is in: auth module
   ```

2. **Show relevant files one at a time**
   ```
   Here is main.py:
   [code]
   
   Now here is auth.py (the problem file):
   [code]
   ```

3. **Focus on the problem area**
   ```
   The error happens in the login() function on line 45.
   Here is just that function:
   [code]
   ```

---

## Step 6: Save AI Responses

When AI gives you a fix:

1. **Copy the fixed code** into your editor
2. **Test it** before committing
3. **Save the conversation** for reference:
   ```powershell
   # In chat mode, copy the output to a file
   # Or use the API and save the JSON response
   ```

---

## Step 7: Integrate with Your IDE

### VS Code + Continue Extension

1. Install **Continue** extension
2. Add to `~/.continue/config.json`:
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
3. Select code → Right-click → Continue: Edit

### OpenCode

1. Start llama.cpp server (Step 1)
2. Set environment:
   ```powershell
   $env:OPENAI_BASE_URL = "http://127.0.0.1:8080/v1"
   $env:OPENAI_API_KEY = "local"
   ```
3. Run OpenCode — it will use your local AI

---

## Performance Tips

| Setting | Value | Why |
|---------|-------|-----|
| `-c` | 2048-4096 | Context size (lower = less RAM) |
| `-t` | 4 | Match your CPU core count |
| `-b` | 512 | Batch size (lower = less RAM) |

### Low RAM (8GB) Server Command
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 2048 -t 4 -b 512 --port 8080
```

---

## Common Issues

### AI Gives Incomplete Answers
- **Cause:** Context too small
- **Fix:** Reduce code per message, use `-c 4096`

### AI Doesn't Understand Your Code
- **Cause:** Gemma 4 E2B is a small model
- **Fix:** Be specific about language, framework, and error

### Server Crashes / Out of Memory
- **Cause:** Context too large
- **Fix:** Reduce `-c` to 1024, close other apps

### Slow Response (1-2 tokens/sec)
- **Cause:** CPU-only inference on low-end CPU
- **Fix:** Reduce `-t` to match physical cores, not logical

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  START SERVER                                           │
│  llama-cpp\llama-server.exe -m model.gguf -c 4096       │
│                                                         │
│  CHAT MODE                                              │
│  llama-cpp\llama-cli.exe -m model.gguf -cnv -c 4096     │
│                                                         │
│  ONE-TIME FIX                                           │
│  llama-cli.exe -m model.gguf -p "Fix this: [code]" -n 200│
│                                                         │
│  API ENDPOINT                                           │
│  http://127.0.0.1:8080/v1/chat/completions              │
│                                                         │
│  STOP SERVER                                            │
│  Ctrl+C in server window                                │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow Summary

```
1. Start llama-server  →  Wait for model to load
2. Open your IDE       →  OpenCode, VS Code, etc.
3. Find the bug        →  Copy error + code
4. Ask AI              →  Paste prompt template
5. Review fix          →  Understand the change
6. Test                →  Run your program
7. Commit              →  Save working fix
```
