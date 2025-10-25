#!/usr/bin/env python3
"""
Test server startup to debug the issue
"""

import sys
import os
import time
import threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_manager import ConfigManager
from printing.printer_manager import PrinterManager
from server.flask_app import FlaskPrintServer

def test_server_startup():
    """Test server startup process"""
    print("🧪 Testing Server Startup Process")
    print("=" * 50)
    
    try:
        print("1. Creating components...")
        config_manager = ConfigManager()
        printer_manager = PrinterManager()
        flask_server = FlaskPrintServer(config_manager, printer_manager)
        print("   ✅ Components created successfully")
        
        print("2. Testing server startup...")
        print("   Starting server on localhost:9000...")
        
        # Start server in a separate thread
        def start_server():
            try:
                flask_server.start_server("127.0.0.1", 9000)
                print("   ✅ Server start command completed")
            except Exception as e:
                print(f"   ❌ Server start failed: {e}")
                import traceback
                traceback.print_exc()
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("3. Waiting for server to start...")
        for i in range(10):
            time.sleep(1)
            if flask_server.is_server_running():
                print(f"   ✅ Server is running after {i+1} seconds")
                break
            print(f"   ⏳ Waiting... ({i+1}/10)")
        else:
            print("   ❌ Server failed to start within 10 seconds")
            return False
        
        print("4. Testing server response...")
        import requests
        try:
            response = requests.get("http://127.0.0.1:9000/", timeout=5)
            print(f"   ✅ Server responding: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            return True
        except Exception as e:
            print(f"   ❌ Server not responding: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_server_startup()
    if success:
        print("\n🎉 Server startup test PASSED!")
    else:
        print("\n💥 Server startup test FAILED!")
