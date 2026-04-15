# Skill: Test Autonomous Agent

## Purpose
Test the Autonomous Agent (menu 8) which creates a complete CRUD system for user management.

## Steps to Execute

### 1. Start the AI Server (if not running)
- Run: `cd C:\dev\ai_setup_llama_cpp\_test_codegen`
- Run: `python ai_coder_modular\ai_coder.py`
- Select: `1` to start server
- Wait for "Server started!" message

### 2. Set Source Directory
- Select: `4`
- Enter: `C:\dev\ai_local_webapp_php` (or your test project directory)

### 3. Run Autonomous Agent (Menu 8)
- Select: `8`
- Enter task: `create a complete CRUD system for user management`

### 4. Monitor Progress
Watch for:
- [Step 1/3] Creating project plan...
- [Step 2/3] Creating files...
- Progress updates every 5 files
- Files being created with timestamps

### 5. Expected Output
Should see:
- Files created: 10-15 files
- Duration: varies based on model speed
- Completed files list

## Verification
Check the source directory for:
- app/Controllers/UserController.php
- app/Models/UserModel.php
- app/Views/users/index.php
- app/Views/users/create.php
- app/Views/users/edit.php
- etc.

## Troubleshooting
- If timeout: retry logic handles 3 attempts
- If no files extracted: check debug output
- If session crash: can resume from last save point