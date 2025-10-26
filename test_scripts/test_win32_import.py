#!/usr/bin/env python3
"""
Test script to diagnose win32print import issues on Windows
"""

import sys
import platform

print(f"Python version: {sys.version}")
print(f"Platform: {platform.system()} {platform.release()}")
print(f"Architecture: {platform.architecture()}")

print("\n" + "="*50)
print("Testing pywin32 imports...")
print("="*50)

# Test 1: Check if pywin32 is installed
try:
    import pywin32
    print("✅ pywin32 package found")
except ImportError:
    print("❌ pywin32 package NOT found")
    print("   Solution: pip install pywin32")

# Test 2: Check win32print specifically
try:
    import win32print
    print("✅ win32print module imported successfully")
    
    # Test basic functionality
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    print(f"✅ Found {len(printers)} printers:")
    for i, printer in enumerate(printers):
        print(f"   {i+1}. {printer[2]}")  # printer[2] is the name
        
except ImportError as e:
    print(f"❌ win32print import failed: {e}")
    print("   Solution: pip install pywin32")
except Exception as e:
    print(f"❌ win32print error: {e}")

# Test 3: Check win32api
try:
    import win32api
    print("✅ win32api module imported successfully")
except ImportError as e:
    print(f"❌ win32api import failed: {e}")
    print("   Solution: pip install pywin32")

# Test 4: Check if we can run post-install script
print("\n" + "="*50)
print("Installation recommendations:")
print("="*50)

if platform.system() == "Windows":
    print("1. Install pywin32:")
    print("   pip install pywin32")
    print()
    print("2. If that doesn't work, try:")
    print("   pip install --upgrade pip")
    print("   pip install pywin32")
    print()
    print("3. If you get permission errors:")
    print("   pip install --user pywin32")
    print()
    print("4. After installation, run post-install script:")
    print("   python Scripts/pywin32_postinstall.py -install")
    print()
    print("5. Or manually run:")
    print("   python -c \"import win32print; print('Success!')\"")
else:
    print("This script is designed for Windows. On macOS/Linux, the app uses mock printing.")
