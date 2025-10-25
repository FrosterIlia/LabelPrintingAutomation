import sys
import os
import logging
from typing import Optional
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QComboBox, QPushButton, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox,
                           QGroupBox, QLineEdit, QSpinBox, QStatusBar, QSplitter, QDialog)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QFont

from config.config_manager import ConfigManager
from printing.printer_manager import PrinterManager
from server.flask_app import FlaskPrintServer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.printer_manager = PrinterManager()
        self.flask_server = FlaskPrintServer(self.config_manager, self.printer_manager)
        
        self.setup_logging()
        self.setup_ui()
        self.load_configuration()
        self.setup_timer()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('printer_app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("Label Printer Automation")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Configuration
        left_panel = self.create_configuration_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Button mappings
        right_panel = self.create_mappings_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 400])
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
        
    def create_configuration_panel(self):
        """Create the configuration panel"""
        group = QGroupBox("Configuration")
        layout = QVBoxLayout(group)
        
        # Printer selection
        printer_layout = QHBoxLayout()
        printer_layout.addWidget(QLabel("Printer:"))
        self.printer_combo = QComboBox()
        self.printer_combo.currentTextChanged.connect(self.on_printer_changed)
        printer_layout.addWidget(self.printer_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_printers)
        printer_layout.addWidget(refresh_btn)
        layout.addLayout(printer_layout)
        
        # Test print button
        test_btn = QPushButton("Test Print")
        test_btn.clicked.connect(self.test_print)
        layout.addWidget(test_btn)
        
        # Server configuration
        server_group = QGroupBox("Server Settings")
        server_layout = QVBoxLayout(server_group)
        
        # Host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_edit = QLineEdit("0.0.0.0")
        host_layout.addWidget(self.host_edit)
        server_layout.addLayout(host_layout)
        
        # Port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1000, 65535)
        self.port_spin.setValue(9000)
        port_layout.addWidget(self.port_spin)
        server_layout.addLayout(port_layout)
        
        # Server controls
        server_controls = QHBoxLayout()
        self.start_server_btn = QPushButton("Start Server")
        self.start_server_btn.clicked.connect(self.toggle_server)
        server_controls.addWidget(self.start_server_btn)
        
        self.server_status_label = QLabel("Stopped")
        self.server_status_label.setStyleSheet("color: red; font-weight: bold;")
        server_controls.addWidget(self.server_status_label)
        server_layout.addLayout(server_controls)
        
        layout.addWidget(server_group)
        layout.addStretch()
        
        return group
    
    def create_mappings_panel(self):
        """Create the button mappings panel"""
        group = QGroupBox("Button Mappings")
        layout = QVBoxLayout(group)
        
        # Table for button mappings
        self.mappings_table = QTableWidget()
        self.mappings_table.setColumnCount(2)
        self.mappings_table.setHorizontalHeaderLabels(["Button ID", "Label File"])
        self.mappings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mappings_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.mappings_table)
        
        # Buttons for managing mappings
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Mapping")
        add_btn.clicked.connect(self.add_mapping)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Mapping")
        edit_btn.clicked.connect(self.edit_mapping)
        buttons_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("Remove Mapping")
        remove_btn.clicked.connect(self.remove_mapping)
        buttons_layout.addWidget(remove_btn)
        
        layout.addLayout(buttons_layout)
        
        return group
    
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5000)  # Update every 5 seconds to reduce logging
    
    def load_configuration(self):
        """Load configuration from file"""
        # Load printers
        self.refresh_printers()
        
        # Load selected printer
        selected_printer = self.config_manager.get_selected_printer()
        if selected_printer:
            index = self.printer_combo.findText(selected_printer)
            if index >= 0:
                self.printer_combo.setCurrentIndex(index)
        
        # Load server settings
        host, port = self.config_manager.get_server_config()
        self.host_edit.setText(host)
        self.port_spin.setValue(port)
        
        # Load button mappings
        self.load_mappings()
    
    def refresh_printers(self):
        """Refresh the list of available printers"""
        self.printer_combo.clear()
        printers = self.printer_manager.get_available_printers()
        
        if not printers:
            self.printer_combo.addItem("No printers found")
            self.logger.warning("No printers found")
        else:
            self.printer_combo.addItems(printers)
            self.logger.info(f"Found {len(printers)} printers")
    
    def on_printer_changed(self, printer_name):
        """Handle printer selection change"""
        if printer_name and printer_name != "No printers found":
            self.config_manager.set_selected_printer(printer_name)
            self.config_manager.save_config()
            self.logger.info(f"Selected printer: {printer_name}")
    
    def test_print(self):
        """Test print to selected printer"""
        printer_name = self.printer_combo.currentText()
        if not printer_name or printer_name == "No printers found":
            QMessageBox.warning(self, "Warning", "Please select a printer first")
            return
        
        if self.printer_manager.test_print(printer_name):
            QMessageBox.information(self, "Success", f"Test print sent to {printer_name}")
            self.logger.info(f"Test print successful to {printer_name}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to send test print to {printer_name}")
            self.logger.error(f"Test print failed to {printer_name}")
    
    def toggle_server(self):
        """Toggle Flask server on/off"""
        if self.flask_server.is_server_running():
            self.flask_server.stop_server()
            self.start_server_btn.setText("Start Server")
            self.server_status_label.setText("Stopped")
            self.server_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.logger.info("Server stopped")
        else:
            host = self.host_edit.text()
            port = self.port_spin.value()
            
            # Save server settings
            self.config_manager.set("server_host", host)
            self.config_manager.set("server_port", port)
            self.config_manager.save_config()
            
            # Start server in a separate thread to avoid blocking GUI
            import threading
            def start_server_thread():
                try:
                    self.flask_server.start_server(host, port)
                    # Give the server time to start
                    import time
                    time.sleep(1)
                except Exception as e:
                    self.logger.error(f"Error starting server: {e}")
            
            server_thread = threading.Thread(target=start_server_thread, daemon=True)
            server_thread.start()
            
            # Update UI immediately
            self.start_server_btn.setText("Starting...")
            self.server_status_label.setText("Starting server...")
            self.server_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.logger.info(f"Starting server on {host}:{port}")
    
    def load_mappings(self):
        """Load button mappings into table"""
        mappings = self.config_manager.get_button_mappings()
        self.mappings_table.setRowCount(len(mappings))
        
        for row, (button_id, label_file) in enumerate(mappings.items()):
            self.mappings_table.setItem(row, 0, QTableWidgetItem(button_id))
            self.mappings_table.setItem(row, 1, QTableWidgetItem(label_file))
    
    def add_mapping(self):
        """Add new button mapping"""
        dialog = MappingDialog(self)
        if dialog.exec():
            button_id, label_file = dialog.get_mapping()
            if button_id and label_file:
                self.config_manager.add_button_mapping(button_id, label_file)
                self.config_manager.save_config()
                self.load_mappings()
                self.logger.info(f"Added mapping: {button_id} -> {label_file}")
    
    def edit_mapping(self):
        """Edit selected button mapping"""
        current_row = self.mappings_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a mapping to edit")
            return
        
        button_id = self.mappings_table.item(current_row, 0).text()
        label_file = self.mappings_table.item(current_row, 1).text()
        
        dialog = MappingDialog(self, button_id, label_file)
        if dialog.exec():
            new_button_id, new_label_file = dialog.get_mapping()
            if new_button_id and new_label_file:
                # Remove old mapping
                self.config_manager.remove_button_mapping(button_id)
                # Add new mapping
                self.config_manager.add_button_mapping(new_button_id, new_label_file)
                self.config_manager.save_config()
                self.load_mappings()
                self.logger.info(f"Updated mapping: {new_button_id} -> {new_label_file}")
    
    def remove_mapping(self):
        """Remove selected button mapping"""
        current_row = self.mappings_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a mapping to remove")
            return
        
        button_id = self.mappings_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "Confirm", f"Remove mapping for button '{button_id}'?")
        if reply == QMessageBox.Yes:
            self.config_manager.remove_button_mapping(button_id)
            self.config_manager.save_config()
            self.load_mappings()
            self.logger.info(f"Removed mapping for button: {button_id}")
    
    def update_status(self):
        """Update status bar and server status"""
        if self.flask_server.is_server_running():
            self.server_status_label.setText("Running")
            self.server_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.start_server_btn.setText("Stop Server")
        else:
            self.server_status_label.setText("Stopped")
            self.server_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.start_server_btn.setText("Start Server")
        
        # Update status bar
        printer_count = len(self.printer_manager.get_available_printers())
        mapping_count = len(self.config_manager.get_button_mappings())
        self.status_bar.showMessage(f"Printers: {printer_count} | Mappings: {mapping_count}")


class MappingDialog(QDialog):
    def __init__(self, parent=None, button_id="", label_file=""):
        super().__init__(parent)
        self.setWindowTitle("Button Mapping")
        self.setModal(True)
        self.resize(400, 150)
        
        layout = QVBoxLayout(self)
        
        # Button ID
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("Button ID:"))
        self.button_id_edit = QLineEdit(button_id)
        id_layout.addWidget(self.button_id_edit)
        layout.addLayout(id_layout)
        
        # Label file
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Label File:"))
        self.label_file_edit = QLineEdit(label_file)
        file_layout.addWidget(self.label_file_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def browse_file(self):
        """Browse for label file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Label File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.svg);;All Files (*)"
        )
        if file_path:
            self.label_file_edit.setText(file_path)
    
    def get_mapping(self):
        """Get the mapping values"""
        return self.button_id_edit.text(), self.label_file_edit.text()

