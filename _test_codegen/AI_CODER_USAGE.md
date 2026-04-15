# AI Coder - Lightweight Agentic Code Editor

> **Your Offline AI Programming Assistant for PHP/CodeIgniter + MySQL**

---

## Overview

AI Coder is a lightweight, menu-driven Python tool that uses your local **llama.cpp + Gemma 4** model to help you:
- Read and analyze code
- Find and fix bugs
- Review code quality
- Write new features
- Process files in batch mode (24/7 automation)
- Analyze MySQL database schemas

**No cloud APIs, no internet required** - everything runs offline on your machine.

---

## Version 2.0 - Modular Architecture

The new modular version uses agents for different tasks:

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

### Key Features
- **Session Persistence** - If program crashes or restarts, it will ask to resume from where you left off
- **Multi-level folders** - Creates nested directories like `app/Views/users/`
- **Retry logic** - 3 automatic retries on timeout (common with CPU inference)
- **YOLO Mode** - Auto-save files without asking (default)

---

## Quick Start

### Step 1: Start the AI Coder (Modular Version)

```powershell
cd C:\dev\ai_setup_llama_cpp\_test_codegen
python ai_coder_modular\ai_coder.py
```

Or use the old version:
```powershell
python ai_coder.py
```

### Step 2: Start the AI Server (Menu 1)

From the main menu, select **Option 1** to start the llama.cpp server.

**What happens:**
- Loads Gemma 4 model (~30 seconds)
- Starts API server on `http://127.0.0.1:8080`
- Ready to answer questions

**Keep AI Coder running** - don't close the window.

### Step 3: Set Your Source Code Directory (Menu 4)

Select **Option 4** and enter the path to your PHP/CodeIgniter project:

```
Enter source directory path: C:\xampp\htdocs\myproject
```

AI Coder will:
- Scan all source files
- Count available files
- Save the path for future sessions

### Step 4: Use AI Tools (Menu 5-11)

Now you can use any AI feature!

---

## Main Menu Guide

```
============================================================
  AI Coder - Lightweight Agentic Code Editor
  Powered by llama.cpp + Gemma 4 (Offline)
============================================================

Server: Running
Source: C:\xampp\htdocs\myproject

Server Management:
  1. Start AI Server          ← Start llama-server
  2. Stop AI Server           ← Stop llama-server
  3. Check Server Status      ← Verify server is running

Source Code:
  4. Set Source Directory     ← Point to your project

AI Tools:
  5. Chat with AI             ← Free-form questions
  6. Fix File with AI         ← Select file, describe problem
  7. Review Code Quality      ← Security, performance, style check
  8. Explain Code             ← What does this code do?
  9. Write New Code           ← Generate Controller/Model/View

Automation:
  10. Batch Process (24/7)    ← Process many files automatically

Database:
  11. Analyze MySQL Database  ← Schema review & optimization

Other:
  0. Exit
```

---

## Feature Details

### 1-3. Server Management

**Start AI Server (Menu 1)**
- Automatically starts llama-server with optimal settings
- Shows progress while loading
- Tests connection when ready

**Stop AI Server (Menu 2)**
- Gracefully stops the server
- Frees up RAM

**Check Server Status (Menu 3)**
- Verifies if server is responding
- Shows current state

---

### 4. Set Source Directory

Points AI Coder to your CodeIgniter project.

**Example:**
```
Select [0-11]: 4

Current: C:\xampp\htdocs\oldproject

Enter source directory path: C:\xampp\htdocs\newproject

[✓] Source directory set: C:\xampp\htdocs\newproject
    Found 127 source files
```

**Supported file types:**
- `.php` - Controllers, Models, Views, Libraries
- `.js` - JavaScript files
- `.html` - View templates
- `.css` - Stylesheets
- `.sql` - Database scripts
- `.json`, `.xml`, `.md` - Config & docs

---

### 5. Chat with AI (Interactive)

Free-form conversation with AI about your code.

**Use cases:**
- Ask how to implement a feature
- Get CodeIgniter help
- Understand error messages
- General programming questions

**Example:**
```
You: How do I create a login controller in CodeIgniter 4?

AI: Here's how to create a login controller:

```php
<?php
namespace App\Controllers;

use App\Controllers\BaseController;

class Login extends BaseController
{
    public function index()
    {
        return view('login/form');
    }
    
