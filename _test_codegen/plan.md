# AI Coder Project Plan

> **Lightweight Agentic AI Code Editor for Multi-Language Development**

---

## Project Overview

Build a Python-based agentic tool that uses local **llama.cpp + Gemma 4** (offline AI) to assist with:
- Reading, analyzing, and editing code
- Finding and fixing bugs automatically
- Code review (security, performance, style)
- Writing new code from requirements
- Batch processing for 24/7 automation
- Database schema analysis

**Target Languages:** PHP (CodeIgniter), Python, Golang  
**Database:** MySQL (XAMPP)  
**AI Model:** Gemma 4 E2B Q4_K_M (3.46GB, offline)

---

## Architecture

```
User Interface (Menu-Driven Python CLI)
    ↓
AI Coder (ai_coder.py)
    ├─ Server Management (start/stop llama-server)
    ├─ File Operations (read/write code files)
    ├─ AI Communication (HTTP REST API)
    ├─ Batch Processing (automated 24/7)
    └─ Database Analysis (MySQL queries)
    ↓
llama-server.exe (local AI API)
    ↓
Gemma 4 Model (offline inference)
```

---

## Current Implementation (Completed ✅)

### Phase 1: Core Infrastructure
- ✅ Configuration system (`ai_coder_config.json`)
- ✅ Main menu system (11 options)
- ✅ Server management (start/stop/check llama-server)
- ✅ File I/O operations (read/write with backup)
- ✅ AI communication via REST API
- ✅ Colored terminal output (colorama)
- ✅ Test suite

### Phase 2: AI Tools
- ✅ Interactive chat mode (free-form questions)
- ✅ File fixing (select file, describe problem, AI fixes)
- ✅ Code review (security, performance, style)
- ✅ Code explanation
- ✅ New code generation
- ✅ Batch processing mode (24/7 automation)
- ✅ MySQL database analysis

### Phase 3: Documentation
- ✅ Complete user guide (`AI_CODER_USAGE.md`)
- ✅ Architecture documentation (`AI_CODER_ARCHITECTURE.md`)
- ✅ Quick reference (`README_AI_CODER.md`)
- ✅ Configuration examples
- ✅ PHP/CodeIgniter examples

---

## Planned Enhancements

### Phase 4: Multi-Language Support (✅ COMPLETED)

#### 4.1 Python Support (✅ Done)
- ✅ Add Python-specific prompt templates
  - PEP 8 style checking
  - Virtual environment awareness
  - pip package management
  - Common frameworks (Flask, FastAPI, Django)
  - pytest integration
- ✅ Python file detection and analysis
- ✅ Import dependency analysis
- ✅ Type hint checking
- ✅ Async/await pattern recognition

#### 4.2 Golang Support (✅ Done)
- ✅ Add Go-specific prompt templates
  - Idiomatic Go patterns
  - Error handling best practices
  - Go modules (go.mod) awareness
  - Goroutine and channel analysis
  - Interface design
- ✅ Go file detection (.go files)
- ✅ Package structure analysis
- ✅ Import cycle detection
- ✅ go fmt/vet integration

#### 4.3 Multi-Language Features (✅ Done)
- ✅ Automatic language detection from file extension
- ✅ Language-specific prompt templates
- ✅ Language-aware batch tasks
  - Python: PEP 8 compliance check (Batch Task 5)
  - Go: Idiomatic patterns review (Batch Task 6)
  - PHP: Security checks (Batch Task 2)
- ✅ Language-specific linting suggestions
- ✅ Multi-language configuration in config file
- ✅ Sample files for testing (Python & Go)

---

### Phase 5: Advanced Features (TODO)

#### 5.1 Project Intelligence
- [ ] Code structure mapping (auto-detect architecture)
- [ ] Dependency graph generation
- [ ] Function call tracking
- [ ] Duplicate code detection
- [ ] Dead code identification

