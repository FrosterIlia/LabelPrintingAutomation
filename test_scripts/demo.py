#!/usr/bin/env python3
"""
Demo script showing how to use the Label Printer Automation application
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_demo_labels():
    """Create some demo label images for testing"""
    print("🎨 Creating demo label images...")
    
    # Create demo labels directory
    demo_dir = "demo_labels"
    if not os.path.exists(demo_dir):
        os.makedirs(demo_dir)
    
    # Create different types of labels
    labels = [
        {
            "name": "kit_a.png",
            "title": "KIT A",
            "description": "Basic Electronics Kit",
            "color": (255, 100, 100)  # Red
        },
        {
            "name": "kit_b.png", 
            "title": "KIT B",
            "description": "Advanced Components",
            "color": (100, 100, 255)  # Blue
        },
        {
            "name": "kit_c.png",
            "title": "KIT C", 
            "description": "Professional Tools",
            "color": (100, 255, 100)  # Green
        }
    ]
    
    for label in labels:
        # Create label image
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw border
        draw.rectangle([10, 10, 390, 190], outline='black', width=3)
        
        # Draw colored header
        draw.rectangle([15, 15, 385, 60], fill=label["color"])
        
        # Add text
        try:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        except:
            font_large = None
            font_small = None
        
        # Title
        draw.text((20, 25), label["title"], fill='white', font=font_large)
        
        # Description
        draw.text((20, 80), label["description"], fill='black', font=font_small)
        
        # Save label
        label_path = os.path.join(demo_dir, label["name"])
        img.save(label_path, 'PNG')
        print(f"   Created: {label_path}")
    
    print(f"✅ Demo labels created in '{demo_dir}' directory")
    return demo_dir

def show_usage_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🎯 LABEL PRINTER AUTOMATION - USAGE INSTRUCTIONS")
    print("="*60)
    
    print("\n1. 🚀 START THE APPLICATION:")
    print("   python main.py")
    
    print("\n2. ⚙️  CONFIGURE THE APPLICATION:")
    print("   • Select a printer from the dropdown")
    print("   • Add button mappings:")
    print("     - Button ID: 'kit_a' → Label File: 'demo_labels/kit_a.png'")
    print("     - Button ID: 'kit_b' → Label File: 'demo_labels/kit_b.png'")
    print("     - Button ID: 'kit_c' → Label File: 'demo_labels/kit_c.png'")
    print("   • Start the Flask server")
    
    print("\n3. 🧪 TEST PRINTING:")
    print("   • Use the 'Test Print' button in the GUI")
    print("   • Or send HTTP requests:")
    print("     curl http://localhost:5000/print/kit_a")
    print("     curl http://localhost:5000/print/kit_b")
    print("     curl http://localhost:5000/print/kit_c")
    
    print("\n4. 📁 CHECK RESULTS:")
    print("   • Mock prints are saved in 'mock_prints/' directory")
    print("   • Logs are written to 'printer_app.log'")
    
    print("\n5. 🔧 FOR PRODUCTION:")
    print("   • Deploy on Windows machine with DYMO printer")
    print("   • Configure your physical button device to send HTTP requests")
    print("   • Compile to executable: pyinstaller --onefile --windowed main.py")
    
    print("\n" + "="*60)

def main():
    """Main demo function"""
    print("🎪 Label Printer Automation Demo")
    print("=" * 50)
    
    # Create demo labels
    demo_dir = create_demo_labels()
    
    # Show usage instructions
    show_usage_instructions()
    
    print(f"\n🎉 Demo setup complete!")
    print(f"📁 Demo labels: {os.path.abspath(demo_dir)}")
    print(f"🚀 Run 'python main.py' to start the application")

if __name__ == "__main__":
    main()
