#!/usr/bin/env python3
"""
Test GUI with server startup
"""

import sys
import os
import time
import threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import QTimer

from config.config_manager import ConfigManager
from printing.printer_manager import PrinterManager
from server.flask_app import FlaskPrintServer

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Test")
        self.setGeometry(100, 100, 400, 200)
        
        # Create components
        self.config_manager = ConfigManager()
        self.printer_manager = PrinterManager()
        self.flask_server = FlaskPrintServer(self.config_manager, self.printer_manager)
        
        # Create UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.status_label = QLabel("Server: Stopped")
        layout.addWidget(self.status_label)
        
        self.start_btn = QPushButton("Start Server")
        self.start_btn.clicked.connect(self.start_server)
        layout.addWidget(self.start_btn)
        
        self.test_btn = QPushButton("Test Server")
        self.test_btn.clicked.connect(self.test_server)
        layout.addWidget(self.test_btn)
        
        # Timer for status updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)  # Update every 2 seconds
    
    def start_server(self):
        """Start the Flask server"""
        print("Starting server...")
        try:
            # Start server in a separate thread
            def start_server_thread():
                try:
                    self.flask_server.start_server("127.0.0.1", 9000)
                    print("Server start command sent")
                except Exception as e:
                    print(f"Error starting server: {e}")
            
            server_thread = threading.Thread(target=start_server_thread, daemon=True)
            server_thread.start()
            
            self.start_btn.setText("Starting...")
            self.status_label.setText("Server: Starting...")
            print("Server thread started")
            
        except Exception as e:
            print(f"Error: {e}")
            self.status_label.setText(f"Error: {e}")
    
    def test_server(self):
        """Test the server"""
        print("Testing server...")
        try:
            import requests
            response = requests.get("http://127.0.0.1:9000/", timeout=5)
            print(f"Server response: {response.status_code}")
            self.status_label.setText(f"Server: Responding ({response.status_code})")
        except Exception as e:
            print(f"Server test failed: {e}")
            self.status_label.setText(f"Server: Not responding ({e})")
    
    def update_status(self):
        """Update server status"""
        if self.flask_server.is_server_running():
            self.status_label.setText("Server: Running")
            self.start_btn.setText("Stop Server")
        else:
            self.status_label.setText("Server: Stopped")
            self.start_btn.setText("Start Server")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    
    print("GUI test window created")
    print("Click 'Start Server' to test server startup")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
