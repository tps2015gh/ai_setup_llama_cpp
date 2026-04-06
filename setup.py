#!/usr/bin/env python3
"""
llama.cpp Setup Script for Windows
Downloads and installs llama.cpp + Gemma 4 model
"""

import os
import sys
import urllib.request
import zipfile
import subprocess
import shutil

LLAMA_VERSION = "b8676"
LLAMA_URL = f"https://github.com/ggml-org/llama.cpp/releases/download/{LLAMA_VERSION}/llama-{LLAMA_VERSION}-bin-win-cpu-x64.zip"
MODEL_URL = "https://huggingface.co/bartowski/google_gemma-4-E2B-it-GGUF/resolve/main/google_gemma-4-E2B-it-Q4_K_M.gguf"
MODEL_NAME = "google_gemma-4-E2B-it-Q4_K_M.gguf"

def print_header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")

def print_step(text):
    print(f"  [>] {text}")

def print_ok(text):
    print(f"  [✓] {text}")

def print_err(text):
    print(f"  [✗] {text}")

def download_file(url, dest):
    def report(block, blocksize, total):
        if total > 0:
            pct = min(100, int(block * blocksize * 100 / total))
            done = int(pct / 2)
            print(f"\r  [{'#' * done}{'.' * (50-done)}] {pct}%", end="", flush=True)
    print_step(f"Downloading from {url}")
    urllib.request.urlretrieve(url, dest, report)
    print()

def install_llama_cpp():
    print_header("Installing llama.cpp")
    
    llama_dir = os.path.join(os.getcwd(), "llama-cpp")
    os.makedirs(llama_dir, exist_ok=True)
    
    zip_path = os.path.join(llama_dir, "llama.zip")
    
    if os.path.exists(os.path.join(llama_dir, "llama-cli.exe")):
        print_ok("llama.cpp already installed")
        return True
    
    try:
        download_file(LLAMA_URL, zip_path)
        
        print_step("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(llama_dir)
        
        os.remove(zip_path)
        
        if os.path.exists(os.path.join(llama_dir, "llama-cli.exe")):
            print_ok(f"llama.cpp {LLAMA_VERSION} installed successfully")
            return True
        else:
            print_err("Installation failed - llama-cli.exe not found")
            return False
    except Exception as e:
        print_err(f"Failed: {e}")
        return False

def download_model():
    print_header("Downloading Gemma 4 E2B Model")
    
    models_dir = os.path.join(os.getcwd(), "llama-cpp", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, MODEL_NAME)
    
    if os.path.exists(model_path) and os.path.getsize(model_path) > 1_000_000_000:
        size_gb = os.path.getsize(model_path) / (1024**3)
        print_ok(f"Model already exists ({size_gb:.1f}GB)")
        return True
    
    try:
        download_file(MODEL_URL, model_path)
        
        size_gb = os.path.getsize(model_path) / (1024**3)
        print_ok(f"Model downloaded ({size_gb:.1f}GB)")
        return True
    except Exception as e:
        print_err(f"Failed: {e}")
        return False

def test_model():
    print_header("Testing Gemma 4")
    
    llama_cli = os.path.join(os.getcwd(), "llama-cpp", "llama-cli.exe")
    model_path = os.path.join(os.getcwd(), "llama-cpp", "models", MODEL_NAME)
    
    if not os.path.exists(llama_cli):
        print_err("llama.cpp not installed. Run option 1 first.")
        return False
    
    if not os.path.exists(model_path):
        print_err("Model not found. Run option 2 first.")
        return False
    
    print_step("Running quick test...")
    result = subprocess.run(
        [llama_cli, "-m", model_path, "-p", "Say hello in 3 words", "-n", "20"],
        capture_output=True, text=True, timeout=120
    )
    
    if result.returncode == 0:
        output = result.stdout.split(">")[-1].strip() if ">" in result.stdout else result.stdout[-200:]
        print_ok("Test passed!")
        print(f"  Response: {output[:100]}")
        return True
    else:
        print_err("Test failed")
        print(result.stderr[-200:] if result.stderr else "Unknown error")
        return False

def remove_ollama():
    print_header("Removing Ollama")
    
    ollama_paths = [
        r"C:\Users\admin\AppData\Local\Programs\Ollama",
        os.path.expanduser("~\\.ollama"),
    ]
    
    found = False
    for path in ollama_paths:
        if os.path.exists(path):
            found = True
            print_step(f"Removing {path}")
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
                print_ok(f"Removed {path}")
            except Exception as e:
                print_err(f"Failed to remove {path}: {e}")
    
    if not found:
        print_ok("Ollama not found, nothing to remove")
    
    return True

def show_status():
    print_header("System Status")
    
    llama_cli = os.path.join(os.getcwd(), "llama-cpp", "llama-cli.exe")
    model_path = os.path.join(os.getcwd(), "llama-cpp", "models", MODEL_NAME)
    
    print(f"  llama.cpp:  {'✓ Installed' if os.path.exists(llama_cli) else '✗ Not installed'}")
    
    if os.path.exists(model_path):
        size_gb = os.path.getsize(model_path) / (1024**3)
        print(f"  Gemma 4:    ✓ Installed ({size_gb:.1f}GB)")
    else:
        print(f"  Gemma 4:    ✗ Not installed")
    
    disk = shutil.disk_usage(os.getcwd())
    print(f"  Disk free:  {disk.free / (1024**3):.1f}GB")
    
    try:
        ram_bytes = int(subprocess.check_output('wmic memorychip get capacity', shell=True).decode().strip().split('\n')[-1])
        print(f"  RAM:        {ram_bytes / (1024**3):.0f}GB")
    except:
        print(f"  RAM:        unknown")

def main_menu():
    while True:
        print_header("llama.cpp Setup Menu")
        print("  1. Install llama.cpp")
        print("  2. Download Gemma 4 E2B model")
        print("  3. Remove Ollama (free space)")
        print("  4. Test installation")
        print("  5. Show status")
        print("  6. Install all (1+2+4)")
        print("  0. Exit")
        print()
        
        choice = input("  Select [0-6]: ").strip()
        
        actions = {
            "1": install_llama_cpp,
            "2": download_model,
            "3": remove_ollama,
            "4": test_model,
            "5": show_status,
            "6": lambda: install_llama_cpp() and download_model() and test_model(),
            "0": lambda: (print("\n  Bye!"), sys.exit(0)),
        }
        
        action = actions.get(choice)
        if action:
            action()
            input("\n  Press Enter to continue...")
        else:
            print("  Invalid option")

if __name__ == "__main__":
    main_menu()
