# Label Printer Automation

A PySide6 + Flask application for automating label printing via WiFi commands from physical button devices.

## Features

- **Cross-Platform Development**: Mock printing on macOS/Linux, real printing on Windows
- **PySide6 GUI**: Configure printer selection and button-to-label mappings
- **Flask Server**: Receives WiFi commands from physical devices
- **Multi-format Support**: PNG, JPG, and SVG label files
- **DYMO Printer Support**: Works with DYMO and other Windows printers
- **Real-time Status**: Server status and print job monitoring
- **Executable Ready**: Designed for PyInstaller compilation

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create demo labels:

   ```bash
   python test_scripts/demo.py
   ```

## Usage

### Development Mode (Cross-Platform)
1. Run the application:

   ```bash
   python main.py
   ```

2. Configure the application:
   - Select a printer from the dropdown (mock printers on macOS/Linux)
   - Add button mappings (Button ID → Label File)
   - Start the Flask server

3. Test printing:
   - Use the "Test Print" button to verify setup
   - Mock prints are saved to `mock_prints/` directory
   - Send HTTP requests: `curl http://localhost:9000/print/<button_id>`

### Production Mode (Windows)
1. Deploy on Windows machine with DYMO printer
2. Configure your physical device to send HTTP requests to `http://your-pc-ip:9000/print/<button_id>`
3. See [WINDOWS_DEPLOYMENT.md](WINDOWS_DEPLOYMENT.md) for detailed Windows setup guide

## API Endpoints

- `GET /print/<button_id>` - Print label for specified button ID
- `GET /status` - Get server status and configuration
- `GET /health` - Health check endpoint

## Configuration

Settings are automatically saved to `config.json`:

- Selected printer
- Button-to-label mappings
- Server host/port settings

## Logging

Application logs are written to `printer_app.log` with timestamps and detailed information about print jobs and errors.

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Requirements

### Development (Cross-Platform)
- **Python 3.8+**
- **macOS/Linux/Windows** for development and testing
- Mock printing functionality for development

### Production (Windows Only)
- **Windows OS** (required for win32print and DYMO printer support)
- DYMO or compatible label printer
- Network connectivity for WiFi commands

**Note**: The application includes mock printing for cross-platform development. For actual printing, deploy on Windows with a DYMO printer.

## Project Structure

```
LabelPrinterAutomation/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                # Git ignore rules
├── config/
│   └── config_manager.py     # Configuration management
├── printing/
│   └── printer_manager.py    # Cross-platform printer handling
├── server/
│   └── flask_app.py          # Flask API server
├── ui/
│   └── main_window.py        # PySide6 GUI
└── test_scripts/             # Test and demo scripts
    ├── README.md
    ├── demo.py
    ├── test_mock_printing.py
    ├── test_flask_direct.py
    └── ... (other test files)
```

## Troubleshooting

### Common Issues

**Qt Platform Plugin Error on macOS:**
```
qt.qpa.plugin: Could not find the Qt platform plugin "cocoa"
```
**Solution:** Downgrade PySide6 to version 6.8.0:
```bash
pip uninstall PySide6 -y
pip install PySide6==6.8.0
```

**Server Won't Start:**
- Check if port 9000 is available: `lsof -i :9000`
- Try a different port in the GUI settings
- Check `printer_app.log` for error details

**Mock Printing Not Working:**
- Ensure `mock_prints/` directory exists and is writable
- Check that image files exist and are accessible
- Verify file permissions

### General Troubleshooting

- Ensure your printer is properly installed and visible in Windows
- Check that label files exist and are accessible
- Verify network connectivity for WiFi commands
- Check `printer_app.log` for detailed error information
- Run test scripts in `test_scripts/` directory to diagnose issues
