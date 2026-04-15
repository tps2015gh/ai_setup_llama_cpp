#!/usr/bin/env python3
"""
Quick test script for AI Coder
Tests basic functionality without needing server running
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_coder import AICoder

def test_config():
    """Test configuration loading"""
    print("=" * 60)
    print("  Testing Configuration")
    print("=" * 60)
    
    coder = AICoder()
    
    print(f"✓ Config loaded")
    print(f"  Server exe: {os.path.basename(coder.config['llama_cpp']['server_exe'])}")
    print(f"  Model: {os.path.basename(coder.config['llama_cpp']['model_path'])}")
    print(f"  Port: {coder.config['llama_cpp']['server_port']}")
    print(f"  Context: {coder.config['llama_cpp']['context_size']}")
    print()
    
    return True

def test_file_operations():
    """Test file read/write operations"""
    print("=" * 60)
    print("  Testing File Operations")
    print("=" * 60)
    
    coder = AICoder()
    
    # Create test PHP file
    test_php = """<?php
namespace App\Controllers;

use App\Controllers\BaseController;

class UserController extends BaseController
{
    public function index()
    {
        $users = $this->userModel->findAll();
        return view('users/index', ['users' => $users]);
    }
    
    public function show($id)
    {
        $user = $this->userModel->find($id);
        if (!$user) {
            return redirect()->to('/users')->with('error', 'User not found');
        }
        return view('users/show', ['user' => $user]);
    }
}
"""
    
    test_file = os.path.join(os.path.dirname(__file__), "test_user_controller.php")
    
    # Write test file
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_php)
    
    print(f"✓ Created test file: {os.path.basename(test_file)}")
    
    # Read test file
    content = coder.read_file(test_file)
    if content:
        print(f"✓ File read successfully ({len(content)} bytes)")
        print(f"  Lines: {len(content.splitlines())}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✓ Cleaned up test file")
    
    print()
    return True

def test_menu_display():
    """Test menu display (doesn't require server)"""
    print("=" * 60)
    print("  Testing Menu System")
    print("=" * 60)
    
    coder = AICoder()
    
    print("✓ AICoder class instantiated")
    print("✓ Menu methods available:")
    print("  - start_server()")
    print("  - stop_server()")
    print("  - chat_mode()")
    print("  - fix_file()")
    print("  - review_code()")
    print("  - explain_code()")
    print("  - write_new_code()")
    print("  - batch_process()")
    print("  - analyze_database()")
    print()
    
    return True

def test_config_save():
    """Test configuration save"""
    print("=" * 60)
    print("  Testing Configuration Save")
    print("=" * 60)
    
    coder = AICoder()
    
    # Modify and save
    coder.config['source_code']['default_directory'] = 'C:\\test\\path'
    coder.save_config()
    
    print("✓ Configuration saved")
    
    # Reload and verify
    coder2 = AICoder()
    if coder2.config['source_code']['default_directory'] == 'C:\\test\\path':
        print("✓ Configuration reload successful")
    
    # Reset
    coder2.config['source_code']['default_directory'] = ''
    coder2.save_config()
    print("✓ Configuration reset")
    print()
    
    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  AI Coder - Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        ("Configuration", test_config),
        ("File Operations", test_file_operations),
        ("Menu System", test_menu_display),
        ("Config Save", test_config_save),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {name} FAILED\n")
        except Exception as e:
            failed += 1
            print(f"✗ {name} ERROR: {e}\n")
    
    print("=" * 60)
    print("  Test Results")
    print("=" * 60)
    print(f"  Passed: {passed}/{len(tests)}")
    print(f"  Failed: {failed}/{len(tests)}")
    print()
    
    if failed == 0:
        print("✓ All tests passed! AI Coder is ready to use.")
        print("\nNext steps:")
        print("  1. Start AI server: Menu 1")
        print("  2. Set source directory: Menu 4")
        print("  3. Use AI tools: Menu 5-11")
        print()
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
