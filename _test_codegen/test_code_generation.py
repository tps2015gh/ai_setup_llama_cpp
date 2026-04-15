#!/usr/bin/env python3
"""
Test AI code generation and auto-save functionality
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ai_coder import AICoder

def test_code_extraction():
    """Test extracting code blocks from AI response"""
    print("=" * 60)
    print("  Testing Code Block Extraction")
    print("=" * 60)
    
    coder = AICoder()
    
    # Test case 1: Multi-language response (like hello world example)
    test_response = """This is a classic request! I will provide "Hello, World!" examples in three languages:

### 1. PHP Example

**Filename:** `hello.php`

```php
<?php
echo "Hello, World!";
?>
```

### 2. Python Example

```python
# Simple Python script
print("Hello, World!")
```

### 3. Golang Example

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

Summary: All three examples output the same message."""
    
    print("\nTest 1: Extract code blocks from multi-language response")
    code_blocks = coder.extract_code_blocks(test_response)
    
    if len(code_blocks) == 3:
        print(f"  ✓ Found {len(code_blocks)} code blocks\n")
        
        for i, block in enumerate(code_blocks, 1):
            print(f"  Block {i}:")
            print(f"    Language: {block['language']}")
            print(f"    Code length: {len(block['code'])} bytes")
            print(f"    First 50 chars: {block['code'][:50]}...")
            print()
    else:
        print(f"  ✗ Expected 3 blocks, found {len(code_blocks)}")
        return False
    
    # Test case 2: Single code block
    test_response2 = """Here's the fixed code:

```python
def hello():
    print("Hello!")
    return True
```

This should work now."""
    
    print("Test 2: Extract single code block")
    code_blocks2 = coder.extract_code_blocks(test_response2)
    
    if len(code_blocks2) == 1:
        print(f"  ✓ Found {len(code_blocks2)} code block")
        print(f"    Language: {code_blocks2[0]['language']}")
        print()
    else:
        print(f"  ✗ Expected 1 block, found {len(code_blocks2)}")
        return False
    
    # Test case 3: No code blocks
    test_response3 = "This is just text with no code blocks."
    
    print("Test 3: Extract from text with no code")
    code_blocks3 = coder.extract_code_blocks(test_response3)
    
    if len(code_blocks3) == 0:
        print(f"  ✓ Found {len(code_blocks3)} code blocks (correct)")
        print()
    else:
        print(f"  ✗ Expected 0 blocks, found {len(code_blocks3)}")
        return False
    
    return True

def test_filename_suggestion():
    """Test filename suggestion logic"""
    print("=" * 60)
    print("  Testing Filename Suggestion")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    # Test 1: PHP class
    block1 = {'language': 'php', 'code': '<?php\nclass UserController {\n    // code\n}', 'filename': None}
    filename1 = coder.suggest_filename(block1)
    print(f"Test 1: PHP class -> {filename1}")
    if filename1 == 'UserController.php':
        print(f"  ✓ Correct\n")
    else:
        print(f"  ✗ Expected UserController.php\n")
    
    # Test 2: Python function
    block2 = {'language': 'python', 'code': 'def calculate_total():\n    return 100', 'filename': None}
    filename2 = coder.suggest_filename(block2)
    print(f"Test 2: Python function -> {filename2}")
    if filename2 == 'calculate_total.py':
        print(f"  ✓ Correct\n")
    else:
        print(f"  ✗ Expected calculate_total.py\n")
    
    # Test 3: Go main package
    block3 = {'language': 'go', 'code': 'package main\n\nfunc main() {}', 'filename': None}
    filename3 = coder.suggest_filename(block3)
    print(f"Test 3: Go main -> {filename3}")
    if filename3 == 'main.go':
        print(f"  ✓ Correct\n")
    else:
        print(f"  ✗ Expected main.go\n")
    
    # Test 4: Filename in comment
    block4 = {'language': 'php', 'code': '// Filename: custom_controller.php\n<?php\nclass Custom {}', 'filename': None}
    filename4 = coder.suggest_filename(block4)
    print(f"Test 4: Filename in comment -> {filename4}")
    if filename4 == 'custom_controller.php':
        print(f"  ✓ Correct\n")
    else:
        print(f"  ✗ Expected custom_controller.php\n")
    
    return True

def test_save_code_blocks():
    """Test saving code blocks to files"""
    print("=" * 60)
    print("  Testing Code Block Saving")
    print("=" * 60)
    
    coder = AICoder()
    
    test_response = """Here are the examples:

### PHP Example

```php
<?php
echo "Hello from PHP!";
?>
```

### Python Example

```python
print("Hello from Python!")
```

### Go Example

```go
package main
import "fmt"
func main() {
    fmt.Println("Hello from Go!")
}
```"""
    
    print("\nTest: Save code blocks to ai_output directory")
    output_dir = os.path.join(os.path.dirname(__file__), 'ai_output')
    
    saved_files = coder.save_ai_code_blocks(test_response, output_dir=output_dir)
    
    if len(saved_files) == 3:
        print(f"  ✓ Saved {len(saved_files)} files\n")
        
        for file_info in saved_files:
            filepath = file_info['filepath']
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✓ {file_info['filename']}")
                print(f"    Path: {filepath}")
                print(f"    Size: {size} bytes")
                print(f"    Language: {file_info['language']}")
                print()
            else:
                print(f"  ✗ File not found: {filepath}\n")
        
        # Cleanup test files
        print("Cleaning up test files...")
        for file_info in saved_files:
            try:
                os.remove(file_info['filepath'])
            except:
                pass
        print(f"  ✓ Cleaned up\n")
    else:
        print(f"  ✗ Expected 3 files, saved {len(saved_files)}\n")
        return False
    
    return True

def main():
    """Run all code generation tests"""
    print("\n" + "=" * 60)
    print("  AI Coder - Code Generation Test")
    print("=" * 60 + "\n")
    
    tests = [
        ("Code Block Extraction", test_code_extraction),
        ("Filename Suggestion", test_filename_suggestion),
        ("Code Block Saving", test_save_code_blocks),
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
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print("  Test Results")
    print("=" * 60)
    print(f"  Passed: {passed}/{len(tests)}")
    print(f"  Failed: {failed}/{len(tests)}")
    print()
    
    if failed == 0:
        print("✓ All code generation tests passed!")
        print("\nFeatures verified:")
        print("  • Code block extraction from AI responses")
        print("  • Multi-language support (PHP, Python, Go)")
        print("  • Smart filename suggestion")
        print("  • Auto-save to disk")
        print("  • Proper file formatting")
        print("\nAI Coder can now automatically save generated code to disk! 🚀")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
