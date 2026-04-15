#!/usr/bin/env python3
"""
Quick test to verify auto-save is working
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ai_coder import AICoder

# Simulate an AI response with code blocks
test_ai_response = """Sure! Here's a simple hello world program in three languages:

### PHP Version

```php
<?php
echo "Hello, World!";
?>
```

### Python Version

```python
print("Hello, World!")
```

### Go Version

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

All three programs will output: Hello, World!"""

print("=" * 60)
print("  Testing Auto-Save with Simulated AI Response")
print("=" * 60)
print()

# Create coder instance
coder = AICoder()

# Check config
auto_save = coder.config.get('ai_code_gen', {}).get('auto_save', False)
output_dir = coder.config.get('ai_code_gen', {}).get('output_directory', '')

print(f"Config check:")
print(f"  auto_save: {auto_save}")
print(f"  output_directory: {output_dir}")
print()

# Try to save code blocks
print("Calling save_ai_code_blocks()...")
print()

saved_files = coder.save_ai_code_blocks(
    test_ai_response,
    question_text="create hello world program",
    output_dir=output_dir if output_dir else None
)

print()
print("=" * 60)
print(f"Results: {len(saved_files)} file(s) saved")
print("=" * 60)

if saved_files:
    print("\nSaved files:")
    for file_info in saved_files:
        print(f"  ✓ {file_info['filename']} ({file_info['size']} bytes)")
        print(f"    Path: {file_info['filepath']}")
        print()
else:
    print("\n✗ No files were saved!")
    print("\nPossible issues:")
    print("  1. No code blocks found in response")
    print("  2. Output directory not accessible")
    print("  3. Auto-save not enabled in config")

print()
