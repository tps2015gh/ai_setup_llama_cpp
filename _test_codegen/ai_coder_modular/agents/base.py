"""
Agent Base Class
Base class for all AI agents
"""

from colorama import Fore, Style
import os


class BaseAgent:
    def __init__(self, ai_server, file_manager, config):
        self.ai = ai_server
        self.files = file_manager
        self.config = config
    
    def run(self, task):
        """Override this in subclasses"""
        raise NotImplementedError
    
    def ask_ai(self, prompt, max_tokens=1024):
        """Ask AI and return response"""
        return self.ai.ask(prompt, max_tokens=max_tokens)
    
    def get_source_dir(self):
        """Get source directory"""
        return self.files.source_dir
    
    def set_source_dir(self, directory):
        """Set source directory"""
        self.files.set_source_dir(directory)
    
    def ensure_source_dir(self):
        """Ensure source directory is set"""
        if not self.get_source_dir():
            print(f"{Fore.RED}[✗] Source directory not set{Style.RESET_ALL}")
            return False
        return True