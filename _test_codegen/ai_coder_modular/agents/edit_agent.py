"""
Edit Agent - Direct file editing like opencode
YOLO Mode: Automatic save without asking (default)
"""

from .base import BaseAgent
from colorama import Fore, Style
import os
import re


class EditAgent(BaseAgent):
    """Agent for editing single files"""
    
    def run(self, task, yolo_mode=None):
        """Execute edit task
        
        Args:
            task: The task description
            yolo_mode: None or True = auto-save (default). False = ask confirmation.
        """
        # Force YOLO by default
        if yolo_mode is None:
            yolo_mode = True
        
        if not self.ensure_source_dir():
            return False
        
        mode_str = f"{Fore.GREEN}YOLO (Auto-save){Style.RESET_ALL}" if yolo_mode else f"{Fore.YELLOW}Manual (Confirm){Style.RESET_ALL}"
        print(f"\n{Fore.CYAN}[Edit Agent] Mode: {mode_str}{Style.RESET_ALL}")
        
        task_lower = task.lower()
        is_create = any(word in task_lower for word in ['create', 'new file', 'add new', 'make new'])
        
        # Extract target file
        target_file = self.files.extract_filename_from_task(task)
        
        if not target_file:
            # Ask AI to find the file
            print(f"{Fore.CYAN}[Agent] Finding target file...{Style.RESET_ALL}")
            files = self.files.list_files()[:30]
            file_list = "\n".join([os.path.relpath(f, self.get_source_dir()) for f in files])
            
            prompt = f"""Task: {task}
            
Available files:
{file_list}

Which file to edit or create? Reply with just the filename."""
            
            response = self.ask_ai(prompt, max_tokens=200)
            if response:
                target_file = self.extract_filename_from_response(response)
        
        if not target_file:
            if is_create:
                target_file = input(f"{Fore.YELLOW}Enter filename: {Style.RESET_ALL}").strip()
                if not target_file:
                    print(f"{Fore.RED}[✗] No filename{Style.RESET_ALL}")
                    return False
                if '.' not in target_file:
                    target_file += '.php'
            else:
                print(f"{Fore.RED}[✗] Could not determine target file{Style.RESET_ALL}")
                return False
        
        filepath = os.path.join(self.get_source_dir(), target_file)
        file_exists = os.path.exists(filepath)
        
        if not file_exists and not is_create:
            print(f"{Fore.RED}[✗] File not found: {target_file}{Style.RESET_ALL}")
            return False
        
        if file_exists:
            print(f"{Fore.CYAN}[Agent] Editing: {target_file}{Style.RESET_ALL}")
            content = self.files.read(filepath)
            if not content:
                return False
            
            prompt = f"""Task: {task}

Current file ({target_file}):
```
{content[:4000]}
```

Provide COMPLETE updated file. Output ONLY code block.
If adding code, append to existing. If fixing, modify only what's needed."""
        else:
            print(f"{Fore.CYAN}[Agent] Creating: {target_file}{Style.RESET_ALL}")
            
            prompt = f"""Task: {task}

Create new file: {target_file}

Generate complete working code. Output ONLY code block."""
        
        response = self.ask_ai(prompt, max_tokens=2000)
        
        if not response:
            print(f"{Fore.RED}[✗] AI failed to generate code{Style.RESET_ALL}")
            return False
        
        new_code = self.files.extract_code_from_response(response)
        
        if not new_code:
            print(f"{Fore.RED}[✗] Could not extract code{Style.RESET_ALL}")
            return False
        
        # YOLO mode: ALWAYS auto-save (DEFAULT)
        if yolo_mode is not False:
            print(f"  {Fore.CYAN}[YOLO] Auto-saving...{Style.RESET_ALL}")
            confirm = 'y'
        else:
            print(f"\n{Fore.CYAN}Preview:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{new_code[:300]}...{Style.RESET_ALL}")
            confirm = input(f"\n{Fore.GREEN}Save? (y/n/s=skip/a=all): {Style.RESET_ALL}").strip().lower()
            
            if confirm == 'a':
                yolo_mode = True
                print(f"{Fore.GREEN}[YOLO] Switched to auto-save{Style.RESET_ALL}")
                confirm = 'y'
        
        if confirm == 's':
            new_name = target_file.replace('.php', '_new.php').replace('.py', '_new.py')
            filepath = os.path.join(self.get_source_dir(), new_name)
        
        if confirm in ['y', 's']:
            if self.files.write(filepath, new_code):
                action = "created" if not file_exists else "updated"
                print(f"{Fore.GREEN}[✓] File {action}: {target_file}{Style.RESET_ALL}")
                return True
        
        print(f"{Fore.YELLOW}Not saved{Style.RESET_ALL}")
        return False
    
    def extract_filename_from_response(self, response):
        """Extract filename from AI response"""
        patterns = [
            r'["\']([^"\']+\.(?:php|py|go|js|html|css|sql|json))["\']',
            r'(?:file|filename)[:\s]+([^\s]+\.(?:php|py|go|js|html|css|sql|json))',
            r'\b(\w+\.(?:php|py|go|js|html|css|sql|json))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None