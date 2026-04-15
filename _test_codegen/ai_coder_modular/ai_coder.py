#!/usr/bin/env python3
"""
AI Coder - Modular Agentic Code Editor
Version: 2.0.0
Uses local llama.cpp + Gemma 4 for offline AI-assisted coding
"""

__version__ = "2.0.0"
__author__ = "AI Coder Team"

import os
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Version info
print(f"{Fore.CYAN}AI Coder v{__version__} - Modular Agentic Editor{Style.RESET_ALL}")

# Add modular path
MODULAR_DIR = os.path.dirname(__file__)
sys.path.insert(0, MODULAR_DIR)

from config import ConfigManager
from ai_server import AIServer
from file_manager import FileManager
from agents.edit_agent import EditAgent
from agents.multifile_agent import MultiFileAgent
from agents.autonomous_agent import AutonomousAgent
from agents.chat_agent import ChatAgent


class AICoder:
    """Main AI Coder application"""
    
    def __init__(self):
        # Initialize modules
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        
        self.ai_server = AIServer(self.config)
        self.file_manager = FileManager(self.config)
        
        # Set source directory
        self.file_manager.set_source_dir(
            self.config.get('source_code', {}).get('default_directory', '')
        )
        
        # Initialize agents
        self.agents = {
            'edit': EditAgent(self.ai_server, self.file_manager, self.config),
            'multifile': MultiFileAgent(self.ai_server, self.file_manager, self.config),
            'autonomous': AutonomousAgent(self.ai_server, self.file_manager, self.config),
            'chat': ChatAgent(self.ai_server, self.file_manager, self.config),
        }
        
        # Default YOLO mode (auto-save without asking)
        self.yolo_mode = True
    
    def start_server(self):
        """Start AI server"""
        if self.ai_server.start():
            print(f"{Fore.GREEN}[✓] Server running on port {self.config.get('llama_cpp', {}).get('server_port', 8080)}{Style.RESET_ALL}")
    
    def stop_server(self):
        """Stop AI server"""
        self.ai_server.stop()
    
    def check_server_status(self):
        """Check server status"""
        status = self.ai_server.status()
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Server Status{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        if status['running']:
            print(f"{Fore.GREEN}  Status: Running ✓{Style.RESET_ALL}")
            print(f"{Fore.GREEN}  API:    Responsive ✓{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}  Status: Not running ✗{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}  Port:   {status['port']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Model:  {status['model']}{Style.RESET_ALL}")
        print()
    
    def set_source_directory(self):
        """Set source code directory"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Set Source Directory{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        current = self.file_manager.source_dir or "(not set)"
        print(f"{Fore.YELLOW}Current: {current}{Style.RESET_ALL}\n")
        
        new_dir = input(f"{Fore.GREEN}Enter path: {Style.RESET_ALL}").strip()
        
        if not new_dir:
            print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")
            return
        
        if not os.path.exists(new_dir):
            print(f"{Fore.RED}[✗] Directory not found: {new_dir}{Style.RESET_ALL}")
            return
        
        # Update config
        self.file_manager.set_source_dir(new_dir)
        self.config['source_code']['default_directory'] = new_dir
        self.config_manager.save()
        
        # Show files
        files = self.file_manager.list_files()
        print(f"{Fore.GREEN}[✓] Source set: {new_dir}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}    Found {len(files)} files{Style.RESET_ALL}")
    
    def run_agent(self, agent_name, task=None, yolo_mode=None):
        """Run an agent
        
        Args:
            agent_name: Name of agent to run
            task: Task description (not needed for chat)
            yolo_mode: None or True = auto-save (default). False = manual confirm.
        """
        agent = self.agents.get(agent_name)
        
        if not agent:
            print(f"{Fore.RED}[✗] Unknown agent: {agent_name}{Style.RESET_ALL}")
            return
        
        if agent_name == 'chat':
            agent.run()
        else:
            if not task:
                task = input(f"{Fore.GREEN}Task: {Style.RESET_ALL}").strip()
            if task:
                # Use yolo_mode from self.yolo_mode (True/False), not None
                agent.run(task, yolo_mode=self.yolo_mode)
    
    def show_menu(self):
        """Display main menu"""
        server_status = f"{Fore.GREEN}Running{Style.RESET_ALL}" if self.ai_server.running else f"{Fore.RED}Stopped{Style.RESET_ALL}"
        source_status = self.file_manager.source_dir or f"{Fore.RED}Not set{Style.RESET_ALL}"
        
        mode_display = f"{Fore.GREEN}YOLO (Auto-save){Style.RESET_ALL}" if self.yolo_mode else f"{Fore.YELLOW}Manual (Confirm){Style.RESET_ALL}"
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  AI Coder - Modular Agentic Editor{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Powered by llama.cpp + Gemma 4{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Server: {server_status}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Source: {source_status}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mode:   {mode_display}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Server:{Style.RESET_ALL}")
        print(f"  1. Start Server")
        print(f"  2. Stop Server")
        print(f"  3. Check Status")
        print(f"  4. Set Source Directory")
        print()
        
        print(f"{Fore.CYAN}Agents (YOLO = auto-save):{Style.RESET_ALL}")
        print(f"  5. Chat Agent (interactive)")
        print(f"  6. Edit Agent (single file)")
        print(f"  7. Multi-File Agent")
        print(f"  8. Autonomous Agent (loop until done)")
        print()
        
        print(f"{Fore.CYAN}Settings:{Style.RESET_ALL}")
        print(f"  9. Toggle YOLO/Manual mode")
        print(f"  0. Exit")
        print()
    
    def run(self):
        """Main loop"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Welcome to AI Coder{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        while True:
            try:
                self.show_menu()
                choice = input(f"{Fore.GREEN}Select [0-9]: {Style.RESET_ALL}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
                    break
                
                elif choice == '1':
                    self.start_server()
                
                elif choice == '2':
                    self.stop_server()
                
                elif choice == '3':
                    self.check_server_status()
                
                elif choice == '4':
                    self.set_source_directory()
                
                elif choice == '5':
                    self.run_agent('chat')
                
                elif choice == '6':
                    self.run_agent('edit', yolo_mode=self.yolo_mode)
                
                elif choice == '7':
                    self.run_agent('multifile', yolo_mode=self.yolo_mode)
                
                elif choice == '8':
                    self.run_agent('autonomous', yolo_mode=self.yolo_mode)
                
                elif choice == '9':
                    self.yolo_mode = not self.yolo_mode
                    mode = f"{Fore.GREEN}YOLO (Auto-save){Style.RESET_ALL}" if self.yolo_mode else f"{Fore.YELLOW}Manual (Confirm){Style.RESET_ALL}"
                    print(f"\n{Fore.GREEN}[✓] Mode switched to: {mode}{Style.RESET_ALL}")
                
                else:
                    print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
                
                if choice != '0':
                    input(f"\n{Fore.YELLOW}Press Enter...{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Interrupted{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    app = AICoder()
    app.run()