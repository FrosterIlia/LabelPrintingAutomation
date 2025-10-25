# Test Scripts

This directory contains various test scripts for the Label Printer Automation application.

## Test Scripts

### Core Functionality Tests

- **`test_mock_printing.py`** - Tests the mock printing functionality on macOS
- **`test_flask_direct.py`** - Tests Flask server startup and basic functionality
- **`test_simple_flask.py`** - Tests a simple Flask server for comparison

### GUI Tests

- **`test_gui_server.py`** - Tests GUI integration with server startup
- **`test_gui_only.py`** - Tests GUI components without server

### API Tests

- **`debug_server.py`** - Tests Flask API endpoints (health, status, print)
- **`test_api.py`** - Tests API endpoints with requests

### Demo Scripts

- **`demo.py`** - Creates demo label images and shows usage instructions

## Running Tests

### Basic Functionality Test
```bash
python test_scripts/test_mock_printing.py
```

### Flask Server Test
```bash
python test_scripts/test_flask_direct.py
```

### GUI Test
```bash
python test_scripts/test_gui_server.py
```

### API Test
```bash
python test_scripts/debug_server.py
```

### Demo Setup
```bash
python test_scripts/demo.py
```

## Notes

- All test scripts use port 9000 for the main application
- Simple Flask test uses port 9001 to avoid conflicts
- Mock printing tests create files in the `mock_prints/` directory
- Demo script creates sample labels in the `demo_labels/` directory
