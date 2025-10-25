# Windows Deployment Guide

This guide explains how to deploy the Label Printer Automation application on Windows for production use with real DYMO printers.

## Prerequisites

### 1. Windows System Requirements
- Windows 10 or later
- Python 3.8 or higher
- DYMO LabelWriter printer installed and configured

### 2. DYMO Printer Setup
1. **Install DYMO Software:**
   - Download and install DYMO Label software from [DYMO website](https://www.dymo.com/en-US/labelwriter-software)
   - Install DYMO printer drivers
   - Test printing from DYMO software to ensure printer works

2. **Verify Printer Installation:**
   - Go to Settings → Printers & scanners
   - Confirm your DYMO printer appears in the list
   - Test print a sample label

## Installation

### 1. Install Python Dependencies
```cmd
pip install -r requirements.txt
```

### 2. Verify Windows-Specific Packages
```cmd
python -c "import win32print; print('win32print available')"
python -c "import win32api; print('win32api available')"
```

### 3. Test the Application
```cmd
python main.py
```

## Configuration

### 1. GUI Configuration
1. **Start the application:** `python main.py`
2. **Select Printer:** Choose your DYMO printer from the dropdown
3. **Add Button Mappings:**
   - Button ID: `kit_a` → Label File: `path/to/kit_a.png`
   - Button ID: `kit_b` → Label File: `path/to/kit_b.png`
   - etc.
4. **Configure Server:**
   - Host: `0.0.0.0` (to accept connections from ESP32)
   - Port: `9000` (or your preferred port)
5. **Start Server:** Click "Start Server" button

### 2. Test Printing
1. **Test Print Button:** Click "Test Print" to verify printer setup
2. **Check Logs:** Look for "✅ WINDOWS PRINT SUCCESS!" in console
3. **Verify Physical Print:** Check that label actually prints

## ESP32 Integration

### 1. Network Configuration
- Ensure ESP32 and Windows computer are on same WiFi network
- Find Windows computer IP: `ipconfig`
- ESP32 should send requests to: `http://WINDOWS_IP:9000/print/BUTTON_ID`

### 2. ESP32 Code Example
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* serverIP = "192.168.1.100";  // Windows computer IP
const int serverPort = 9000;

void sendPrintRequest(String buttonId) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/print/" + buttonId;
    
    http.begin(url);
    int httpResponseCode = http.POST("");
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);
    }
    http.end();
  }
}
```

## Production Deployment

### 1. Create Executable (Optional)
```cmd
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### 2. Windows Service (Optional)
For automatic startup, consider using:
- NSSM (Non-Sucking Service Manager)
- Windows Task Scheduler
- Or run as a Windows service

### 3. Firewall Configuration
- Allow Python through Windows Firewall
- Or allow port 9000 specifically

## Troubleshooting

### Common Issues

**1. Printer Not Found:**
```
Error: Printer 'DYMO LabelWriter 450' is not available
```
**Solution:**
- Verify printer is installed in Windows
- Check printer name matches exactly
- Test printing from other applications

**2. Print Job Not Printing:**
- Check DYMO printer is powered on
- Verify paper is loaded
- Check Windows print queue for stuck jobs
- Restart DYMO printer service

**3. ESP32 Can't Connect:**
- Verify Windows computer IP address
- Check firewall settings
- Ensure Flask server is running on `0.0.0.0:9000`
- Test with browser: `http://WINDOWS_IP:9000/`

**4. Import Errors:**
```
ImportError: No module named 'win32print'
```
**Solution:**
```cmd
pip install pywin32
```

### Debugging Steps

1. **Check Application Logs:**
   - Look for "✅ WINDOWS PRINT SUCCESS!" messages
   - Check `printer_app.log` file

2. **Test Printer Manually:**
   - Open DYMO software
   - Print a test label
   - Verify printer works independently

3. **Test Network Connectivity:**
   - From ESP32, ping Windows computer
   - Test HTTP request with curl or browser

4. **Verify Configuration:**
   - Check button mappings in GUI
   - Verify label files exist and are accessible
   - Confirm server is running and accessible

## Performance Tips

1. **Optimize Images:**
   - Use PNG format for best quality
   - Keep image sizes reasonable (under 1MB)
   - Avoid very large images that may cause memory issues

2. **Network Optimization:**
   - Use wired connection if possible
   - Ensure stable WiFi connection
   - Consider using static IP addresses

3. **System Resources:**
   - Close unnecessary applications
   - Ensure sufficient disk space
   - Monitor system performance

## Security Considerations

1. **Network Security:**
   - Use secure WiFi network
   - Consider VPN for remote access
   - Implement authentication if needed

2. **File Access:**
   - Secure label files with appropriate permissions
   - Regular backups of configuration
   - Monitor access logs

This deployment guide ensures your Label Printer Automation application works correctly on Windows with real DYMO printers!
