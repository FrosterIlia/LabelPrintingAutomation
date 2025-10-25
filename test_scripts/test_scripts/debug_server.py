#!/usr/bin/env python3
"""
Debug script to test Flask server directly
"""

import requests
import json
import time

def test_server():
    """Test the Flask server endpoints"""
    base_url = "http://localhost:9000"
    
    print("🔍 Debugging Flask Server")
    print("=" * 40)
    
    # Test basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Root endpoint status: {response.status_code}")
        print(f"   Response text: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return
    
    # Test health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Health status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print("   ❌ Health endpoint failed")
    except Exception as e:
        print(f"   ❌ Health test failed: {e}")
    
    # Test status endpoint
    print("\n3. Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Status endpoint working")
        else:
            print("   ❌ Status endpoint failed")
    except Exception as e:
        print(f"   ❌ Status test failed: {e}")
    
    # Test print endpoint
    print("\n4. Testing print endpoint...")
    try:
        response = requests.get(f"{base_url}/print/test", timeout=5)
        print(f"   Print status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Print test failed: {e}")

if __name__ == "__main__":
    test_server()