    public function authenticate()
    {
        $username = $this->request->getPost('username');
        $password = $this->request->getPost('password');
        
        // Your authentication logic here
        // ...
    }
}
```

Save this to `app/Controllers/Login.php`...
```

**Tips:**
- Reference files with `@filename.php`
- Type `exit` or `quit` to return to menu
- Keep questions specific and clear

---

### 6. Fix File with AI

Select a file, describe the problem, AI analyzes and suggests fixes.

**Example workflow:**

```
Select [0-11]: 6

Available files:
  1. app\Controllers\UserController.php
  2. app\Models\UserModel.php
  3. app\Views\login.php
  ...

Select file number (or type full path): 1

File: app\Controllers\UserController.php
Size: 2847 bytes

Describe the problem (or press Enter for general review): 
Getting "Undefined variable $user" error on line 45 when login fails
```

**AI Response:**
```
============================================================
  AI Analysis & Fix
============================================================

I found the issue in your UserController.php:

**Problem:**
On line 45, you're trying to access `$user->username` but the `$user` 
variable is only set when login succeeds. When authentication fails, 
`$user` remains undefined.

**Current code (line 40-50):**
```php
$user = $userModel->verify($username, $password);

if (!$user) {
    session()->setFlashdata('error', 'Invalid credentials');
}

return redirect()->to('/dashboard')->with('user', $user->username);
                                                        ^ Problem here
```

**Fixed code:**
```php
$user = $userModel->verify($username, $password);

if (!$user) {
    session()->setFlashdata('error', 'Invalid credentials');
    return redirect()->to('/login');  // Return early
}

// Now $user is guaranteed to exist
return redirect()->to('/dashboard')->with('user', $user->username);
```

**Why this works:**
- Added early return when login fails
- Prevents accessing undefined `$user`
- Follows redirect pattern properly

Apply AI suggestions to file? (y/n): y
[✓] AI fix saved to: UserController.php.ai_fixed
    Review before replacing original file
```

---

### 7. Review Code Quality

Comprehensive code review covering:
- ✓ Bugs and errors
- ✓ Security vulnerabilities (SQL injection, XSS, CSRF)
- ✓ Performance issues
- ✓ Code style and best practices
- ✓ Database query optimization

**Example:**
```
Select [0-11]: 7

Select file to review:
  1. app\Controllers\UserController.php
  2. app\Models\UserModel.php
  
Select file number: 2

[AI] Reviewing app\Models\UserModel.php...

============================================================
  Code Review Results
============================================================

**Security Issues:**

1. **CRITICAL** - SQL Injection Risk (Line 23)
   ```php
   $query = $this->db->query("SELECT * FROM users WHERE email='$email'");
   ```
   **Fix:** Use query builder:
   ```php
   $query = $this->db->table('users')->where('email', $email)->get();
   ```

2. **HIGH** - Password not hashed (Line 45)
   Storing plain-text passwords
   **Fix:** Use `password_hash($password, PASSWORD_DEFAULT)`

**Performance Issues:**

3. **MEDIUM** - N+1 Query Problem (Line 67)
   Fetching related records in loop
   **Fix:** Use JOIN or eager loading

**Code Style:**

4. **LOW** - Missing type hints on method parameters
   **Fix:** Add `string $email`, `int $id`, etc.

**Summary:** 4 issues found (1 Critical, 1 High, 1 Medium, 1 Low)

[✓] Review saved to: UserModel.php.review
```

---

### 8. Explain Code

AI explains what a file does step-by-step.

**Great for:**
- Understanding legacy code
- Onboarding to existing projects
- Learning how features work

**Example:**
```
Select [0-11]: 8

Select file to explain:
  1. app\Libraries\PaymentGateway.php

[AI] Explaining app\Libraries\PaymentGateway.php...

============================================================
  Code Explanation
============================================================

This `PaymentGateway` library handles payment processing for your 
application. Here's what it does step by step:

**1. Initialization (constructor)**
- Loads configuration from `Config/Payment.php`
- Sets up API credentials
- Initializes HTTP client

**2. processPayment() method**
- Validates payment amount and currency
- Encrypts sensitive card data
- Sends request to payment API
- Handles response and errors
- Returns transaction ID or failure message

**3. verifyPayment() method**
- Checks transaction status with API
- Updates database record
- Triggers webhook if successful

**Key dependencies:**
- Requires `Config/Payment.php` for settings
- Uses `Database` connection for logging
- Depends on external payment API

**Potential issues:**
- No retry logic for failed API calls
- Error messages could be more specific
```

