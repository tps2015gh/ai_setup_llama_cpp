#!/usr/bin/env python3
"""
Test server status functionality
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from ai_coder import AICoder

def test_status_methods():
    """Test new status methods"""
    print("=" * 60)
    print("  Testing Server Status Methods")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    # Test 1: get_server_status (when not running)
    print("Test 1: get_server_status() - Server not running")
    status = coder.get_server_status()
    
    if 'process_alive' in status and 'api_health' in status:
        print(f"  ✓ Status dict has required keys")
        print(f"    Process alive: {status['process_alive']}")
        print(f"    API health: {status['api_health']}")
        print(f"    Uptime: {status['uptime']}")
        print()
    else:
        print(f"  ✗ Missing required keys")
        return False
    
    # Test 2: get_api_health (when not running)
    print("Test 2: get_api_health() - Server not running")
    api_health = coder.get_api_health()
    
    if api_health and 'api_responsive' in api_health:
        print(f"  ✓ API health check works")
        print(f"    API responsive: {api_health['api_responsive']}")
        print(f"    Error: {api_health.get('error', 'N/A')}")
        print()
    else:
        print(f"  ✗ API health check failed")
        return False
    
    # Test 3: get_server_uptime (when not running)
    print("Test 3: get_server_uptime() - Server not running")
    uptime = coder.get_server_uptime()
    
    if uptime == "N/A":
        print(f"  ✓ Uptime correctly shows N/A when not running")
        print()
    else:
        print(f"  ✗ Uptime should be N/A, got: {uptime}")
        return False
    
    return True

def test_status_with_server():
    """Test status methods with actual server (optional)"""
    print("=" * 60)
    print("  Testing with Live Server (if available)")
    print("=" * 60)
    
    coder = AICoder()
    
    print()
    
    # Try to start server
    print("Attempting to start server for testing...")
    started = coder.start_server()
    
    if not started:
        print(f"  ⚠ Server not started, skipping live tests")
        print(f"    (This is OK if you just want to test the methods)")
        print()
        return True
    
    print()
    
    # Test with running server
    print("Test 1: get_server_status() - Server running")
    status = coder.get_server_status()
    
    if status['process_alive']:
        print(f"  ✓ Process detected as running")
        print(f"    PID: {status['pid']}")
        print(f"    Uptime: {status['uptime']}")
        print()
    else:
        print(f"  ✗ Process not detected as running")
        coder.stop_server()
        return False
    
    print("Test 2: get_api_health() - Server running")
    api_health = coder.get_api_health()
    
    if api_health['api_responsive']:
        print(f"  ✓ API is responsive")
        print(f"    Response time: {api_health['response_time_ms']}ms")
        print(f"    Models: {api_health['models_count']}")
        print()
    else:
        print(f"  ⚠ API not responding (may still be loading)")
        print(f"    Error: {api_health.get('error', 'Unknown')}")
        print()
    
    print("Test 3: check_server_status() - Full display")
    result = coder.check_server_status()
    
    if result:
        print(f"  ✓ Full status check completed")
        print()
    else:
        print(f"  ⚠ Status check had issues (server may still be starting)")
        print()
    
    # Stop server
    print("Stopping test server...")
    coder.stop_server()
    print()
    
    return True

def main():
    """Run all status tests"""
    print("\n" + "=" * 60)
    print("  AI Coder - Server Status Test")
    print("=" * 60 + "\n")
    
    # Test methods (no server needed)
    if test_status_methods():
        print("✓ Basic status methods work correctly\n")
    else:
        print("✗ Basic status methods failed\n")
    
    # Test with live server (optional)
    print("=" * 60)
    choice = input("Start server for live testing? (y/n): ").strip().lower()
    
    if choice == 'y':
        if test_status_with_server():
            print("✓ Live server tests completed\n")
        else:
            print("✗ Live server tests failed\n")
    else:
        print("\nSkipping live server tests\n")
    
    print("=" * 60)
    print("  Summary")
    print("=" * 60)
    print()
    print("New methods added:")
    print("  • get_server_status()     - Comprehensive status dict")
    print("  • get_server_uptime()     - Calculate uptime")
    print("  • get_api_health()        - API health check")
    print("  • check_server_status()   - Display full status (Menu 3)")
    print()
    print("Menu 3 now shows:")
    print("  ✓ Process status (Running/Stopped)")
    print("  ✓ Process ID (PID)")
    print("  ✓ Server uptime")
    print("  ✓ API responsiveness")
    print("  ✓ Response time")
    print("  ✓ Models available")
    print("  ✓ Performance indicator")
    print("  ✓ Full configuration")
    print("  ✓ API endpoints")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
