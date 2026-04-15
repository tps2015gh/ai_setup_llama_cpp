# llama.cpp + Gemma 4 Local AI Setup

> **Complete local AI solution for low-RAM Windows machines (8GB)**

---

## Project Overview

This project sets up **llama.cpp** with **Gemma 4 E2B** as a fully local AI inference stack on Windows — no WSL, no cloud, no API keys. Everything runs on your machine.

### Why This Approach?

| Aspect | Ollama | llama.cpp (this project) |
|--------|--------|--------------------------|
| **WSL Required** | Yes | No (native Windows) |
| **Memory Overhead** | 200-500MB daemon | Minimal |
| **Control** | Abstracted | Full control |
| **Disk Usage** | Heavy | Lightweight |
| **Speed on 8GB** | Slower | Optimized |

---

## Team

### 👤 Supervisor: tps2015gh (Thitipong Samranvanich)
- Define direction and requirements
- Make decisions on model selection
- Guide the setup process
- Review and approve each phase

### 🤖 AI Agent (Qwen / KIMI)
- Execute setup tasks autonomously
- Research and select optimal configurations
- Create scripts, documentation, and skills
- Troubleshoot issues (like architecture mismatches)
- Maintain project documentation

### 🧠 AI Models (The Team)

| Model | Role | Status |
|-------|------|--------|
| **Gemma 4 E2B Q4_K_M** | Primary local coding assistant | ✅ Active (llama.cpp b8676) |
| **MiniMax M2.5 Free** | Cloud fallback (OpenCode Zen) | ✅ Available |
| **Qwen3 1.7B** | Local lightweight model (Ollama) | ✅ Available |

### 💻 Model: Gemma 4 E2B Q4_K_M
- **Type:** Google's Gemma 4, Expert 2B variant
- **Quantization:** Q4_K_M (4-bit, medium quality)
- **Size:** 3.46GB
- **Architecture:** 35 layers, 1536 embedding dim, sliding window attention
- **Context:** 131,072 tokens (theoretical), 2,048-4,096 (practical on 8GB)
- **Speed:** ~10 tokens/sec on CPU (8GB RAM)
- **Memory:** ~4.8GB RAM usage
- **Integration:** OpenCode via llama.cpp server (port 8080)

---

## Quick Start

### Automated Setup (Recommended)
```powershell
python setup.py
# Select option 6 (Install all)
```

### Manual Setup
```powershell
# 1. Install llama.cpp
python setup.py  # Option 1

# 2. Download Gemma 4
python setup.py  # Option 2

# 3. Test
python setup.py  # Option 4
```

### Run Gemma 4
```powershell
# Chat mode
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 2048

# One-time response
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -p "Hello" -n 128

# Start API server (for OpenCode, Continue, etc.)
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 4096 --port 8080
```

---

## Project Structure

```
ai_setup_llama_cpp/
├── setup.py                    # Interactive setup menu (Python)
├── HOW_TO_RUN.md               # Quick reference guide
├── AGENTIC_USAGE.md            # Integration with OpenCode, Qwen, etc.
├── AI.md                       # Recovery checkpoint (RCP)
├── .gitignore                  # Git ignore rules
├── prompt01.txt                # Original requirements
├── prompt02.txt                # Original requirements
├── what_i_doing_and_have_done.log  # Activity log
│
├── .qwen/
│   ├── skills/
│   │   ├── llama-cpp-setup/    # Skill: llama.cpp installation
│   │   └── gemma4-test/        # Skill: Model testing
│   └── agents/                 # Virtual agent configs
│
├── REPORTS/
│   ├── 01-cleanup-ollama.md    # Phase 1 report
│   ├── 02-install-llama-cpp.md # Phase 2 report
│   └── 03-setup-gemma4.md      # Phase 3 report
│
└── llama-cpp/                  # llama.cpp binaries (gitignored)
    ├── llama-cli.exe
    ├── llama-server.exe
    └── models/
        └── google_gemma-4-E2B-it-Q4_K_M.gguf  # Model (gitignored)
```

---

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | This file — project overview and guide |
| `WORKFLOW.md` | **How to use each model effectively** |
| `HOW_TO_RUN.md` | Quick start, commands, parameters |
| `HOW_TO_FIX_CODE.md` | **How to use local AI to fix your program** |
| `OPENCODE_USAGE.md` | **How to call local AI from OpenCode** |
| `AGENTIC_USAGE.md` | OpenCode, Qwen, Continue, API integration |
| `AI.md` | Recovery checkpoint for AI context loss |
| `setup.py` | Interactive setup menu |
| `REPORTS/` | Detailed phase-by-phase documentation |
| `what_i_doing_and_have_done.log` | Complete activity timeline |

---

