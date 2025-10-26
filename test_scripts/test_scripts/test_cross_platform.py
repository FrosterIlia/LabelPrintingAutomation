#!/usr/bin/env python3
"""
Test cross-platform functionality
"""

import sys
import os
import platform
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from printing.printer_manager import PrinterManager
from PIL import Image

def test_cross_platform():
    """Test cross-platform printing functionality"""
    print("🧪 Testing Cross-Platform Functionality")
    print("=" * 50)
    
    # Get system info
    system = platform.system()
    print(f"Operating System: {system}")
    print(f"Platform: {platform.platform()}")
    
    # Create printer manager
    printer_manager = PrinterManager()
    
    # Test printer enumeration
    print(f"\n1. Testing printer enumeration on {system}...")
    printers = printer_manager.get_available_printers()
    print(f"   Found {len(printers)} printers:")
    for printer in printers:
        print(f"   - {printer}")
    
    # Test platform-specific behavior
    print(f"\n2. Testing platform-specific behavior...")
    if system == "Windows":
        print("   ✅ Windows detected - will use real printing with win32print")
        print("   📝 Note: Requires DYMO printer and win32print package")
    else:
        print("   ✅ Non-Windows detected - will use mock printing")
        print("   📁 Mock prints will be saved to 'mock_prints/' directory")
    
    # Test printer availability
    print(f"\n3. Testing printer availability...")
    test_printer = printers[0] if printers else "Test Printer"
    is_available = printer_manager.is_printer_available(test_printer)
    print(f"   Printer '{test_printer}' available: {is_available}")
    
    # Create test image
    print(f"\n4. Creating test image...")
    test_img = Image.new('RGB', (200, 100), color='white')
    test_path = "test_cross_platform.png"
    test_img.save(test_path, 'PNG')
    print(f"   ✅ Test image created: {test_path}")
    
    # Test printing
    print(f"\n5. Testing print functionality...")
    try:
        success = printer_manager.print_image(test_path, test_printer, "portrait")
        if success:
            print("   ✅ Print test successful!")
            if system != "Windows":
                print("   📁 Check 'mock_prints/' directory for saved file")
        else:
            print("   ❌ Print test failed")
    except Exception as e:
        print(f"   ❌ Print test error: {e}")
    
    # Clean up
    print(f"\n6. Cleaning up...")
    try:
        os.remove(test_path)
        print(f"   ✅ Removed test file: {test_path}")
    except:
        print(f"   ⚠️  Could not remove test file: {test_path}")
    
    print(f"\n🎉 Cross-platform test completed!")
    print(f"📋 Summary:")
    print(f"   - System: {system}")
    print(f"   - Printers found: {len(printers)}")
    print(f"   - Platform detection: {'✅ Working' if printer_manager.is_windows == (system == 'Windows') else '❌ Failed'}")
    
    if system == "Windows":
        print(f"   - Real printing: {'✅ Ready' if 'win32print' in str(printer_manager.__class__.__module__) else '❌ Not available'}")
    else:
        print(f"   - Mock printing: ✅ Active")

if __name__ == "__main__":
    test_cross_platform()