#### 5.2 Database Integration
- [ ] Auto-detect database config from CodeIgniter/Python/Go
- [ ] ORM mapping analysis (SQLAlchemy, GORM)
- [ ] Migration file generation
- [ ] Query optimization suggestions
- [ ] Schema comparison between environments

#### 5.3 Testing Support
- [ ] Generate test cases from requirements
- [ ] Create unit test templates
- [ ] pytest test generation (Python)
- [ ] go test generation (Go)
- [ ] PHPUnit test generation (PHP)
- [ ] Mock object generation

#### 5.4 Git Integration
- [ ] Commit message generation
- [ ] Code review on PR diff
- [ ] Merge conflict resolution assistance
- [ ] Change impact analysis
- [ ] Automated changelog generation

---

### Phase 6: Automation & Scheduling (TODO)

#### 6.1 Task Scheduling
- [ ] Cron-like scheduling for batch tasks
- [ ] Run security review every night at 2 AM
- [ ] Generate documentation weekly
- [ ] Monitor for code quality regression

#### 6.2 Continuous Integration
- [ ] Watch for file changes (file system monitoring)
- [ ] Auto-review on save
- [ ] Auto-fix on commit
- [ ] Pre-commit hook integration

#### 6.3 Reporting
- [ ] Generate weekly quality reports
- [ ] Track code metrics over time
- [ ] Email/Slack notifications
- [ ] Dashboard with metrics

---

### Phase 7: UI/UX Improvements (TODO)

#### 7.1 Better Terminal UI
- [ ] Progress bars for batch operations
- [ ] Syntax highlighting for code display
- [ ] Interactive diff viewer (original vs fixed)
- [ ] Searchable history
- [ ] Tab completion for file paths

#### 7.2 Web Interface (Optional)
- [ ] Simple Flask/FastAPI web UI
- [ ] File browser
- [ ] Chat interface
- [ ] Results viewer
- [ ] Configuration editor

#### 7.3 IDE Integration
- [ ] VS Code extension
- [ ] Vim/Neovim plugin
- [ ] LSP (Language Server Protocol) support

---

## Configuration Updates Needed

### Current State
```json
{
  "ai_prompts": {
    "system_prompt": "PHP/CodeIgniter focused",
    "fix_code_prompt": "PHP examples",
    ...
  }
}
```

### Target State
```json
{
  "ai_prompts": {
    "system_prompt": "Multi-language expert (PHP, Python, Go)",
    "fix_code_prompt": "Language-agnostic with examples",
    "python_prompts": {
      "pep8_review": "...",
      "pytest_gen": "...",
      "flask_controller": "..."
    },
    "go_prompts": {
      "idiomatic_review": "...",
      "test_gen": "...",
      "http_handler": "..."
    },
    "php_prompts": {
      "codeigniter_review": "...",
      "phpunit_gen": "...",
      "controller": "..."
    }
  },
  "languages": {
    "php": {
      "extensions": [".php"],
      "frameworks": ["CodeIgniter", "Laravel", "Symfony"],
      "lint_command": "php -l"
    },
    "python": {
      "extensions": [".py"],
      "frameworks": ["Flask", "FastAPI", "Django"],
      "lint_command": "python -m pylint"
    },
    "go": {
      "extensions": [".go"],
      "frameworks": ["net/http", "gin", "echo", "fiber"],
      "lint_command": "go vet"
    }
  }
}
```

---

## File Structure (Current)

```
_testcodegen/
├── ai_coder.py                    # Main program ✅
├── ai_coder_config.json           # Configuration ✅
├── run_ai_coder.bat               # Quick launcher ✅
├── AI_CODER_USAGE.md              # User guide ✅
├── AI_CODER_ARCHITECTURE.md       # Architecture docs ✅
├── README_AI_CODER.md             # Quick reference ✅
├── test_ai_coder.py               # Test suite ✅
└── plan.md                        # This file ✅
```

