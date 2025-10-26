# Changelog

## Version 1.0.0 - Initial Release

### Features
- **Cross-platform development support** with mock printing on macOS/Linux
- **PySide6 GUI** with printer selection and button mapping configuration
- **Flask API server** with `/print/<button_id>` endpoint
- **Multi-format image support** (PNG, JPG, SVG)
- **Configuration persistence** with JSON-based settings
- **Comprehensive logging** with file and console output
- **Test suite** with multiple test scripts

### Technical Details
- **Default port**: 9000 (changed from 5000 to avoid conflicts)
- **Mock printing**: Saves to `mock_prints/` directory on macOS/Linux
- **Real printing**: Uses `win32print` on Windows with DYMO printers
- **Threading**: Flask server runs in background thread
- **Dependencies**: PySide6, Flask, Pillow, svglib, reportlab, pywin32 (Windows only)

### Project Structure
```
LabelPrinterAutomation/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── .gitignore                # Git ignore rules
├── config/                   # Configuration management
├── printing/                  # Cross-platform printer handling
├── server/                   # Flask API server
├── ui/                       # PySide6 GUI
└── test_scripts/             # Test and demo scripts
```

### Bug Fixes
- Fixed excessive logging spam in printer manager
- Replaced cairosvg with svglib + reportlab for better SVG support
- Fixed GUI threading issues with server startup
- Resolved port conflicts by changing default port to 9000
- Reduced status update frequency to improve performance

### Testing
- Mock printing functionality tested and working
- Flask server startup and API endpoints tested
- GUI integration tested with proper threading
- Cross-platform compatibility verified