---

### 9. Write New Code

AI generates new Controllers, Models, Views, or Libraries.

**Example:**
```
Select [0-11]: 9

What type? (Controller/Model/View/Library/Script): Controller

Describe requirements: 
User registration with email validation, duplicate check, 
and welcome email sending

CodeIgniter version? (3/4, default 4): 4

[AI] Writing Controller...

============================================================
  Generated Code
============================================================

```php
<?php
namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\UserModel;
use App\Libraries\EmailService;

class Registration extends BaseController
{
    public function create()
    {
        return view('registration/form');
    }
    
    public function store()
    {
        // Validation rules
        $rules = [
            'username' => 'required|min_length[3]|max_length[30]|is_unique[users.username]',
            'email'    => 'required|valid_email|is_unique[users.email]',
            'password' => 'required|min_length[8]'
        ];
        
        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }
        
        // Create user
        $userModel = new UserModel();
        $userData = [
            'username' => $this->request->getPost('username'),
            'email'    => $this->request->getPost('email'),
            'password' => password_hash($this->request->getPost('password'), PASSWORD_DEFAULT)
        ];
        
        $userId = $userModel->insert($userData);
        
        // Send welcome email
        $emailService = new EmailService();
        $emailService->sendWelcomeEmail($userData['email'], $userData['username']);
        
        return redirect()->to('/login')->with('success', 'Registration successful!');
    }
}
```

Save to file? (y/n): y
Filename: app/Controllers/Registration.php

[✓] Code saved to: Registration.php
```

---

### 10. Batch Process (24/7 Mode)

Process multiple files automatically - perfect for overnight work!

**Available batch tasks:**
1. Review all files for code quality
2. Check for security issues
3. Generate documentation
4. Find and fix common bugs
5. Custom prompt for all files

**Example:**
```
Select [0-11]: 10

Found 127 files

Select batch task:
  1. Review all files for code quality
  2. Check for security issues
  3. Generate documentation
  4. Find and fix common bugs
  5. Custom prompt for all files

Select task [1-5]: 2

Processing up to 50 files...
Press Ctrl+C to stop at any time

[1/50] app\Controllers\UserController.php
  [✓] Done - Results saved

[2/50] app\Models\UserModel.php
  [✓] Done - Results saved

  Waiting 5s...

[3/50] app\Controllers\Dashboard.php
  [✓] Done - Results saved

...

============================================================
  Batch Processing Complete
============================================================
  Processed: 50
  Errors: 0
  Results saved to .batch_result files
```

**Results:**
- Each file gets a `.batch_result` file with AI analysis
- Review results and apply fixes manually
- Can process 50+ files in one run
- Add delay between files to avoid overloading AI

**24/7 Usage Tips:**
- Set task before leaving (e.g., security review)
- Let it run overnight
- Check results in the morning
- Apply fixes as needed

---

### 11. Analyze MySQL Database

Connect to your XAMPP MySQL database and get AI-powered schema analysis.

**Example:**
```
Select [0-11]: 11

MySQL Host [localhost]: 
MySQL User [root]: 
MySQL Password []: 
Database name: myapp_db

[DB] Connecting to MySQL...
[✓] Connected successfully
    Found 12 tables

Tables: users, posts, comments, categories, sessions, ...

[DB] Analyzing schema...

============================================================
  Database Analysis Results
============================================================

**Schema Design Review:**

1. **users** table ✓
   - Good: Proper primary key
   - Good: Email index for fast lookups
   - Suggestion: Add `created_at` and `updated_at` timestamps

2. **posts** table ⚠
   - Issue: Missing foreign key on `user_id`
   - Issue: `content` column should be TEXT, not VARCHAR(255)
   - Suggestion: Add index on `status` for filtering

**Index Recommendations:**

```sql
-- Add these indexes for better performance:
ALTER TABLE `posts` ADD INDEX `idx_user_id` (`user_id`);
ALTER TABLE `posts` ADD INDEX `idx_status` (`status`);
ALTER TABLE `comments` ADD INDEX `idx_post_id` (`post_id`);
```

**Performance Optimizations:**

- Consider adding query cache for frequently-read tables
- Use `EXPLAIN` on slow queries to check index usage
- Add composite index on `(user_id, status)` for dashboard queries

**Potential Issues:**

- No foreign key constraints (data integrity risk)
- Missing soft-delete columns
- No audit trail columns

[✓] Analysis saved to: myapp_db_analysis.txt
```