## AI Coder (Advanced Agentic Code Editor)

Located in `_test_codegen/` - A menu-driven AI code editor using local Gemma 4.

### Quick Start
```powershell
cd C:\dev\ai_setup_llama_cpp\_test_codegen
python ai_coder_modular\ai_coder.py
```

### Main Menu
```
Server:
  1. Start Server          ← Load Gemma 4 model & start API
  2. Stop Server           ← Free up RAM
  3. Check Status          ← Verify it's running
  4. Set Source Directory  ← Point to your project

Agents (YOLO = auto-save):
  5. Chat Agent            ← Interactive chat with AI
  6. Edit Agent            ← Single file edit
  7. Multi-File Agent      ← Create multiple files at once
  8. Autonomous Agent     ← Loop until task complete (batch create)

Settings:
  9. Toggle YOLO/Manual    ← Auto-save or confirm each file
  0. Exit
```

### Features
- **Session Persistence** - Resume after crash/restart
- **Multi-level folders** - Creates nested directories like `app/Views/users/`
- **Retry logic** - 3 retries on timeout (common with CPU inference)
- **YOLO Mode** - Auto-save without asking (default)
- **Multi-file creation** - Generate entire project structure

### Documentation
See [`_test_codegen/README_AI_CODER.md`](_test_codegen/README_AI_CODER.md) and [`_test_codegen/AI_CODER_USAGE.md`](_test_codegen/AI_CODER_USAGE.md)

### All _test_codegen Documentation Files

| File | Purpose |
|------|---------|
| [`_test_codegen/README_AI_CODER.md`](_test_codegen/README_AI_CODER.md) | Main documentation & quick start |
| [`_test_codegen/AI_CODER_USAGE.md`](_test_codegen/AI_CODER_USAGE.md) | Complete usage guide (detailed) |
| [`_test_codegen/AI_CODER_ARCHITECTURE.md`](_test_codegen/AI_CODER_ARCHITECTURE.md) | System architecture & design |
| [`_test_codegen/CODE_GENERATION_DOCS.md`](_test_codegen/CODE_GENERATION_DOCS.md) | Code generation features |
| [`_test_codegen/SERVER_STATUS_DOCS.md`](_test_codegen/SERVER_STATUS_DOCS.md) | Server status & monitoring |
| [`_test_codegen/MULTILANG_SUMMARY.md`](_test_codegen/MULTILANG_SUMMARY.md) | Multi-language support |
| [`_test_codegen/plan.md`](_test_codegen/plan.md) | Project plan & roadmap |

---

## System Requirements

- **OS:** Windows 10/11 (x64)
- **RAM:** 8GB minimum
- **Disk:** 5GB free (3.5GB for model + 100MB for binaries)
- **Python:** 3.10+ (for setup.py)
- **No GPU required** (CPU inference)

---

## AI Agent's Opinion on This Project

### What Works Well
1. **Local-first approach** — No dependency on cloud APIs, full privacy
2. **Low-RAM optimization** — Gemma 4 E2B at Q4_K_M fits 8GB comfortably
3. **Automated setup** — `setup.py` makes it reproducible for others
4. **Modular design** — Each component (llama.cpp, model, skills) is independent
5. **Documentation-first** — Every step logged and reported

### Challenges Encountered
1. **Version compatibility** — Initial b4773 didn't support Gemma 4 architecture. Had to upgrade to b8676.
2. **Download reliability** — HuggingFace direct downloads sometimes return HTML instead of binary. Required finding correct URLs via GitHub API.
3. **Disk space constraints** — 8GB RAM machine had only ~15GB free disk. Every MB counted.

### Recommendations
1. **For better speed:** Consider Vulkan build (`llama-b8676-bin-win-vulkan-x64.zip`) if you have AMD GPU
2. **For better quality:** If you upgrade to 16GB RAM, use Gemma 4 E4B Q4_K_M (~6GB)
3. **For production:** Add authentication to llama-server if exposing to network
4. **For development:** Keep this repo lightweight — binaries and models are gitignored, downloaded by `setup.py`

### Future Improvements
- [ ] Add GPU support (CUDA/Vulkan) detection in setup.py
- [ ] Add model switching (multiple models)
- [ ] Add benchmark mode with performance tracking
- [ ] Add Docker support for containerized deployment

---

## License

This setup project: MIT
Gemma 4 model: Apache 2.0 (see https://ai.google.dev/gemma/docs)
llama.cpp: MIT (https://github.com/ggml-org/llama.cpp)

---

## Credits

- **llama.cpp:** Georgi Gerganov & contributors
- **Gemma 4:** Google DeepMind
- **Quantized model:** bartowski (HuggingFace)
- **Setup automation:** AI Agent (Qwen/KIMI) under human supervision
