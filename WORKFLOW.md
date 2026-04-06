# AI Workflow Guide

> **How to use each model effectively with OpenCode**

---

## Team Members

| Member | Role | Access |
|--------|------|--------|
| **tps2015gh (Thitipong Samranvanich)** | Supervisor — sets direction, reviews, approves | Full control |
| **Qwen / KIMI** | AI Agent — research, setup, documentation, troubleshooting | File system, git, web |
| **Gemma 4 E2B Local** | Code reviewer — reads, explains, finds bugs | Read-only (no file creation) |
| **MiniMax M2.5 Free** | Code creator — writes files, creates features | Full agent (read + write) |
| **Qwen3 1.7B Local** | Quick assistant — simple questions, local fallback | Read-only |

---

## Model Capabilities

### Gemma 4 E2B (llama.cpp Local)
| Can Do | Can't Do |
|--------|----------|
| ✅ Read and analyze code | ❌ Create files on disk |
| ✅ Trace controller → view flow | ❌ Write code from scratch |
| ✅ Explain CodeIgniter architecture | ❌ Agent file operations |
| ✅ Find bugs in existing code | ❌ Execute shell commands |
| ✅ Answer questions about codebase | ❌ Generate complete programs |

**Best for:** Code review, debugging, understanding existing code

### MiniMax M2.5 Free (Cloud)
| Can Do | Can't Do |
|--------|----------|
| ✅ Create new files | ❌ Runs offline |
| ✅ Write complete programs | ❌ Uses API quota |
| ✅ Full agent mode (read + write) | |
| ✅ Execute shell commands | |
| ✅ Refactor and save | |

**Best for:** Creating new code, file operations, feature development

### Qwen3 1.7B (Ollama Local)
| Can Do | Can't Do |
|--------|----------|
| ✅ Quick questions | ❌ Complex reasoning |
| ✅ Simple explanations | ❌ Large codebases |
| ✅ Local, no internet | ❌ File creation |

**Best for:** Fast local answers when cloud is unavailable

---

## Workflow: CodeIgniter 3 Example

### Scenario: Understand existing project

```
Step 1: Switch to Gemma 4 Local
Step 2: In OpenCode shell, read the code:
  $ dir application/controllers/
  $ cat application/controllers/Auth.php
  $ cat application/views/login_view.php
  $ cat application/models/User_model.php

Step 3: Ask Gemma 4:
  "Which controller calls which view?"
  "Find bugs in Auth.php"
  "Explain the login flow"

Step 4: Gemma 4 reads and explains — no files created
```

### Scenario: Create new feature

```
Step 1: Switch to MiniMax M2.5 Free (cloud)
Step 2: Ask:
  "Create a new controller for user profile"
  "Create a view for dashboard"

Step 3: MiniMax writes files to disk
Step 4: Switch to Gemma 4 Local to review:
  "Review the new Profile controller for bugs"
```

### Scenario: Fix a bug

```
Step 1: Switch to Gemma 4 Local
Step 2: Read the buggy file:
  $ cat application/controllers/Report.php
Step 3: Ask:
  "Find the bug in this controller"
Step 4: Gemma 4 explains the issue
Step 5: Switch to MiniMax M2.5 Free
Step 6: Ask:
  "Fix the bug in Report.php and save"
Step 7: MiniMax writes the fix to disk
```

---

## Quick Reference

| Task | Use This Model | Command |
|------|----------------|---------|
| Read and explain CI3 code | **Gemma 4 Local** | `/model local-gemma4/google_gemma-4-E2B-it-Q4_K_M.gguf` |
| Trace controller → view | **Gemma 4 Local** | Same |
| Find bugs | **Gemma 4 Local** | Same |
| Create new controller | **MiniMax M2.5 Free** | `/model` → select MiniMax |
| Create new view | **MiniMax M2.5 Free** | Same |
| Write and save files | **MiniMax M2.5 Free** | Same |
| Quick local question | **Qwen3 1.7B** | `/model` → select Qwen3 |

---

## Switching Models in OpenCode

```
/model
→ Select from the list:
  - Gemma 4 (llama.cpp) — local, read-only
  - MiniMax M2.5 Free — cloud, full agent
  - Qwen3 1.7B — local, lightweight
```

---

## Server Requirements

### Gemma 4 Local
```powershell
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```
- RAM: ~4.8GB
- Speed: ~10 tokens/sec
- Offline: Yes

### Qwen3 1.7B (Ollama)
```powershell
ollama run qwen3:1.7b
```
- RAM: ~1.5GB
- Speed: ~20 tokens/sec
- Offline: Yes

### MiniMax M2.5 Free
- No server needed — cloud API
- Requires internet
- Free tier available

---

## Notes

- **Gemma 4 E2B** is a 2B parameter model — good for reading/understanding, too small for code generation
- **MiniMax M2.5 Free** is a cloud model — capable of full agent workflows
- **Qwen3 1.7B** is a lightweight local model — fast but limited reasoning
- Always use the right tool for the task: **read = local**, **write = cloud**