---

## Configuration

Edit `ai_coder_config.json` to customize settings:

```json
{
  "llama_cpp": {
    "server_port": 8080,        // Change API port
    "context_size": 4096,       // AI memory (lower = less RAM)
    "threads": 4,               // CPU threads to use
    "batch_size": 512           // Processing batch size
  },
  "source_code": {
    "default_directory": "",    // Your project path
    "file_extensions": [".php", ".js", ".html"]  // File types to scan
  },
  "batch_mode": {
    "delay_between_files": 5,   // Seconds between files
    "max_files_per_run": 50,    // Limit per batch
    "create_backup": true       // Backup before changes
  }
}
```

---

## PHP/CodeIgniter Examples

### Example 1: Fix Database Query Error

**Problem:** Query returns empty results

**Chat prompt:**
```
@Models/ProductModel.php line 34 returns empty array even though 
database has products. Here's the method:

public function getActiveProducts() {
    return $this->where('status', 'active')->findAll();
}

Database table has status='Active' (capital A). Is this the issue?
```

**AI Response:**
```
Yes! This is a case-sensitivity issue.

Your database has `status='Active'` but your query checks for 
`status='active'` (lowercase). MySQL string comparisons are 
case-sensitive by default with UTF-8 collation.

**Fix options:**

1. **Match the case:**
```php
return $this->where('status', 'Active')->findAll();
```

2. **Case-insensitive comparison:**
```php
return $this->where('LOWER(status)', 'active')->findAll();
```

3. **Best practice - Use constant:**
```php
const STATUS_ACTIVE = 'Active';

public function getActiveProducts() {
    return $this->where('status', self::STATUS_ACTIVE)->findAll();
}
```

I recommend option 3 for consistency across your codebase.
```

---

### Example 2: Add Pagination to Controller

**Chat prompt:**
```
Add pagination to this controller method. Show 20 items per page.

Current method:
public function listAll() {
    $productModel = new ProductModel();
    $data['products'] = $productModel->findAll();
    return view('products/list', $data);
}
```

**AI Response:**
```php
public function listAll() {
    $productModel = new ProductModel();
    
    // Pagination config
    $perPage = 20;
    $page = (int) ($this->request->getGet('page') ?? 1);
    $offset = ($page - 1) * $perPage;
    
    // Get paginated results
    $data['products'] = $productModel
        ->orderBy('created_at', 'DESC')
        ->limit($perPage, $offset)
        ->findAll();
    
    // Total count for pagination links
    $data['total'] = $productModel->countAll();
    $data['perPage'] = $perPage;
    $data['currentPage'] = $page;
    
    return view('products/list', $data);
}
```

**View pagination links:**
```php
<?php 
$totalPages = ceil($total / $perPage);
for ($i = 1; $i <= $totalPages; $i++): 
?>
    <a href="?page=<?= $i ?>" 
       class="<?= $i == $currentPage ? 'active' : '' ?>">
        <?= $i ?>
    </a>
<?php endfor; ?>
```

---

## Troubleshooting

### Server Won't Start

**Problem:** `[✗] Server executable not found`

**Solution:**
1. Check config file has correct path:
   ```json
   "server_exe": "C:\\dev\\ai_setup_llama_cpp\\llama-cpp\\llama-server.exe"
   ```
2. Verify file exists:
   ```powershell
   Test-Path C:\dev\ai_setup_llama_cpp\llama-cpp\llama-server.exe
   ```

---

### AI Gives Incomplete Answers

**Problem:** Response cuts off mid-sentence

**Solution:**
1. Increase context size in config:
   ```json
   "context_size": 4096  // Increase to 8192 if you have 16GB RAM
   ```
2. Reduce code per request (show only relevant parts)
3. Ask follow-up questions: "Continue from where you left off"

---

### Batch Mode Too Slow

**Problem:** Processing takes too long

**Solution:**
1. Reduce delay in config:
   ```json
   "delay_between_files": 2  // Reduce from 5 to 2 seconds
   ```
2. Increase max files:
   ```json
   "max_files_per_run": 100
   ```
3. Run overnight for large projects

---

### Out of Memory

**Problem:** Server crashes or system slows down

**Solution:**
1. Reduce context size:
   ```json
   "context_size": 2048  // Lower for 8GB RAM
   ```
