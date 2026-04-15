"""
Configuration Module
Handles loading and saving configuration
"""

import os
import json
from colorama import Fore, Style

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ai_coder_config.json")

DEFAULT_CONFIG = {
    "llama_cpp": {
        "server_exe": "C:\\dev\\ai_setup_llama_cpp\\llama-cpp\\llama-server.exe",
        "cli_exe": "C:\\dev\\ai_setup_llama_cpp\\llama-cpp\\llama-cli.exe",
        "model_path": "C:\\dev\\ai_setup_llama_cpp\\llama-cpp\\models\\google_gemma-4-E2B-it-Q4_K_M.gguf",
        "server_host": "127.0.0.1",
        "server_port": 8080,
        "context_size": 4096,
        "threads": 4,
        "batch_size": 512
    },
    "source_code": {
        "default_directory": "",
        "recent_projects": [],
        "file_extensions": [".php", ".py", ".go", ".js", ".html", ".css", ".sql", ".json", ".xml", ".md"]
    },
    "languages": {
        "php": {"extensions": [".php"], "frameworks": ["CodeIgniter", "Laravel"], "style_guide": "PSR-12"},
        "python": {"extensions": [".py"], "frameworks": ["Flask", "FastAPI"], "style_guide": "PEP 8"},
        "go": {"extensions": [".go"], "frameworks": ["net/http"], "style_guide": "Effective Go"}
    },
    "ai_prompts": {
        "system_prompt": "You are an expert programmer. Help analyze and fix code.",
        "fix_code_prompt": "I have a {language} file with a problem. Please analyze and fix it.\n\nFile: {filename}\nProblem: {problem}\n\nCode:\n{code}",
        "review_prompt": "Please review this {language} code for bugs, security, and best practices.\n\nCode:\n{code}",
        "explain_prompt": "Please explain what this {language} code does:\n\n{code}",
        "write_prompt": "Write a {language} {type} that:\n{requirements}\n\nFollow {style_guide} conventions."
    },
    "batch_mode": {
        "delay_between_files": 5,
        "max_files_per_run": 50,
        "auto_save": True,
        "create_backup": True
    },
    "ai_code_gen": {
        "auto_save": False,
        "output_directory": "",
        "backup_on_overwrite": True
    }
}


class ConfigManager:
    def __init__(self):
        self.config = self.load()
    
    def load(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"{Fore.YELLOW}[WARN] Config load failed: {e}{Style.RESET_ALL}")
        
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to JSON file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}[✓] Configuration saved{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Config save failed: {e}{Style.RESET_ALL}")
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set config value"""
        self.config[key] = value