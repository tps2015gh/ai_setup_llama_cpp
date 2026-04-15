"""
Multi-File Agent - Creates/edits multiple files at once
YOLO Mode: Automatic save without asking (default)
"""

from .base import BaseAgent
from .edit_agent import EditAgent
from colorama import Fore, Style
import os
import re


class MultiFileAgent(BaseAgent):
    """Agent for creating/editing multiple files"""
    
    def run(self, task, yolo_mode=None):
        """Execute multi-file task
        
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
        print(f"\n{Fore.CYAN}[Agent] Mode: {mode_str}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[Agent] Analyzing task...{Style.RESET_ALL}")
        
        # Get project files
        files = self.files.list_files()
        file_list = "\n".join([os.path.relpath(f, self.get_source_dir()) for f in files[:50]])
        
        # Ask AI for file plan
        prompt = f"""Task: {task}

Project files:
{file_list}

List all files that need to be created or modified. One per line.
Example:
controllers/User.php
models/User_model.php
views/user_list.php"""

        response = self.ask_ai(prompt, max_tokens=1000)
        
        if not response:
            print(f"{Fore.RED}[✗] AI failed to plan{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.CYAN}Task Plan:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{response[:500]}...{Style.RESET_ALL}\n")
        
        # Extract file list
        files_to_create = self.extract_file_list(response)
        
        if not files_to_create:
            print(f"{Fore.RED}[✗] Could not determine files{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.YELLOW}Files to create: {len(files_to_create)}{Style.RESET_ALL}")
        for f in files_to_create:
            print(f"  - {f}")
        
        # YOLO mode skips confirmation
        if not yolo_mode:
            confirm = input(f"\n{Fore.GREEN}Create files? (y/n/a=all): {Style.RESET_ALL}").strip().lower()
            
            if confirm == 'a':
                yolo_mode = True
                print(f"{Fore.GREEN}[YOLO] Auto-save enabled{Style.RESET_ALL}")
            
            if confirm not in ['y', 'a']:
                print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")
                return False
        
        # Generate all files at once
        print(f"\n{Fore.CYAN}[Agent] Generating code...{Style.RESET_ALL}")
        
        prompt = f"""Task: {task}

Create these files:
{chr(10).join('- ' + f for f in files_to_create)}

For each file provide complete code in code block format:
FILE: path/to/file.php
```php
// code
```

FILE: views/test.php
```php
// code
```"""
        
        response = self.ask_ai(prompt, max_tokens=3000)
        
        if not response:
            print(f"{Fore.RED}[✗] AI failed to generate code{Style.RESET_ALL}")
            return False
        
        # Save each file
        print(f"\n{Fore.CYAN}[Agent] Saving files...{Style.RESET_ALL}")
        
        saved = self.save_files_from_response(response, files_to_create, yolo_mode=yolo_mode)
        
        print(f"\n{Fore.GREEN}[✓] Created {len(saved)} file(s){Style.RESET_ALL}")
        for f in saved:
            print(f"  - {f}")
        
        return len(saved) > 0
    
    def extract_file_list(self, response):
        """Extract file list from AI response"""
        files = []
        
        for line in response.split('\n'):
            line = line.strip().strip('-').strip()
            line = re.sub(r'^\d+[.)]\s*', '', line)
            line = re.sub(r'^(File|file)[:\s]+', '', line)
            
            if any(line.endswith(ext) for ext in ['.php', '.py', '.go', '.js', '.html', '.css', '.sql', '.json']):
                files.append(line)
        
        return files[:20]
    
    def save_files_from_response(self, response, expected_files, yolo_mode=True):
        """Extract and save multiple files from AI response"""
        saved = []
        
        # Try to find FILE: markers
        sections = re.split(r'(?:FILE|File)[:\s]+', response)
        
        if len(sections) > 1:
            for i, section in enumerate(sections[1:], 0):
                if i < len(expected_files):
                    filename = expected_files[i]
                    code = self.files.extract_code_from_response(section)
                    if code:
                        filepath = os.path.join(self.get_source_dir(), filename)
                        if yolo_mode is not False:
                            # YOLO: auto-save (DEFAULT)
                            if self.files.write(filepath, code):
                                print(f"  {Fore.GREEN}[YOLO] Saved: {filename}{Style.RESET_ALL}")
                                saved.append(filename)
                        else:
                            # Manual: show preview and ask
                            print(f"\n  File: {filename}")
                            print(f"  Preview: {code[:200]}...")
                            confirm = input(f"    {Fore.GREEN}Save? (y/n/a=all): {Style.RESET_ALL}").strip().lower()
                            if confirm == 'a':
                                yolo_mode = True
                            if confirm in ['y', 'a'] and self.files.write(filepath, code):
                                saved.append(filename)
                                print(f"    {Fore.GREEN}[✓] Saved{Style.RESET_ALL}")
        else:
            # Try matching by filename in content
            for filename in expected_files:
                pattern = rf'{re.escape(filename)}.*?(?:```|$)'
                match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if match:
                    code = self.files.extract_code_from_response(match.group(0))
                    if code:
                        filepath = os.path.join(self.get_source_dir(), filename)
                        if yolo_mode is not False:
                            # YOLO: auto-save (DEFAULT)
                            if self.files.write(filepath, code):
                                print(f"  {Fore.GREEN}[YOLO] Saved: {filename}{Style.RESET_ALL}")
                                saved.append(filename)
                        else:
                            # Manual: show preview and ask
                            print(f"\n  File: {filename}")
                            print(f"  Preview: {code[:200]}...")
                            confirm = input(f"    {Fore.GREEN}Save? (y/n): {Style.RESET_ALL}").strip().lower()
                            if confirm == 'y' and self.files.write(filepath, code):
                                saved.append(filename)
        
        return saved