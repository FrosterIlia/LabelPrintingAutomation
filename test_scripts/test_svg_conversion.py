#!/usr/bin/env python3
"""
Test script to verify SVG conversion using svglib + reportlab
"""

import os
import tempfile
import sys

def test_svg_conversion():
    """Test SVG conversion functionality"""
    print("="*50)
    print("Testing SVG Conversion with svglib + reportlab")
    print("="*50)
    
    # Test 1: Check if libraries are installed
    try:
        from svglib.svglib import renderSVG
        from reportlab.graphics import renderPM
        print("✅ svglib and reportlab are installed")
    except ImportError as e:
        print(f"❌ Missing libraries: {e}")
        print("   Install with: pip install svglib reportlab")
        return False
    
    # Test 2: Create a simple test SVG
    test_svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="100" fill="lightblue" stroke="black" stroke-width="2"/>
  <text x="100" y="50" text-anchor="middle" font-family="Arial" font-size="16" fill="black">Test SVG</text>
  <circle cx="50" cy="50" r="20" fill="red"/>
  <circle cx="150" cy="50" r="20" fill="green"/>
</svg>"""
    
    # Create temporary SVG file
    temp_fd, temp_svg_path = tempfile.mkstemp(suffix='.svg')
    os.close(temp_fd)
    
    with open(temp_svg_path, 'w') as f:
        f.write(test_svg_content)
    
    print(f"✅ Created test SVG: {temp_svg_path}")
    
    # Test 3: Convert SVG to PNG
    try:
        # Convert SVG to reportlab drawing
        drawing = renderSVG.renderSVG(temp_svg_path)
        print("✅ SVG parsed successfully")
        
        # Create temporary PNG file
        temp_fd, temp_png_path = tempfile.mkstemp(suffix='.png')
        os.close(temp_fd)
        
        # Render drawing to PNG
        renderPM.drawToFile(drawing, temp_png_path, fmt='PNG')
        print("✅ SVG converted to PNG successfully")
        
        # Check if PNG file was created and has content
        if os.path.exists(temp_png_path) and os.path.getsize(temp_png_path) > 0:
            print(f"✅ PNG file created: {temp_png_path}")
            print(f"   File size: {os.path.getsize(temp_png_path)} bytes")
        else:
            print("❌ PNG file was not created or is empty")
            return False
        
        # Clean up
        try:
            os.unlink(temp_svg_path)
            os.unlink(temp_png_path)
            print("✅ Cleaned up temporary files")
        except:
            pass
        
        print("\n🎉 SVG conversion test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ SVG conversion failed: {e}")
        return False

if __name__ == "__main__":
    success = test_svg_conversion()
    
    if success:
        print("\n" + "="*50)
        print("✅ SVG conversion is working correctly!")
        print("   Your Label Printer Automation app can now handle SVG files.")
    else:
        print("\n" + "="*50)
        print("❌ SVG conversion test failed")
        print("   Install dependencies: pip install svglib reportlab")
    
    sys.exit(0 if success else 1)
