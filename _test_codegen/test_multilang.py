#!/usr/bin/env python3
"""
Test multi-language detection in AI Coder
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ai_coder import AICoder

def test_language_detection():
    """Test language detection from file extensions"""
    print("=" * 60)
    print("  Testing Language Detection")
    print("=" * 60)
    
    coder = AICoder()
    
    test_cases = [
        ("test.php", "PHP"),
        ("test.py", "Python"),
        ("test.go", "Go"),
        ("controller.php", "PHP"),
        ("app.py", "Python"),
        ("main.go", "Go"),
        ("test.js", "JavaScript"),
        ("page.html", "HTML"),
        ("style.css", "CSS"),
        ("query.sql", "SQL"),
        ("unknown.xyz", "Unknown"),
    ]
    
    print()
    all_passed = True
    
    for filename, expected in test_cases:
        result = coder.detect_language(filename)
        status = "✓" if result == expected else "✗"
        
        if result != expected:
            all_passed = False
        
        print(f"  {status} {filename:20} -> {result:15} (expected: {expected})")
    
    print()
    return all_passed

def test_language_config():
    """Test language-specific configuration retrieval"""
    print("=" * 60)
    print("  Testing Language Configuration")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    # Test PHP config
    php_config = coder.get_language_config('PHP')
    if php_config and 'extensions' in php_config:
        print(f"  ✓ PHP config loaded")
        print(f"    Extensions: {php_config['extensions']}")
        print(f"    Frameworks: {php_config['frameworks']}")
        print(f"    Style: {php_config['style_guide']}")
    else:
        print(f"  ✗ PHP config missing")
        return False
    
    print()
    
    # Test Python config
    py_config = coder.get_language_config('Python')
    if py_config and 'extensions' in py_config:
        print(f"  ✓ Python config loaded")
        print(f"    Extensions: {py_config['extensions']}")
        print(f"    Frameworks: {py_config['frameworks']}")
        print(f"    Style: {py_config['style_guide']}")
    else:
        print(f"  ✗ Python config missing")
        return False
    
    print()
    
    # Test Go config
    go_config = coder.get_language_config('Go')
    if go_config and 'extensions' in go_config:
        print(f"  ✓ Go config loaded")
        print(f"    Extensions: {go_config['extensions']}")
        print(f"    Frameworks: {go_config['frameworks']}")
        print(f"    Style: {go_config['style_guide']}")
    else:
        print(f"  ✗ Go config missing")
        return False
    
    print()
    return True

def test_prompt_templates():
    """Test language-specific prompt generation"""
    print("=" * 60)
    print("  Testing Prompt Templates")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    # Test PHP prompt
    php_prompt = coder.get_prompt_for_language(
        'review_prompt',
        'PHP',
        code='<?php echo "hello"; ?>'
    )
    if php_prompt and 'PHP' in php_prompt:
        print(f"  ✓ PHP prompt generated ({len(php_prompt)} chars)")
    else:
        print(f"  ✗ PHP prompt failed")
        return False
    
    print()
    
    # Test Python prompt
    py_prompt = coder.get_prompt_for_language(
        'review_prompt',
        'Python',
        code='def hello(): print("hello")'
    )
    if py_prompt and 'Python' in py_prompt:
        print(f"  ✓ Python prompt generated ({len(py_prompt)} chars)")
    else:
        print(f"  ✗ Python prompt failed")
        return False
    
    print()
    
    # Test Go prompt
    go_prompt = coder.get_prompt_for_language(
        'review_prompt',
        'Go',
        code='func main() { println("hello") }'
    )
    if go_prompt and 'Go' in go_prompt:
        print(f"  ✓ Go prompt generated ({len(go_prompt)} chars)")
    else:
        print(f"  ✗ Go prompt failed")
        return False
    
    print()
    return True

def test_sample_files():
    """Test language detection on sample files"""
    print("=" * 60)
    print("  Testing Sample Files")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    sample_files = [
        ("sample_python_app.py", "Python"),
        ("sample_go_app.go", "Go"),
    ]
    
    all_passed = True
    
    for filename, expected_lang in sample_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if not os.path.exists(filepath):
            print(f"  ✗ {filename} not found")
            all_passed = False
            continue
        
        detected_lang = coder.detect_language(filepath)
        
        if detected_lang == expected_lang:
            print(f"  ✓ {filename:30} -> {detected_lang}")
            
            # Try to read file
            content = coder.read_file(filepath)
            if content:
                print(f"    File read: {len(content)} bytes, {len(content.splitlines())} lines")
        else:
            print(f"  ✗ {filename:30} -> {detected_lang} (expected: {expected_lang})")
            all_passed = False
    
    print()
    return all_passed

def main():
    """Run all multi-language tests"""
    print("\n" + "=" * 60)
    print("  AI Coder - Multi-Language Support Test")
    print("=" * 60 + "\n")
    
    tests = [
        ("Language Detection", test_language_detection),
        ("Language Config", test_language_config),
        ("Prompt Templates", test_prompt_templates),
        ("Sample Files", test_sample_files),
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
        print("✓ All multi-language tests passed!")
        print("\nSupported languages:")
        print("  • PHP (CodeIgniter, Laravel, Symfony)")
        print("  • Python (Flask, FastAPI, Django)")
        print("  • Go (net/http, gin, echo, fiber)")
        print("\nAI Coder is ready for multi-language development!")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
