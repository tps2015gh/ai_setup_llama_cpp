"""
Autonomous Agent - Loops until task is complete
YOLO Mode: Automatic save without asking (default)
"""

from .base import BaseAgent
from colorama import Fore, Style
import os
import re
import time
import json


class AutonomousAgent(BaseAgent):
    """Agent that loops and creates/edits files until task is done"""
    
    def get_session_file(self):
        """Get session state file path"""
        session_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        return os.path.join(session_dir, 'ai_session.json')
    
    def save_session(self, task, todo, completed, errors, loop_count):
        """Save current session state"""
        session = {
            'task': task,
            'todo': todo,
            'completed': completed,
            'errors': errors,
            'loop_count': loop_count,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            with open(self.get_session_file(), 'w') as f:
                json.dump(session, f)
            print(f"{Fore.YELLOW}[SESSION] Progress saved{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[SESSION] Save failed: {e}{Style.RESET_ALL}")
    
    def load_session(self):
        """Load previous session if exists"""
        session_file = self.get_session_file()
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session = json.load(f)
                print(f"\n{Fore.YELLOW}[SESSION] Found previous session:{Style.RESET_ALL}")
                print(f"  Task: {session.get('task', 'Unknown')[:50]}...")
                print(f"  Completed: {len(session.get('completed', []))} files")
                print(f"  Remaining: {len(session.get('todo', []))} files")
                print(f"  Last run: {session.get('timestamp', 'Unknown')}\n")
                
                confirm = input(f"{Fore.GREEN}Resume? (y/n): {Style.RESET_ALL}").strip().lower()
                if confirm == 'y':
                    return session
                else:
                    # Clear session
                    os.remove(session_file)
            except Exception as e:
                print(f"{Fore.RED}[SESSION] Load failed: {e}{Style.RESET_ALL}")
        return None
    
    def clear_session(self):
        """Clear session file"""
        session_file = self.get_session_file()
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except:
                pass
    
    def run(self, task, yolo_mode=None):
        """Run autonomous agent
        
        Args:
            task: The task description
            yolo_mode: None or True = auto-save (default). False = ask confirmation.
        """
        # Force YOLO by default for long-running autonomous tasks
        if yolo_mode is None:
            yolo_mode = True
        
        if not self.ensure_source_dir():
            return False
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Autonomous Agent - Loop Mode{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Start: {self.get_timestamp()}{Style.RESET_ALL}\n")
        
        mode_str = f"{Fore.GREEN}YOLO (Auto-save){Style.RESET_ALL}" if yolo_mode else f"{Fore.YELLOW}Manual (Confirm){Style.RESET_ALL}"
        self.log(f"Mode: {mode_str}")
        self.log(f"Task: {task}")
        print(f"{Fore.YELLOW}The AI will loop and create files until done{Style.RESET_ALL}\n")
        
        max_loops = 5000
        completed = []
        todo = []
        loop_count = 0
        errors = 0
        start_time = time.time()
        
        # Check for previous session
        session = self.load_session()
        if session:
            todo = session.get('todo', [])
            completed = session.get('completed', [])
            errors = session.get('errors', 0)
            loop_count = session.get('loop_count', 0)
            self.log(f"[SESSION] Resuming from loop {loop_count}")
        else:
            # Initial planning - ask for MORE files (only if no session)
            self.log("[Step 1/3] Creating project plan...")
            
            files = self.files.list_files()
            file_list = "\n".join([os.path.relpath(f, self.get_source_dir()) for f in files[:30]])
            
            prompt = f"""Task: {task}

Current project files:
{file_list}

List ALL files that need to be created for a COMPLETE working system.
Include: migrations, models, controllers, views, routes, config, etc.
List at least 10-15 files minimum. One file per line with full path.
Example format:
app/Controllers/UserController.php
app/Models/UserModel.php
app/Views/users/index.php"""

            response = self.ask_ai(prompt, max_tokens=1500)
            
            if response:
                todo = self.extract_todo(response)
            
            # If too few files, ask AI to expand
            if todo and len(todo) < 5:
                self.log(f"Only {len(todo)} files planned. Asking for more...")
                prompt2 = f"""Task: {task}

Already planned: {', '.join(todo)}

What ADDITIONAL files are needed? List more files that should be created.
Include: views, controllers, models, config, helpers, etc.
Reply with list of additional files, one per line."""

                response2 = self.ask_ai(prompt2, max_tokens=800)
                if response2:
                    more_files = self.extract_todo(response2)
                    todo.extend([f for f in more_files if f not in todo])
        
        if not todo:
            todo = []
        
        self.log(f"[✓] Todo: {len(todo)} files to create")
        
        # Main loop
        self.log("[Step 2/3] Creating files...")
        
        while loop_count < max_loops and todo:
            loop_count += 1
            
            # Progress update every 5 loops
            if loop_count % 5 == 0:
                self.log(f"[Progress] {loop_count} loops done, {len(completed)} completed, {len(todo)} remaining")
            
            current = todo.pop(0)
            
            # If todo is empty, ask AI what to do
            if not current:
                status = f"Completed: {', '.join(completed[-5:])}" if completed else "Nothing yet"
                
                prompt = f"""Task: {task}
{status}
Files remaining in todo: {len(todo)}

What next? Reply with ONE of:
- CREATE: filename.php (create new file)
- DONE (task complete)
- TODO: file1.php, file2.php, file3.php (add more items)"""

                response = self.ask_ai(prompt, max_tokens=300)
                
                if response:
                    response = response.strip().upper()
                    
                    if 'DONE' in response and 'CONTINUE' not in response:
                        print(f"\n{Fore.GREEN}[✓] Task complete!{Style.RESET_ALL}")
                        break
                    
                    if 'TODO:' in response:
                        new_items = response.split('TODO:')[1].strip().split(',')
                        todo.extend([i.strip() for i in new_items if i.strip()])
                        print(f"{Fore.CYAN}Added {len(new_items)} more items (now {len(todo)} total){Style.RESET_ALL}")
                    
                    if 'CREATE:' in response:
                        filename = response.split('CREATE:')[1].strip()
                        current = filename
                    else:
                        continue
            
            # Extract filename
            if current.upper().startswith('CREATE:'):
                filename = current.split(':', 1)[1].strip()
            else:
                filename = current
            
            print(f"  [{loop_count}] {filename}")
            
            # Generate code with retry logic
            filepath = os.path.join(self.get_source_dir(), filename)
            exists = os.path.exists(filepath)
            
            code = None
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries and not code:
                if exists:
                    content = self.files.read(filepath)
                    prompt = f"""Task: {task}

Edit file: {filename}

Current content:
```
{content[:3000]}
```

Provide COMPLETE updated file. Output ONLY code block."""
                else:
                    prompt = f"""Task: {task}

Create new file: {filename}

Generate complete working code. Output ONLY code block."""
                
                response = self.ask_ai(prompt, max_tokens=2000)
                
                if response:
                    code = self.files.extract_code_from_response(response)
                
                if not code:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"    {Fore.YELLOW}Retry {retry_count}/{max_retries}...{Style.RESET_ALL}")
                        time.sleep(2)
                    else:
                        print(f"    {Fore.RED}[✗] Failed after {max_retries} retries{Style.RESET_ALL}")
                        errors += 1
            
            if not code:
                # Continue to next file on failure
                continue
            
            # Auto-save (YOLO mode is default)
            if self.files.write(filepath, code):
                self.log(f"[✓] Saved: {filename}")
                completed.append(filename)
            else:
                print(f"    {Fore.RED}[✗] Write failed{Style.RESET_ALL}")
                errors += 1
            
            # Save session every 10 files
            if len(completed) % 10 == 0:
                self.save_session(task, todo, completed, errors, loop_count)
            
            # Small delay between loops
            time.sleep(0.3)
        
        # Clear session on completion
        self.clear_session()
        
        # Calculate elapsed time
        elapsed = int(time.time() - start_time)
        hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
        elapsed_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Autonomous Agent Complete{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  End: {self.get_timestamp()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Duration: {elapsed_str}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Files created/edited: {len(completed)}{Style.RESET_ALL}")
        print(f"{Fore.RED}  Errors: {errors}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Total loops: {loop_count}{Style.RESET_ALL}")
        
        if completed:
            print(f"\n{Fore.GREEN}Completed files:{Style.RESET_ALL}")
            for f in completed:
                print(f"  - {f}")
        
        if loop_count >= max_loops:
            print(f"\n{Fore.YELLOW}Reached maximum loops ({max_loops}){Style.RESET_ALL}")
        
        return len(completed) > 0
    
    def extract_todo(self, response):
        """Extract todo list from AI response"""
        files = []
        
        for line in response.split('\n'):
            line = line.strip()
            line = re.sub(r'^\d+[.)]\s*', '', line)
            line = re.sub(r'^(File|file)[:\s]+', '', line)
            line = line.strip('-').strip()
            
            # Check for valid file extensions
            if any(line.endswith(ext) for ext in ['.php', '.py', '.go', '.js', '.html', '.css', '.sql', '.json', '.yaml', '.yml', '.txt']):
                # Remove any quotes or extra characters
                line = line.strip('"').strip("'")
                if line and '/' in line:
                    files.append(line)
        
        return files if files else []