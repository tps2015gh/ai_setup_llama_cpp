# AI Coder - Lightweight Agentic Code Editor

> **Your Offline AI Programming Assistant for PHP/CodeIgniter + MySQL Development**

---

## What is AI Coder?

A **menu-driven Python tool** that uses your local **llama.cpp + Gemma 4** model to help you:
- 🔍 **Read & analyze** code
- 🐛 **Find & fix** bugs automatically
- 📝 **Review code** quality (security, performance, style)
- 💡 **Explain** what code does
- ✍️ **Write new** Controllers, Models, Views, Libraries
- ⚙️ **Batch process** files (24/7 automation mode)
- 🗄️ **Analyze MySQL** database schemas

**100% Offline** - No cloud APIs, no internet required!

---

## Quick Start (3 Steps)

### Option 1: Double-click launcher (Easiest)
```
Just run: run_ai_coder.bat
```

### Option 2: Manual start
```powershell
cd C:\dev\ai_setup_llama_cpp\_test_codegen
python ai_coder.py
```

### Then use the menu:
1. **Menu 1** - Start AI Server (loads Gemma 4)
2. **Menu 4** - Set your source code directory
3. **Menu 5-11** - Use AI tools!

---

## Main Menu

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
  8. Autonomous Agent     ← Loop until task complete

Settings:
  9. Toggle YOLO/Manual    ← Auto-save or confirm each file
  0. Exit
```

### New Features (v2.0)

- **Session Persistence** - If crash/restart, ask to resume from where left off
- **Multi-level folders** - Creates nested directories like `app/Views/users/`
- **Better path display** - Shows full relative paths like `app/Views/users/index.php`
- **Increased timeout** - 300s for longer operations

---

## Features

### 🔧 Fix Files with AI
Select a file, describe the problem, AI analyzes and provides fixes with explanations.

### 📊 Code Review
Comprehensive review covering:
- ✓ Bugs and errors
- ✓ Security vulnerabilities (SQL injection, XSS, CSRF)
- ✓ Performance issues
- ✓ Code style and best practices
- ✓ Database query optimization

### 💬 Interactive Chat
Free-form conversation with AI about your code. Reference files with `@filename.php`.

### ⚡ Batch Mode (24/7)
Process multiple files automatically:
- Review all files for code quality
- Check for security issues
- Generate documentation
- Find and fix common bugs
- Custom prompts

Perfect for **overnight automation**!

### 🗄️ Database Analysis
Connect to MySQL and get:
- Schema design review
- Index recommendations
- Performance optimizations
- Potential issues

---

## Files Created

| File | Purpose |
|------|---------|
| `ai_coder.py` | Main program (menu-driven) |
| `ai_coder_config.json` | Configuration settings |
| `run_ai_coder.bat` | Quick launcher |
| `AI_CODER_USAGE.md` | **Complete documentation** |
| `test_ai_coder.py` | Test suite |

---

## Example Usage

### Fix a Bug
```
Select [0-11]: 6

Available files:
  1. app\Controllers\UserController.php
  2. app\Models\UserModel.php
  
Select file number: 1

Describe the problem: Getting "Undefined variable $user" error on line 45

[AI] Analyzing...

I found the issue! On line 45, you're accessing $user but it's only 
set when login succeeds. When auth fails, $user is undefined.

**Fixed code:**
[AI provides corrected code with explanation]

Apply AI suggestions? (y/n): y
[✓] AI fix saved to: UserController.php.ai_fixed
```

### Batch Security Review (Overnight)
```
Select [0-11]: 10

Found 127 files

Select task [1-5]: 2  (Check for security issues)

Processing up to 50 files...

[1/50] app\Controllers\UserController.php
  [✓] Done - Results saved

[2/50] app\Models\UserModel.php
  [✓] Done - Results saved
  
... (continues automatically)