---

## Implementation Priority

### High Priority (Next)
1. **Update config** for Python & Go support
2. **Add Python prompt templates** (PEP 8, Flask, FastAPI)
3. **Add Go prompt templates** (idiomatic patterns, goroutines)
4. **Update file detection** to include .py and .go
5. **Add language detection** (auto-detect from file extension)

### Medium Priority
6. Language-specific batch tasks
7. Dependency analysis (pip, go modules)
8. Test generation (pytest, go test, PHPUnit)
9. Better error handling and retry logic

### Low Priority (Future)
10. Git integration
11. Scheduled tasks
12. Web interface
13. IDE plugins

---

## Technical Considerations

### Context Window Management
- Gemma 4 E2B has limited context (use 2048-4096 on 8GB RAM)
- Large files need chunking strategy
- Multi-file analysis requires careful prompt construction
- **Solution:** Smart file selection, focus on relevant sections

### Multi-Language Prompts
- Each language has different conventions
- Need language-specific prompt templates
- AI should detect language automatically
- **Solution:** Config-based prompts per language, extension detection

### Performance on 8GB RAM
- Model uses ~4.8GB RAM
- Only ~3GB available for everything else
- Batch processing needs delays
- **Solution:** Conservative context sizes, file-by-file processing

### Backup & Safety
- Always backup before AI modifies files
- Require manual review before applying changes
- Create `.ai_fixed` files, don't overwrite originals
- **Solution:** Already implemented, keep this approach

---

## Success Metrics

### Current
- ✅ Can start/stop AI server from menu
- ✅ Can set source code directory
- ✅ Can chat with AI about code
- ✅ Can fix individual files with AI help
- ✅ Can batch process files overnight
- ✅ Can analyze MySQL database

### Target
- ☐ Support Python files (.py) with framework awareness
- ☐ Support Golang files (.go) with idiomatic pattern detection
- ☐ Auto-detect language and apply correct prompts
- ☐ Generate tests for Python/Go/PHP
- ☐ Analyze dependencies across all three languages
- ☐ Language-specific linting suggestions
- ☐ Scheduled overnight tasks
- ☐ Weekly quality reports

---

## Development Workflow

```
1. Identify feature need (e.g., "Python support")
2. Update config (add prompts, extensions)
3. Implement feature in ai_coder.py
4. Test with sample files
5. Update documentation
6. Add to test suite
7. Mark as complete in this plan
```

---

## Notes

- **Gemma 4 E2B is small** (3.46GB) - can't handle very complex tasks
- **Keep prompts focused** - specific questions get better answers
- **Batch mode is key feature** - overnight automation is valuable
- **Safety first** - never auto-apply changes without review
- **Offline-only** - no cloud dependencies

---

**Last Updated:** 2025-04-15  
**Status:** Phase 4 Complete ✅ | Phase 5 Planning 🚧

---

## Recent Updates (2025-04-15)

### ✅ Multi-Language Support Added

**New Features:**
- Automatic language detection from file extension (.php, .py, .go)
- Language-specific prompt templates for PHP, Python, and Go
- Python support with PEP 8, Flask, FastAPI, Django awareness
- Go support with idiomatic patterns, Effective Go guidelines
- Multi-language batch processing (Tasks 5 & 6)
- Language-aware code review and fixing
- Sample Python and Go files for testing

**Files Modified:**
- `ai_coder_config.json` - Added language configurations and prompts
- `ai_coder.py` - Added language detection and multi-language methods
- `plan.md` - Updated Phase 4 status to Complete
- `sample_python_app.py` - New Python Flask example
- `sample_go_app.go` - New Go HTTP server example
- `test_multilang.py` - New multi-language test suite

**Test Results:**
- ✅ All original tests pass (4/4)
- ✅ All multi-language tests pass (4/4)
- ✅ Language detection works for 11 file types
- ✅ Python and Go file analysis working
