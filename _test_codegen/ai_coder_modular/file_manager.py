"""
File Manager Module
Handles file operations - read, write, list
"""

import os
import glob
import shutil
from datetime import datetime
from colorama import Fore, Style


class FileManager:
    def __init__(self, config):
        self.config = config
        self.source_dir = config.get('source_code', {}).get('default_directory', '')
    
    def set_source_dir(self, directory):
        """Set the source directory"""
        self.source_dir = directory
    
    def read(self, filepath):
        """Read file content"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"{Fore.RED}[✗] Read failed: {e}{Style.RESET_ALL}")
            return None
    
    def write(self, filepath, content):
        """Write content to file, create directories if needed"""
        try:
            # Create full directory path if it doesn't exist
            directory = os.path.dirname(filepath)
            if directory:
                # Normalize path separators for Windows
                directory = os.path.normpath(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    # Show relative path from source directory
                    src_dir = self.source_dir or os.getcwd()
                    try:
                        rel_path = os.path.relpath(directory, src_dir)
                        if rel_path == '.':
                            rel_path = os.path.basename(directory)
                        print(f"{Fore.CYAN}[✓] Created directory: {rel_path}{Style.RESET_ALL}")
                    except:
                        print(f"{Fore.CYAN}[✓] Created directory: {os.path.basename(directory)}{Style.RESET_ALL}")
            
            # Create backup if enabled
            if self.config.get('batch_mode', {}).get('create_backup', True):
                if os.path.exists(filepath):
                    backup_path = filepath + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    shutil.copy2(filepath, backup_path)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            # Show relative path from source directory
            src_dir = self.source_dir or os.getcwd()
            try:
                rel_path = os.path.relpath(filepath, src_dir)
                print(f"{Fore.GREEN}[✓] Saved: {rel_path}{Style.RESET_ALL}")
            except:
                print(f"{Fore.GREEN}[✓] Saved: {os.path.basename(filepath)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Write failed: {e}{Style.RESET_ALL}")
            return False
    
    def list_files(self, directory=None, extensions=None):
        """List all source files in directory"""
        if directory is None:
            directory = self.source_dir
        
        if not directory or not os.path.exists(directory):
            return []
        
        if extensions is None:
            extensions = self.config.get('source_code', {}).get('file_extensions', ['.php'])
        
        files = []
        for ext in extensions:
            pattern = os.path.join(directory, f"**/*{ext}")
            files.extend(glob.glob(pattern, recursive=True))
        
        return sorted(files)
    
    def detect_language(self, filepath):
        """Detect programming language from file extension"""
        ext = os.path.splitext(filepath)[1].lower()
        
        lang_map = {
            '.php': 'PHP',
            '.py': 'Python',
            '.go': 'Go',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.sql': 'SQL'
        }
        
        return lang_map.get(ext, 'Unknown')
    
    def extract_code_from_response(self, response):
        """Extract code block from AI response"""
        import re
        
        if '```' in response:
            parts = response.split('```')
            if len(parts) >= 3:
                code = parts[1]
                lines = code.split('\n', 1)
                if lines[0].strip() in ['php', 'python', 'py', 'go', 'js', 'html', 'css', 'sql', 'json']:
                    code = lines[1] if len(lines) > 1 else code
                return code.strip()
        
        if len(response) > 50 and ('function' in response.lower() or 'class' in response.lower() or 'def ' in response):
            return response.strip()
        
        return None
    
    def extract_filename_from_task(self, task):
        """Extract filename from task text"""
        import re
        
        patterns = [
            r'\b(?:in|to|from|at|file)\s+([^\s]+\.(?:php|py|go|js|html|css|sql|json))',
            r'([^\s]+\.(?:php|py|go|js|html|css|sql|json))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, task, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None