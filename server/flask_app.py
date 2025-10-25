import logging
from flask import Flask, jsonify, request
from typing import Dict, Optional
import threading
import time

class FlaskPrintServer:
    def __init__(self, config_manager, printer_manager):
        self.config_manager = config_manager
        self.printer_manager = printer_manager
        self.app = Flask(__name__)
        self.server_thread = None
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/', methods=['GET'])
        def root():
            """Root endpoint"""
            return jsonify({
                'message': 'Label Printer Automation API',
                'version': '1.0.0',
                'endpoints': ['/print/<button_id>', '/status', '/health']
            })
        
        @self.app.route('/print/<button_id>', methods=['GET', 'POST'])
        def print_label(button_id):
            """Print label for given button ID"""
            try:
                # Get button mappings
                button_mappings = self.config_manager.get_button_mappings()
                
                if button_id not in button_mappings:
                    self.logger.warning(f"Button ID '{button_id}' not found in mappings")
                    return jsonify({
                        'success': False,
                        'error': f'Button ID "{button_id}" not configured'
                    }), 404
                
                label_file = button_mappings[button_id]
                selected_printer = self.config_manager.get_selected_printer()
                
                if not selected_printer:
                    self.logger.error("No printer selected")
                    return jsonify({
                        'success': False,
                        'error': 'No printer selected'
                    }), 500
                
                # Print the label
                success = self.printer_manager.print_image(label_file, selected_printer)
                
                if success:
                    self.logger.info(f"Successfully printed label for button {button_id}: {label_file}")
                    return jsonify({
                        'success': True,
                        'message': f'Print job sent for button {button_id}',
                        'label_file': label_file,
                        'printer': selected_printer
                    })
                else:
                    self.logger.error(f"Failed to print label for button {button_id}: {label_file}")
                    return jsonify({
                        'success': False,
                        'error': f'Failed to print label: {label_file}'
                    }), 500
                    
            except Exception as e:
                self.logger.error(f"Error processing print request for button {button_id}: {e}")
                return jsonify({
                    'success': False,
                    'error': f'Internal server error: {str(e)}'
                }), 500
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get server status"""
            return jsonify({
                'success': True,
                'status': 'running',
                'printer': self.config_manager.get_selected_printer(),
                'button_count': len(self.config_manager.get_button_mappings())
            })
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({'status': 'healthy'})
    
    def start_server(self, host: str = "0.0.0.0", port: int = 5000):
        """Start Flask server in background thread"""
        if self.is_running:
            self.logger.warning("Server is already running")
            return
        
        def run_server():
            try:
                self.logger.info(f"Starting Flask server on {host}:{port}")
                # Use Flask's built-in development server
                self.app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
            except Exception as e:
                self.logger.error(f"Flask server error: {e}")
                self.is_running = False
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self.is_running = True
        self.logger.info(f"Flask server started on {host}:{port}")
    
    def stop_server(self):
        """Stop Flask server"""
        if not self.is_running:
            self.logger.warning("Server is not running")
            return
        
        # Note: Flask development server doesn't have a clean shutdown
        # The daemon thread will be terminated when main process exits
        self.is_running = False
        self.logger.info("Flask server stopped")
    
    def is_server_running(self) -> bool:
        """Check if server is running"""
        return self.is_running and self.server_thread and self.server_thread.is_alive()
