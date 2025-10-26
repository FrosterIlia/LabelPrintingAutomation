import os
import tempfile
import logging
import platform
from typing import List
from PIL import Image, ImageWin


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
                for printer_info in win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
                ):
                    printers.append(printer_info[2])  # printer_info[2] is the printer name
                return printers
            except Exception as e:
                self.logger.error(f"Error enumerating printers: {e}")
                return self.mock_printers
        else:
            if not hasattr(self, '_mock_logged'):
                self.logger.info("Using mock printers for macOS development")
                self._mock_logged = True
            return self.mock_printers

    def is_printer_available(self, printer_name: str) -> bool:
        """Check if a specific printer is available"""
        available_printers = self.get_available_printers()
        return printer_name in available_printers

    def _convert_svg_to_png(self, svg_path: str) -> str:
        """Convert SVG file to temporary PNG file using svglib + reportlab (no Cairo)."""
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"Image file not found: {svg_path}")

        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM
        except ImportError as e:
            self.logger.error(f"svglib/reportlab missing: {e}")
            raise ImportError(
                "SVG support requires svglib and reportlab. Install: pip install svglib reportlab"
            )

        try:
            drawing = svg2rlg(svg_path)
            if drawing is None:
                raise ValueError("Failed to parse SVG (invalid or unsupported).")

            # Create temp PNG path
            temp_fd, temp_path = tempfile.mkstemp(suffix=".png")
            os.close(temp_fd)  # close the handle immediately (Windows lock avoidance)

            # Render to PNG (ReportLab uses Pillow internally; no Cairo)
            # You can tweak dpi if you need crisper labels (e.g., dpi=300)
            renderPM.drawToFile(drawing, temp_path, fmt="PNG")

            # Sanity check
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                raise ValueError("PNG render produced an empty file.")

            self.logger.info("✅ SVG converted using svglib+reportlab")
            return temp_path

        except Exception as e:
            self.logger.error(f"SVG conversion failed: {e}")
            raise FileNotFoundError(f"Failed to convert SVG file '{svg_path}': {e}")

    def _prepare_image_for_printing(self, image_path: str) -> str:
        """Prepare image for printing, converting SVG if necessary"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        if image_path.lower().endswith('.svg'):
            try:
                return self._convert_svg_to_png(image_path)
            except ImportError:
                self.logger.warning("SVG file detected but svglib/reportlab not available. SVG support disabled.")
                raise FileNotFoundError("SVG files are not supported without svglib and reportlab libraries")
        else:
            return image_path

    def _direct_print_windows(self, image_path: str, printer_name: str, orientation: str = "portrait") -> bool:
        """Direct silent printing for Windows (no dialog boxes)"""
        try:
            import win32print
            import win32ui

            # Open printer
            hprinter = win32print.OpenPrinter(printer_name)
            printer_dc = win32ui.CreateDC()
            printer_dc.CreatePrinterDC(printer_name)

            # Get printable area in pixels
            HORZRES = printer_dc.GetDeviceCaps(8)
            VERTRES = printer_dc.GetDeviceCaps(10)
            printable_area = (HORZRES, VERTRES)

            # Start document
            printer_dc.StartDoc(image_path)
            printer_dc.StartPage()

            # Load and prep image
            img = Image.open(image_path)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Rotate image if landscape
            if orientation.lower() == "landscape":
                img = img.rotate(-90, expand=True)  # rotate clockwise

            # Scale image to fit printable area
            img_width, img_height = img.size
            scale = min(printable_area[0] / img_width, printable_area[1] / img_height)
            scaled_width = int(img_width * scale)
            scaled_height = int(img_height * scale)

            # Center on page
            left = int((printable_area[0] - scaled_width) / 2)
            top = int((printable_area[1] - scaled_height) / 2)
            box = (left, top, left + scaled_width, top + scaled_height)

            # Draw to printer DC
            dib = ImageWin.Dib(img)
            hdc = printer_dc.GetHandleOutput()

            # Try stretch_draw first (newer Pillow)
            if hasattr(dib, "stretch_draw"):
                dib.stretch_draw(hdc, box)
            else:
                # Some Pillow versions only have draw(hdc, box)
                try:
                    dib.draw(hdc, box)
                except TypeError:
                    # Fallback if draw only accepts 1 arg
                    dib.draw(hdc)

            # Finish print job
            printer_dc.EndPage()
            printer_dc.EndDoc()
            printer_dc.DeleteDC()
            win32print.ClosePrinter(hprinter)

            print(f"\n🖨️  SILENT PRINT SUCCESS!")
            print(f"   📄 File: {os.path.basename(image_path)}")
            print(f"   🖨️  Printer: {printer_name}")
            print(f"   📐 Orientation: {orientation.title()}")
            print(f"   ✅ Print job sent automatically.\n")
            return True

        except Exception as e:
            self.logger.error(f"Direct Windows print failed: {e}")
            return False


    def _mock_print(self, image_path: str, printer_name: str, orientation: str = "portrait") -> bool:
        """Mock printing functionality for development"""
        try:
            import time
            timestamp = int(time.time())
            filename = os.path.basename(image_path)
            name, ext = os.path.splitext(filename)
            mock_filename = f"{name}_printed_{timestamp}_{orientation}{ext}"
            mock_path = os.path.join(self.mock_print_dir, mock_filename)

            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Rotate image if landscape for mock printing
                if orientation.lower() == "landscape":
                    img = img.rotate(90, expand=True)

                img.save(mock_path, 'PNG')

            print(f"\n🎨 MOCK PRINT SUCCESS!")
            print(f"   📄 File: {os.path.basename(image_path)}")
            print(f"   🖨️  Printer: {printer_name}")
            print(f"   📐 Orientation: {orientation.title()}")
            print(f"   📁 Saved to: {mock_path}")
            print(f"   📂 Mock prints directory: {os.path.abspath(self.mock_print_dir)}\n")

            return True

        except Exception as e:
            self.logger.error(f"Error in mock print: {e}")
            return False

    def print_image(self, image_path: str, printer_name: str, orientation: str = "portrait") -> bool:
        """Print an image to the specified printer"""
        try:
            if not self.is_printer_available(printer_name):
                self.logger.error(f"Printer '{printer_name}' is not available")
                return False

            print_path = self._prepare_image_for_printing(image_path)

            if self.is_windows:
                success = self._direct_print_windows(print_path, printer_name, orientation)
            else:
                success = self._mock_print(print_path, printer_name, orientation)

            # Clean up temporary file if it was a converted SVG
            if print_path != image_path and os.path.exists(print_path):
                try:
                    os.unlink(print_path)
                except Exception:
                    pass

            return success

        except Exception as e:
            self.logger.error(f"Error printing {image_path} to {printer_name}: {e}")
            return False

    def test_print(self, printer_name: str) -> bool:
        """Test print a simple image to verify printer is working"""
        try:
            test_img = Image.new('RGB', (200, 100), color='white')
            temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
            os.close(temp_fd)
            test_img.save(temp_path, 'PNG')

            result = self.print_image(temp_path, printer_name, "portrait")

            try:
                os.unlink(temp_path)
            except Exception:
                pass

            return result
        except Exception as e:
            self.logger.error(f"Error in test print: {e}")
            return False