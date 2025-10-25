#!/usr/bin/env python3
"""
Simple Flask test to verify basic functionality
"""

from flask import Flask, jsonify
import threading
import time
import requests

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({'message': 'Hello World'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

def run_server():
    app.run(host='0.0.0.0', port=9001, debug=False, use_reloader=False)

def test_simple_flask():
    """Test a simple Flask server"""
    print("🧪 Testing Simple Flask Server")
    print("=" * 40)
    
    # Start server in background
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Test endpoints
    try:
        response = requests.get('http://localhost:9001/', timeout=5)
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
    
    try:
        response = requests.get('http://localhost:9001/health', timeout=5)
        print(f"Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health endpoint failed: {e}")

if __name__ == "__main__":
    test_simple_flask()
