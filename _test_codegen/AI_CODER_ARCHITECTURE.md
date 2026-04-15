# AI Coder Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         AI Coder (ai_coder.py)                      │    │
│  │         Menu-Driven Python Tool                     │    │
│  │                                                      │    │
│  │  ┌───────────────────────────────────────────┐     │    │
│  │  │  Main Menu System                         │     │    │
│  │  │  1-3:  Server Management                  │     │    │
│  │  │  4:    Source Directory                   │     │    │
│  │  │  5-9:  AI Tools                           │     │    │
│  │  │  10:   Batch Processing                   │     │    │
│  │  │  11:   Database Analysis                  │     │    │
│  │  └───────────────────────────────────────────┘     │    │
│  │                                                      │    │
│  │  ┌───────────────────────────────────────────┐     │    │
│  │  │  Features:                                │     │    │
│  │  │  • File I/O (read/write PHP, JS, etc.)   │     │    │
│  │  │  • Server management (subprocess)         │     │    │
│  │  │  • AI communication (HTTP requests)       │     │    │
│  │  │  • Batch automation                       │     │    │
│  │  │  • Database queries (MySQL)               │     │    │
│  │  └───────────────────────────────────────────┘     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP REST API
                            │ (requests library)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI INFERENCE LAYER                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     llama-server.exe (llama.cpp)                    │    │
│  │     • Loads Gemma 4 model                           │    │
│  │     • Provides OpenAI-compatible API                │    │
│  │     • Runs on http://127.0.0.1:8080                 │    │
│  │     • CPU inference (optimized for 8GB RAM)         │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            │ Model loading                   │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     Gemma 4 E2B Q4_K_M Model                        │    │
│  │     • 3.46GB GGUF format                            │    │
│  │     • 4-bit quantized                               │    │
│  │     • 131K context (use 2-4K on 8GB)               │    │
│  │     • ~10 tokens/sec on CPU                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ File operations
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   YOUR SOURCE CODE                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  CodeIgniter Project                                │    │
│  │  • Controllers (.php)                               │    │
│  │  • Models (.php)                                    │    │
│  │  • Views (.php, .html)                              │    │
│  │  • Libraries (.php)                                 │    │
│  │  • Config (.json, .xml)                             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Database connection
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE                                │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     MySQL (XAMPP)                                   │    │
│  │     • Schema analysis                               │    │
│  │     • Index recommendations                         │    │
│  │     • Performance optimization                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Server Management Flow
```
User selects Menu 1
    ↓
AICoder.start_server()
    ↓
Subprocess: llama-server.exe -m model.gguf -c 4096 --port 8080
    ↓
Wait loop (test /v1/models endpoint)
    ↓
Server ready ✓
```

### 2. Fix File Flow
```
User selects Menu 6
    ↓
List source files → User selects file
    ↓
Read file content
    ↓
User describes problem
    ↓
Build prompt (fix_code_prompt template)
    ↓
POST to /v1/chat/completions
    ↓
AI analyzes code
    ↓
Returns fix suggestions
    ↓
Save to .ai_fixed file
    ↓
User reviews & applies
```

### 3. Batch Processing Flow
```
User selects Menu 10
    ↓
Choose task (1-5)
    ↓
Loop through files (up to max_files_per_run)
    ├─ Read file
    ├─ Build prompt
    ├─ POST to AI
    ├─ Save results to .batch_result
    ├─ Wait delay_between_files
    └─ Next file
    ↓
Summary report
```

---

## Component Details

### AICoder Class

**Properties:**
- `config` - Loaded from ai_coder_config.json
- `server_process` - Subprocess handle for llama-server
- `server_running` - Boolean flag
- `source_dir` - Current project directory

**Key Methods:**

| Category | Methods |
|----------|---------|
| **Config** | `load_config()`, `save_config()` |
| **Server** | `start_server()`, `stop_server()`, `test_server()`, `check_server_status()` |
| **AI** | `ask_ai(prompt, system_prompt, max_tokens)` |
| **Files** | `read_file()`, `write_file()`, `list_source_files()` |
| **Setup** | `set_source_directory()` |
| **AI Tools** | `chat_mode()`, `fix_file()`, `review_code()`, `explain_code()`, `write_new_code()` |
| **Batch** | `batch_process()` |
| **Database** | `analyze_database()` |
| **UI** | `show_menu()`, `run()` |

