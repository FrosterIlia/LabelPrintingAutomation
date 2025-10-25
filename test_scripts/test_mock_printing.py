#!/usr/bin/env python3
"""
Test script for mock printing functionality
"""

import os
import sys
from PIL import Image
from printing.printer_manager import PrinterManager

def create_test_image():
    """Create a simple test image"""
    # Create a test image with some text
    img = Image.new('RGB', (400, 200), color='white')
    
    # This is a simple test - in a real scenario you'd use PIL's ImageDraw
    # to add text, but for now we'll just create a colored rectangle
    from PIL import ImageDraw, ImageFont
    
    draw = ImageDraw.Draw(img)
    
    # Draw a border
    draw.rectangle([10, 10, 390, 190], outline='black', width=2)
    
    # Draw some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
        draw.text((20, 50), "TEST LABEL", fill='black', font=font)
        draw.text((20, 80), "Mock Print Test", fill='black', font=font)
        draw.text((20, 110), "DYMO LabelWriter", fill='black', font=font)
    except:
        # If font loading fails, just draw without font
        draw.text((20, 50), "TEST LABEL", fill='black')
        draw.text((20, 80), "Mock Print Test", fill='black')
        draw.text((20, 110), "DYMO LabelWriter", fill='black')
    
    return img

def test_mock_printing():
    """Test the mock printing functionality"""
    print("🧪 Testing Mock Printing Functionality")
    print("=" * 50)
    
    # Create printer manager
    printer_manager = PrinterManager()
    
    # Test printer enumeration
    print("\n1. Testing printer enumeration...")
    printers = printer_manager.get_available_printers()
    print(f"   Found {len(printers)} printers:")
    for printer in printers:
        print(f"   - {printer}")
    
    # Test printer availability
    print("\n2. Testing printer availability...")
    test_printer = printers[0] if printers else "DYMO LabelWriter 4XL"
    is_available = printer_manager.is_printer_available(test_printer)
    print(f"   Printer '{test_printer}' available: {is_available}")
    
    # Create test image
    print("\n3. Creating test image...")
    test_img = create_test_image()
    test_path = "test_label.png"
    test_img.save(test_path, 'PNG')
    print(f"   Test image saved: {test_path}")
    
    # Test mock printing
    print("\n4. Testing mock printing...")
    success = printer_manager.print_image(test_path, test_printer)
    print(f"   Print result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Test print functionality
    print("\n5. Testing test_print method...")
    test_success = printer_manager.test_print(test_printer)
    print(f"   Test print result: {'✅ SUCCESS' if test_success else '❌ FAILED'}")
    
    # Clean up
    print("\n6. Cleaning up...")
    try:
        os.remove(test_path)
        print(f"   Removed test file: {test_path}")
    except:
        print(f"   Could not remove test file: {test_path}")
    
    print("\n🎉 Mock printing test completed!")
    print(f"📁 Check the 'mock_prints' directory for saved print files")

if __name__ == "__main__":
    test_mock_printing()
