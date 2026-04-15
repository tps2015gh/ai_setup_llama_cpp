"""
AI Server Module
Manages llama.cpp server for local AI
"""

import os
import time
import subprocess
import requests
from colorama import Fore, Style


class AIServer:
    def __init__(self, config):
        self.config = config
        self.process = None
        self.running = False
    
    def get_llama_config(self):
        """Get llama.cpp configuration"""
        return self.config.get('llama_cpp', {})
    
    def start(self):
        """Start llama-server in background"""
        if self.running:
            port = self.get_llama_config().get('server_port', 8080)
            print(f"{Fore.YELLOW}[!] Server already running on port {port}{Style.RESET_ALL}")
            return True
        
        llm_config = self.get_llama_config()
        server_exe = llm_config.get('server_exe', '')
        model_path = llm_config.get('model_path', '')
        port = llm_config.get('server_port', 8080)
        context = llm_config.get('context_size', 4096)
        threads = llm_config.get('threads', 4)
        batch = llm_config.get('batch_size', 512)
        
        if not os.path.exists(server_exe):
            print(f"{Fore.RED}[✗] Server not found: {server_exe}{Style.RESET_ALL}")
            return False
        
        if not os.path.exists(model_path):
            print(f"{Fore.RED}[✗] Model not found: {model_path}{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.CYAN}[▶] Starting AI server...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Model: {os.path.basename(model_path)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Port: {port}{Style.RESET_ALL}")
        
        try:
            cmd = [
                server_exe,
                "-m", model_path,
                "-c", str(context),
                "-t", str(threads),
                "-b", str(batch),
                "--port", str(port),
                "--host", llm_config.get('server_host', '127.0.0.1')
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for server to be ready
            print(f"{Fore.CYAN}    Waiting for server...{Style.RESET_ALL}")
            max_wait = 60
            waited = 0
            while waited < max_wait:
                if self.test():
                    self.running = True
                    print(f"{Fore.GREEN}[✓] Server started!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}    API: http://127.0.0.1:{port}/v1{Style.RESET_ALL}")
                    return True
                time.sleep(2)
                waited += 2
            
            print(f"{Fore.RED}[✗] Server startup timeout{Style.RESET_ALL}")
            self.process.kill()
            return False
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Server start failed: {e}{Style.RESET_ALL}")
            return False
    
    def stop(self):
        """Stop llama-server"""
        if not self.running or not self.process:
            print(f"{Fore.YELLOW}[!] Server not running{Style.RESET_ALL}")
            return True
        
        print(f"{Fore.CYAN}[■] Stopping AI server...{Style.RESET_ALL}")
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.running = False
            print(f"{Fore.GREEN}[✓] Server stopped{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Server stop failed: {e}{Style.RESET_ALL}")
            try:
                self.process.kill()
                self.running = False
                return True
            except:
                return False
    
    def test(self):
        """Test if server is responding"""
        try:
            port = self.get_llama_config().get('server_port', 8080)
            response = requests.get(f"http://127.0.0.1:{port}/v1/models", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def status(self):
        """Get server status"""
        port = self.get_llama_config().get('server_port', 8080)
        
        status = {
            'running': self.running,
            'process_alive': self.process.poll() is None if self.process else False,
            'api_responsive': self.test(),
            'port': port,
            'model': os.path.basename(self.get_llama_config().get('model_path', 'Unknown'))
        }
        
        if status['process_alive'] and status['api_responsive']:
            self.running = True
        else:
            self.running = False
        
        return status
    
    def ask(self, prompt, system_prompt=None, max_tokens=1024):
        """Send prompt to AI and get response"""
        if not self.running:
            if not self.test():
                print(f"{Fore.RED}[✗] AI server not running{Style.RESET_ALL}")
                return None
        
        port = self.get_llama_config().get('server_port', 8080)
        url = f"http://127.0.0.1:{port}/v1/chat/completions"
        
        if system_prompt is None:
            system_prompt = self.config.get('ai_prompts', {}).get('system_prompt', 
                "You are an expert programmer.")
        
        payload = {
            "model": "gemma-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
        
        try:
            print(f"{Fore.CYAN}[AI] Thinking...{Style.RESET_ALL}")
            # Increase timeout for longer operations
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"{Fore.RED}[✗] AI error: {response.status_code}{Style.RESET_ALL}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[✗] Request timeout{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[✗] Request failed: {e}{Style.RESET_ALL}")
            return None