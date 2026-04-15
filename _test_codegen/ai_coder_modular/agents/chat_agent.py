"""
Chat Agent - Interactive chat with AI
"""

from .base import BaseAgent
from colorama import Fore, Style


class ChatAgent(BaseAgent):
    """Interactive chat with AI"""
    
    def run(self, task=None):
        """Start chat loop"""
        if not self.ensure_source_dir():
            return False
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  AI Chat Mode{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Type questions about your code{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit' to quit\n{Style.RESET_ALL}")
        
        while True:
            try:
                question = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    break
                
                response = self.ask_ai(question, max_tokens=1500)
                
                if response:
                    print(f"\n{Fore.CYAN}AI: {Style.RESET_ALL}")
                    print(f"{Fore.WHITE}{response}{Style.RESET_ALL}\n")
                    
                    # Auto-save code blocks
                    self.auto_save_code(response, question)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Chat ended{Style.RESET_ALL}")
        return True
    
    def auto_save_code(self, response, question):
        """Auto-save code blocks from AI response"""
        code_blocks = self.extract_code_blocks(response)
        
        if not code_blocks:
            return
        
        output_dir = self.config.get('ai_code_gen', {}).get('output_directory', '')
        
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'ai_output')
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for i, code in enumerate(code_blocks, 1):
            ext = self.guess_extension(code)
            filename = f"generated_{i}{ext}"
            filepath = os.path.join(output_dir, filename)
            
            if self.files.write(filepath, code):
                print(f"{Fore.CYAN}[Auto-saved] {filename}{Style.RESET_ALL}")
    
    def extract_code_blocks(self, response):
        """Extract code blocks from response"""
        import re
        
        blocks = []
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for lang, code in matches:
            if code.strip():
                blocks.append(code.strip())
        
        return blocks
    
    def guess_extension(self, code):
        """Guess file extension from code"""
        if '<?php' in code:
            return '.php'
        if 'def ' in code or 'import ' in code:
            return '.py'
        if 'func ' in code or 'package ' in code:
            return '.go'
        if '<html' in code.lower() or '<!DOCTYPE' in code:
            return '.html'
        return '.txt'


import os