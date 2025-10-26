#!/usr/bin/env python3
"""
Debug script to test print failure issues
"""

import os
import sys
from PIL import Image

def test_file_access(file_path):
    """Test if file exists and is accessible"""
    print(f"Testing file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        print(f"File size: {os.path.getsize(file_path)} bytes")
        print(f"File permissions: {oct(os.stat(file_path).st_mode)[-3:]}")
        
        # Test if PIL can open the image
        try:
            with Image.open(file_path) as img:
                print(f"Image format: {img.format}")
                print(f"Image size: {img.size}")
                print(f"Image mode: {img.mode}")
                print("✅ Image can be opened successfully")
        except Exception as e:
            print(f"❌ Error opening image: {e}")
    else:
        print("❌ File does not exist")
        
        # Check if it's a network drive issue
        if file_path.startswith("H:/") or file_path.startswith("H:\\"):
            print("⚠️  This appears to be a network drive path")
            print("   Network drives might not be accessible from the application")
            print("   Consider copying the file to a local path")

def test_printer_manager():
    """Test printer manager functionality"""
    print("\n" + "="*50)
    print("Testing Printer Manager")
    print("="*50)
    
    try:
        from printing.printer_manager import PrinterManager
        pm = PrinterManager()
        
        print(f"Available printers: {pm.get_available_printers()}")
        
        # Test if we can create a simple test image
        test_img = Image.new('RGB', (100, 100), color='white')
        test_path = "test_image.png"
        test_img.save(test_path)
        
        print(f"Created test image: {test_path}")
        
        # Clean up
        if os.path.exists(test_path):
            os.unlink(test_path)
            print("Cleaned up test image")
            
    except Exception as e:
        print(f"❌ Error testing printer manager: {e}")

if __name__ == "__main__":
    # Test the specific file from the error
    file_path = "H:/Shared drives/headamame/Products/Headphones/Media/Labels/Production Labels/Headamame - Wholesale.png"
    
    print("="*50)
    print("DEBUG: Print Failure Analysis")
    print("="*50)
    
    test_file_access(file_path)
    test_printer_manager()
    
    print("\n" + "="*50)
    print("RECOMMENDATIONS:")
    print("="*50)
    print("1. Check if the file path is accessible from your application")
    print("2. Verify that a printer is selected in the application")
    print("3. Test with a local file first")
    print("4. Check the application logs for detailed error messages")