Batch Processing Complete
Processed: 50
Results saved to .batch_result files
```

---

## Configuration

Edit `ai_coder_config.json`:

```json
{
  "llama_cpp": {
    "server_port": 8080,
    "context_size": 4096,      // Lower = less RAM
    "threads": 4                // CPU threads
  },
  "source_code": {
    "default_directory": "",    // Your project path
    "file_extensions": [".php", ".js", ".html", ".css", ".sql"]
  },
  "batch_mode": {
    "delay_between_files": 5,   // Seconds between files
    "max_files_per_run": 50,    // Limit per batch
    "create_backup": true       // Auto-backup
  }
}
```

---

## Requirements

- **Python:** 3.7+ (tested with 3.7.7)
- **llama.cpp:** Installed at `C:\dev\ai_setup_llama_cpp\llama-cpp\`
- **Model:** Gemma 4 E2B Q4_K_M
- **RAM:** 8GB minimum
- **Optional:** XAMPP MySQL (for database analysis)

### Python Packages
```bash
pip install colorama requests
```

---

## Performance Tips

| For 8GB RAM | For 16GB RAM |
|-------------|--------------|
| context_size: 2048-4096 | context_size: 8192 |
| threads: 4 | threads: 8 |
| Close other apps | Normal usage |

---

## Documentation

📖 **Full guide:** See [`AI_CODER_USAGE.md`](AI_CODER_USAGE.md)

Includes:
- Detailed feature explanations
- PHP/CodeIgniter examples
- Troubleshooting guide
- Advanced usage
- 24/7 automation guide

---

## Test Suite

Run tests to verify installation:

```powershell
python test_ai_coder.py
```

Expected output:
```
✓ All tests passed! AI Coder is ready to use.
```

---

## Comparison with Other Tools

| Feature | AI Coder | OpenCode | Gemini CLI |
|---------|----------|----------|------------|
| **Offline** | ✓ 100% | Partial | ✗ No |
| **Cost** | Free | Free/Paid | Paid |
| **Privacy** | All local | Varies | Cloud |
| **Batch Mode** | ✓ Yes | Limited | ✗ No |
| **24/7 Work** | ✓ Yes | Partial | ✗ No |
| **DB Analysis** | ✓ Yes | ✗ No | ✗ No |

---

## Workflow

```
1. Start AI Coder        →  python ai_coder.py
2. Start server          →  Menu 1 (wait for ready)
3. Set source directory  →  Menu 4 (point to project)
4. Choose AI tool        →  Menu 5-11 (what you need)
5. Review AI output      →  Check suggestions
6. Apply fixes           →  Manual review & test
7. Commit working code   →  Save to git
8. Repeat                →  Continuous improvement
```

---

## Troubleshooting

**Server won't start?**
- Check paths in `ai_coder_config.json`
- Verify llama.cpp is installed

**AI gives incomplete answers?**
- Increase `context_size` in config
- Reduce code per request

**Out of memory?**
- Reduce `context_size` to 2048
- Close other applications

**See `AI_CODER_USAGE.md` for full troubleshooting guide**

---

## Support

For issues:
1. Check config file paths are correct
2. Verify llama.cpp server is installed
3. Ensure Gemma 4 model is downloaded
4. Check MySQL is running (for DB features)

---

## License

This tool: MIT
Gemma 4 model: Apache 2.0
llama.cpp: MIT

---

## About This Project

This AI Coder tool was created by AI agents:
- **80% Qwen** - Main architecture, agents, file management, session persistence
- **20% Minimax** - Code improvements, bug fixes, documentation

Both agents worked under human supervision (tps2015gh) to build this modular agentic code editor.

### What the AI Agents Created
- Modular agent architecture (ChatAgent, EditAgent, MultiFileAgent, AutonomousAgent)
- File manager with multi-level directory creation
- Session persistence for crash recovery
- Retry logic for timeout handling
- Menu-driven interface with YOLO mode

---

## My Opinion (as Minimax)

As an AI agent who contributed 20% to this project, here's my honest assessment:

### What Works Well
1. **Modular design** - Agents are independent and easy to extend
2. **Session persistence** - The `ai_session.json` feature is crucial for long-running autonomous tasks
3. **YOLO mode** - Auto-save speeds up workflow significantly
4. **Retry logic** - 3 retries handle most timeout issues with CPU inference
5. **Multi-level folders** - Fixed the nested directory creation issue

### Areas for Improvement
1. **Context handling** - When resuming session, should also load what files were already created to avoid duplicates
2. **Error recovery** - Could add more granular save points (every file instead of every 10)
3. **Token management** - No tracking of total tokens used per session
4. **Logging** - Could add more detailed logs for debugging
5. **Tests** - Need more unit tests for edge cases

### Technical Notes
- The autonomous agent is powerful but can be slow on 8GB RAM
- Gemma 4 E2B is good but sometimes struggles with complex multi-file generation
- The retry logic works but adds time to already slow operations

### Verdict
A solid foundation for local AI-assisted coding. With more refinements, it could become a truly useful tool for developers who need offline AI assistance.

---

**Enjoy coding with AI assistance! 🚀**
