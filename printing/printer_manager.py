import os
import tempfile
import logging
import platform
from typing import List, Optional
from PIL import Image

# cairosvg will be imported conditionally when needed

class PrinterManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_windows = platform.system() == "Windows"
        
        # Mock printers for development
        self.mock_printers = [
            "DYMO LabelWriter 4XL",
            "DYMO LabelWriter 450",
            "DYMO LabelWriter 450 Turbo",
            "DYMO LabelWriter 450 Duo",
            "HP LaserJet Pro",
            "Canon PIXMA"
        ]
        
        # Create mock print directory for development
        self.mock_print_dir = "mock_prints"
        if not os.path.exists(self.mock_print_dir):
            os.makedirs(self.mock_print_dir)
    
    def get_available_printers(self) -> List[str]:
        """Get list of available printer names"""
        if self.is_windows:
            try:
                import win32print
                printers = []
                for printer_info in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
                    printers.append(printer_info[2])  # printer_info[2] is the printer name
                return printers
            except Exception as e:
                self.logger.error(f"Error enumerating printers: {e}")
                return self.mock_printers
        else:
            # Return mock printers for macOS development
            # Only log once, not every time this method is called
            if not hasattr(self, '_mock_logged'):
                self.logger.info("Using mock printers for macOS development")
                self._mock_logged = True
            return self.mock_printers
    
    def is_printer_available(self, printer_name: str) -> bool:
        """Check if a specific printer is available"""
        available_printers = self.get_available_printers()
        return printer_name in available_printers
    
    def _convert_svg_to_png(self, svg_path: str) -> str:
        """Convert SVG file to temporary PNG file"""
        try:
            import cairosvg
        except ImportError:
            raise ImportError("cairosvg is not available. Cannot convert SVG files.")
        
        try:
            # Create temporary PNG file
            temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
            os.close(temp_fd)
            
            # Convert SVG to PNG
            cairosvg.svg2png(url=svg_path, write_to=temp_path)
            return temp_path
        except Exception as e:
            self.logger.error(f"Error converting SVG to PNG: {e}")
            raise
    
    def _prepare_image_for_printing(self, image_path: str) -> str:
        """Prepare image for printing, converting SVG if necessary"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Check if it's an SVG file
        if image_path.lower().endswith('.svg'):
            try:
                return self._convert_svg_to_png(image_path)
            except ImportError:
                self.logger.warning("SVG file detected but cairosvg not available. SVG support disabled.")
                raise FileNotFoundError("SVG files are not supported without cairosvg library")
        else:
            # For PNG/JPG, return the original path
            return image_path
    
    def print_image(self, image_path: str, printer_name: str) -> bool:
        """Print an image to the specified printer"""
        try:
            # Check if printer is available
            if not self.is_printer_available(printer_name):
                self.logger.error(f"Printer '{printer_name}' is not available")
                return False
            
            # Prepare image for printing
            print_path = self._prepare_image_for_printing(image_path)
            
            if self.is_windows:
                # Real Windows printing
                import win32api
                
                # Open image with PIL to ensure it's in the right format
                with Image.open(print_path) as img:
                    # Convert to RGB if necessary (some printers don't support RGBA)
                    if img.mode in ('RGBA', 'LA'):
                        # Create white background
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save to temporary file for printing
                    temp_fd, temp_print_path = tempfile.mkstemp(suffix='.png')
                    os.close(temp_fd)
                    img.save(temp_print_path, 'PNG')
                
                # Print using Windows API
                win32api.ShellExecute(
                    0,
                    "print",
                    temp_print_path,
                    f'/d:"{printer_name}"',
                    ".",
                    0
                )
                
                # Clean up temporary files
                try:
                    if print_path != image_path:  # Only delete if it was a converted SVG
                        os.unlink(print_path)
                    os.unlink(temp_print_path)
                except:
                    pass  # Ignore cleanup errors
                
                self.logger.info(f"Successfully sent print job for {image_path} to {printer_name}")
                return True
            else:
                # Mock printing for macOS development
                return self._mock_print(print_path, printer_name)
            
        except Exception as e:
            self.logger.error(f"Error printing {image_path} to {printer_name}: {e}")
            return False
    
    def _mock_print(self, image_path: str, printer_name: str) -> bool:
        """Mock printing functionality for development"""
        try:
            # Create a mock print file
            import time
            timestamp = int(time.time())
            filename = os.path.basename(image_path)
            name, ext = os.path.splitext(filename)
            mock_filename = f"{name}_printed_{timestamp}{ext}"
            mock_path = os.path.join(self.mock_print_dir, mock_filename)
            
            # Copy the image to mock print directory
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(mock_path, 'PNG')
            
            # Clean up converted SVG if it was created
            if image_path != image_path and image_path.endswith('.png'):
                try:
                    os.unlink(image_path)
                except:
                    pass
            
            self.logger.info(f"🎨 MOCK PRINT: '{os.path.basename(image_path)}' → '{printer_name}'")
            self.logger.info(f"📁 Saved to: {mock_path}")
            print(f"\n🎨 MOCK PRINT SUCCESS!")
            print(f"   📄 File: {os.path.basename(image_path)}")
            print(f"   🖨️  Printer: {printer_name}")
            print(f"   📁 Saved to: {mock_path}")
            print(f"   📂 Mock prints directory: {os.path.abspath(self.mock_print_dir)}\n")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in mock print: {e}")
            return False
    
    def test_print(self, printer_name: str) -> bool:
        """Test print a simple image to verify printer is working"""
        try:
            # Create a simple test image
            test_img = Image.new('RGB', (200, 100), color='white')
            temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
            os.close(temp_fd)
            test_img.save(temp_path, 'PNG')
            
            result = self.print_image(temp_path, printer_name)
            
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return result
        except Exception as e:
            self.logger.error(f"Error in test print: {e}")
            return False