---

## Configuration Structure

```json
{
  "llama_cpp": {
    "server_exe": "path/to/llama-server.exe",
    "cli_exe": "path/to/llama-cli.exe",
    "model_path": "path/to/model.gguf",
    "server_host": "127.0.0.1",
    "server_port": 8080,
    "context_size": 4096,
    "threads": 4,
    "batch_size": 512
  },
  "source_code": {
    "default_directory": "path/to/project",
    "recent_projects": [],
    "file_extensions": [".php", ".js", ...]
  },
  "ai_prompts": {
    "system_prompt": "...",
    "fix_code_prompt": "...",
    "review_prompt": "...",
    "explain_prompt": "...",
    "refactor_prompt": "...",
    "write_prompt": "..."
  },
  "batch_mode": {
    "delay_between_files": 5,
    "max_files_per_run": 50,
    "auto_save": true,
    "create_backup": true
  },
  "database": {
    "xampp_mysql_path": "...",
    "default_host": "localhost",
    "default_user": "root",
    "default_password": ""
  }
}
```

---

## File Outputs

| Extension | Created By | Purpose |
|-----------|------------|---------|
| `.ai_fixed` | Fix File (Menu 6) | AI-suggested code fixes |
| `.review` | Review Code (Menu 7) | Code review results |
| `.batch_result` | Batch Process (Menu 10) | Batch analysis output |
| `.backup_YYYYMMDD_HHMMSS` | Write operations | Automatic backups |
| `*_analysis.txt` | DB Analysis (Menu 11) | Database schema review |

---

## Memory Usage

| Component | RAM Usage |
|-----------|-----------|
| llama-server (idle) | ~200MB |
| Gemma 4 model loaded | ~4.8GB |
| AI Coder (Python) | ~50MB |
| **Total** | **~5GB** |

**Remaining for system:** ~3GB on 8GB machine

---

## Performance Characteristics

| Operation | Speed |
|-----------|-------|
| Model loading (startup) | ~30 seconds |
| AI inference | ~10 tokens/sec |
| File I/O | Instant |
| Server start/stop | 2-5 seconds |
| Batch processing | ~1-2 min per file (with AI) |

---

## Security Considerations

✅ **Fully Offline** - No data leaves your machine
✅ **No API Keys** - No credentials to leak
✅ **Local Model** - Complete privacy
✅ **Manual Review** - All AI suggestions require approval
✅ **Backups** - Automatic before changes

---

## Extensibility

### Adding New Features

1. **New Menu Option:**
   - Add method to AICoder class
   - Add to show_menu()
   - Add to actions dict in run()

2. **New Prompt Templates:**
   - Add to ai_prompts in config JSON
   - Use format() with placeholders

3. **New File Types:**
   - Add extensions to source_code.file_extensions

4. **Custom Analysis:**
   - Add batch task option
   - Create prompt template
   - Implement in batch_process()

---

## Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `colorama` | Colored terminal output | 0.4.6 |
| `requests` | HTTP client for AI API | 2.23+ |
| `subprocess` | Server management | Built-in |
| `json` | Config handling | Built-in |
| `glob` | File searching | Built-in |

---

## Error Handling

```
┌─────────────────────────────────────┐
│         Error Types                  │
├─────────────────────────────────────┤
│ Server not found → Check paths      │
│ Server timeout → Increase wait      │
│ AI request fail → Retry or warn     │
│ File read fail → Skip & continue    │
│ Database fail → Show error details  │
│ Memory low → Reduce context size    │
│ Context overflow → Reduce code input│
└─────────────────────────────────────┘
```

All errors are caught with try/except and displayed with colored indicators:
- 🔴 Red: Critical errors (can't continue)
- 🟡 Yellow: Warnings (can continue with limitations)
- 🟢 Green: Success messages

---

**End of Architecture Document**
