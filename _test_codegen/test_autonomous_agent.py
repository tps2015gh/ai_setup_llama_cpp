#!/usr/bin/env python3
"""
Test script for Autonomous Agent (Menu 8)
Tests the complete CRUD system generation
"""

import os
import sys

# Add modular path
MODULAR_DIR = os.path.join(os.path.dirname(__file__), 'ai_coder_modular')
sys.path.insert(0, MODULAR_DIR)

from config import ConfigManager
from ai_server import AIServer
from file_manager import FileManager
from agents.autonomous_agent import AutonomousAgent

def main():
    print("=" * 60)
    print("  Testing Autonomous Agent")
    print("=" * 60)
    
    # Initialize
    config_manager = ConfigManager()
    config = config_manager.config
    
    ai_server = AIServer(config)
    file_manager = FileManager(config)
    
    # Set source directory
    test_dir = r"C:\dev\ai_local_webapp_php"
    if not os.path.exists(test_dir):
        print(f"[!] Test directory not found: {test_dir}")
        print("[!] Using current directory instead")
        test_dir = os.getcwd()
    
    file_manager.set_source_dir(test_dir)
    
    # Check server
    print(f"\n[1] Checking server status...")
    if not ai_server.test():
        print("[!] Server not running. Starting...")
        if ai_server.start():
            print("[✓] Server started")
        else:
            print("[✗] Failed to start server")
            return
    else:
        print("[✓] Server already running")
    
    # Create agent
    agent = AutonomousAgent(ai_server, file_manager, config)
    
    # Run task
    task = "create a complete CRUD system for user management"
    print(f"\n[2] Running task: {task}")
    print(f"[2] Source directory: {test_dir}\n")
    
    # Run with YOLO mode
    result = agent.run(task, yolo_mode=True)
    
    print("\n" + "=" * 60)
    if result:
        print("[✓] Test completed successfully")
    else:
        print("[✗] Test failed")
    print("=" * 60)

if __name__ == "__main__":
    main()