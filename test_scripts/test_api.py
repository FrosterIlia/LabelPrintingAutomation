#!/usr/bin/env python3
"""
Test script for Flask API endpoints
"""

import requests
import time
import json

def test_flask_api():
    """Test the Flask API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Flask API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - is the Flask server running?")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test status endpoint
    print("\n2. Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test print endpoint (this will fail if no mappings are configured)
    print("\n3. Testing print endpoint...")
    try:
        response = requests.get(f"{base_url}/print/test_button", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 API testing completed!")
    print("\nTo test printing:")
    print("1. Open the GUI application")
    print("2. Add a button mapping (e.g., 'test_button' → 'path/to/label.png')")
    print("3. Start the Flask server")
    print("4. Run: curl http://localhost:5000/print/test_button")

if __name__ == "__main__":
    test_flask_api()
