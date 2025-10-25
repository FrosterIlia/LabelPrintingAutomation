#!/usr/bin/env python3
"""
Test GUI only without Flask server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def test_gui():
    """Test GUI without server"""
    print("🧪 Testing GUI Only")
    print("=" * 30)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("✅ GUI created and shown")
    print("   - Check if the window appears")
    print("   - Try clicking 'Start Server' button")
    print("   - Check the status label")
    
    # Run for a short time to test
    app.processEvents()
    print("✅ GUI test completed")

if __name__ == "__main__":
    test_gui()