2. Close other applications
3. Reduce threads:
   ```json
   "threads": 2  // Use fewer CPU threads
   ```

---

### Database Connection Fails

**Problem:** `[✗] Connection failed`

**Solution:**
1. Verify MySQL is running in XAMPP Control Panel
2. Check credentials (default: root / no password)
3. Test manually:
   ```powershell
   C:\xampp\mysql\bin\mysql.exe -u root
   ```

---

## Advanced Usage

### Running 24/7 Unattended

1. **Prepare before leaving:**
   ```
   - Set source directory
   - Start AI server
   - Select Batch Process (Menu 10)
   - Choose task (e.g., security review)
   - Let it run
   ```

2. **Next morning:**
   ```
   - Check .batch_result files
   - Review AI suggestions
   - Apply fixes manually
   - Test changes
   ```

---

### Custom AI Prompts

Edit `ai_coder_config.json` to add your own prompt templates:

```json
{
  "ai_prompts": {
    "my_custom_prompt": "You are a CodeIgniter expert. Review this code for: {specific_items}\n\nCode:\n{code}"
  }
}
```

---

### Multi-File Analysis

For complex issues spanning multiple files:

1. Use Chat mode (Menu 5)
2. Reference files with `@filename`
3. Paste relevant sections from each file
4. Ask AI to analyze relationships and flow

---

## Comparison with Other Tools

| Feature | AI Coder | OpenCode | Gemini CLI |
|---------|----------|----------|------------|
| **Offline** | ✓ Yes | Partial | ✗ No |
| **Cost** | Free | Free/Paid | Paid |
| **Privacy** | 100% Local | Varies | Cloud |
| **Speed** | ~10 tok/s | ~20 tok/s | ~50 tok/s |
| **RAM Usage** | ~5GB | ~3GB | Cloud |
| **Code Editing** | Manual review | Auto-apply | Auto-apply |
| **Batch Mode** | ✓ Yes | Limited | ✗ No |
| **24/7 Work** | ✓ Yes | Partial | ✗ No |
| **Database Analysis** | ✓ Yes | ✗ No | ✗ No |

**AI Coder is best for:**
- Offline/air-gapped environments
- Privacy-sensitive projects
- Overnight batch processing
- Learning and understanding code
- Low-resource machines (8GB RAM)

---

## Performance Tips

| Setting | 8GB RAM | 16GB RAM |
|---------|---------|----------|
| `context_size` | 2048-4096 | 8192 |
| `threads` | 4 | 8 |
| `batch_size` | 512 | 1024 |
| **Max code per request** | 2500 chars | 5000 chars |

**For faster responses:**
- Close browser tabs and other apps
- Reduce `-t` (threads) to match physical CPU cores
- Use smaller context size

---

## File Outputs

AI Coder creates result files for review:

| Extension | Purpose |
|-----------|---------|
| `.ai_fixed` | AI-suggested code fixes |
| `.review` | Code review results |
| `.batch_result` | Batch processing output |
| `.backup_YYYYMMDD_HHMMSS` | Automatic backup before changes |
| `*_analysis.txt` | Database analysis |

**Always review AI output before applying to production!**

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  START                                                    │
│  python ai_coder.py                                       │
│                                                           │
│  MENU OPTIONS                                             │
│  1-3: Server management (start/stop/check)                │
│  4:   Set source directory                                │
│  5:   Chat with AI (free form)                            │
│  6:   Fix specific file                                   │
│  7:   Review code quality                                 │
│  8:   Explain what code does                              │
│  9:   Write new code from requirements                    │
│  10:  Batch process (24/7 automation)                     │
│  11:  Analyze MySQL database                              │
│  0:   Exit                                                │
│                                                           │
│  TIPS                                                     │
│  - Start server first (Menu 1)                            │
│  - Set source directory (Menu 4)                          │
│  - Use batch mode overnight                               │
│  - Review all AI suggestions before applying              │
│  - Check .batch_result files after automation             │
│                                                           │
│  STOP                                                     │
│  Menu 0 or Ctrl+C (server auto-stops)                     │
└─────────────────────────────────────────────────────────┘
```

---

## Support & Updates

For issues or questions:
1. Check `ai_coder_config.json` paths are correct
2. Verify llama.cpp server is installed
3. Ensure Gemma 4 model is downloaded
4. Check XAMPP MySQL is running (for DB features)

---

## Workflow Summary

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

**Enjoy coding with AI assistance! 🚀**
