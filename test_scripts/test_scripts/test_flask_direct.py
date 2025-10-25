#!/usr/bin/env python3
"""
Test Flask server directly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_manager import ConfigManager
from printing.printer_manager import PrinterManager
from server.flask_app import FlaskPrintServer
import time

def test_flask_direct():
    """Test Flask server directly"""
    print("🧪 Testing Flask Server Directly")
    print("=" * 40)
    
    try:
        # Create components
        print("1. Creating components...")
        config_manager = ConfigManager()
        printer_manager = PrinterManager()
        flask_server = FlaskPrintServer(config_manager, printer_manager)
        print("   ✅ Components created")
        
        # Start server
        print("2. Starting server...")
        flask_server.start_server("0.0.0.0", 9000)
        print("   ✅ Server start command sent")
        
        # Wait a bit
        print("3. Waiting for server to start...")
        time.sleep(3)
        
        # Check if running
        print("4. Checking server status...")
        is_running = flask_server.is_server_running()
        print(f"   Server running: {is_running}")
        
        # Test with requests
        print("5. Testing with requests...")
        import requests
        try:
            response = requests.get("http://localhost:5001/", timeout=5)
            print(f"   Root endpoint: {response.status_code}")
            print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_flask_direct()
