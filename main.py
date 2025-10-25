#!/usr/bin/env python3
"""
Label Printer Automation Application
Main entry point that launches the PySide6 UI and Flask server
"""

import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

def setup_logging():
    """Setup application-wide logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('printer_app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)  # Reduce Flask logs
    logging.getLogger('PIL').setLevel(logging.WARNING)  # Reduce Pillow logs

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Label Printer Automation Application")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Label Printer Automation")
        app.setApplicationVersion("1.0.0")
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Application started successfully")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
