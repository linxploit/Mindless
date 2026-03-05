#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: URL TO QR CODE GENERATOR
Advanced QR Code Creation with Multiple Output Formats
Author: ICAT Project | Linxploit.xyz
"""

import qrcode
import os
import json
from datetime import datetime
from colorama import Fore, Style, init
from PIL import Image
import io
import base64

init(autoreset=True)

class QRCodeGenerator:
    """Advanced QR code generator with customization options"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██████╗     ████████╗ ██████╗     ██████╗ ██████╗     ║
    ║  ██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗    ║
    ║  ██████╔╝██████╔╝       ██║   ██║   ██║    ██████╔╝██████╔╝    ║
    ║  ██╔══██╗██╔══██╗       ██║   ██║▄▄ ██║    ██╔══██╗██╔══██╗    ║
    ║  ██║  ██║██║  ██║       ██║   ╚██████╔╝    ██║  ██║██║  ██║    ║
    ║  ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚══▀▀═╝     ╚═╝  ╚═╝╚═╝  ╚═╝    ║
    ║                    {Fore.GREEN}URL TO QR CODE GENERATOR v2.0{Fore.CYAN}               ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # QR Code versions and capacities
    QR_VERSIONS = {
        1: "21x21 - 25 alphanumeric",
        2: "25x25 - 47 alphanumeric",
        3: "29x29 - 77 alphanumeric",
        4: "33x33 - 114 alphanumeric",
        5: "37x37 - 154 alphanumeric",
        6: "41x41 - 195 alphanumeric",
        7: "45x45 - 224 alphanumeric",
        8: "49x49 - 279 alphanumeric",
        9: "53x53 - 335 alphanumeric",
        10: "57x57 - 395 alphanumeric",
    }
    
    # Error correction levels
    ERROR_CORRECTION = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    
    def __init__(self):
        self.url = None
        self.filename = None
        self.qr_image = None
        self.qr_code = None
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def validate_url(self, url):
        """Validate and normalize URL"""
        if not url:
            return False
            
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        self.url = url
        return True
        
    def generate_qr(self, 
                   url=None,
                   version=1,
                   box_size=10,
                   border=4,
                   error_correction='M',
                   fill_color='black',
                   back_color='white'):
        """Generate QR code with customization"""
        
        if url:
            self.url = url
            
        if not self.url:
            raise ValueError("No URL specified")
            
        # Configure QR code
        qr = qrcode.QRCode(
            version=version if version <= 10 else None,
            error_correction=self.ERROR_CORRECTION.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_M),
            box_size=box_size,
            border=border
        )
        
        # Add data
        qr.add_data(self.url)
        qr.make(fit=True)
        
        # Create image
        self.qr_code = qr
        self.qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        return self.qr_image
        
    def save_qr(self, filename=None, format='PNG'):
        """Save QR code to file"""
        if not self.qr_image:
            raise ValueError("No QR code generated")
            
        if not filename:
            # Generate filename from URL
            url_clean = self.url.replace('https://', '').replace('http://', '').replace('/', '_').replace('.', '_')
            filename = f"qr_{url_clean[:30]}_{self.scan_id}.{format.lower()}"
            
        self.filename = filename
        
        # Save in specified format
        if format.upper() == 'PNG':
            self.qr_image.save(filename)
        elif format.upper() == 'JPEG' or format.upper() == 'JPG':
            # Convert to RGB for JPEG
            rgb_image = self.qr_image.convert('RGB')
            rgb_image.save(filename, 'JPEG')
        elif format.upper() == 'BMP':
            self.qr_image.save(filename, 'BMP')
        elif format.upper() == 'PDF':
            # Save as PDF (simplified)
            self.qr_image.save(filename.replace('.pdf', '.png'), 'PNG')
            # In production, you'd use reportlab or similar
        else:
            self.qr_image.save(filename)
            
        return filename
        
    def get_base64(self):
        """Get QR code as base64 string"""
        if not self.qr_image:
            raise ValueError("No QR code generated")
            
        buffered = io.BytesIO()
        self.qr_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
        
    def get_ascii_representation(self):
        """Generate ASCII art representation of QR code"""
        if not self.qr_image:
            return ""
            
        # Resize for terminal display (max 80 chars width)
        width, height = self.qr_image.size
        aspect_ratio = height / width
        new_width = min(60, width)
        new_height = int(new_width * aspect_ratio * 0.5)  # Terminal characters are ~2x tall
        
        img = self.qr_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img = img.convert('L')  # Grayscale
        
        # ASCII characters from dark to light
        ascii_chars = '@%#*+=-:. '
        
        ascii_art = []
        for y in range(new_height):
            line = ''
            for x in range(new_width):
                pixel = img.getpixel((x, y))
                # Map pixel value to ASCII character
                char_index = int(pixel / 255 * (len(ascii_chars) - 1))
                line += ascii_chars[char_index]
            ascii_art.append(line)
            
        return '\n'.join(ascii_art)
        
    def generate_report(self):
        """Generate QR code generation report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] QR CODE GENERATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Generated: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Saved As: {Fore.LIGHTGREEN_EX}{self.filename}{Style.RESET_ALL}")
        
        # QR Code Specifications
        print(f"\n{Fore.CYAN}[ QR CODE SPECIFICATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.qr_code:
            version = self.qr_code.version
            box_size = self.qr_code.box_size
            border = self.qr_code.border
            
            print(f"\n  {Fore.WHITE}Version:{Style.RESET_ALL} {version} - {self.QR_VERSIONS.get(version, 'Custom')}")
            print(f"  {Fore.WHITE}Matrix Size:{Style.RESET_ALL} {version*4 + 17} x {version*4 + 17} pixels")
            print(f"  {Fore.WHITE}Box Size:{Style.RESET_ALL} {box_size} pixels")
            print(f"  {Fore.WHITE}Border:{Style.RESET_ALL} {border} modules")
            print(f"  {Fore.WHITE}Error Correction:{Style.RESET_ALL} {self.qr_code.error_correction}")
            print(f"  {Fore.WHITE}Data Capacity:{Style.RESET_ALL} {len(self.qr_code.data_cache[0]) if self.qr_code.data_cache else 0} characters")
            
        # Image Information
        if self.qr_image:
            width, height = self.qr_image.size
            format_type = self.filename.split('.')[-1].upper() if self.filename else 'PNG'
            file_size = os.path.getsize(self.filename) if self.filename and os.path.exists(self.filename) else 0
            
            print(f"\n{Fore.CYAN}[ IMAGE INFORMATION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}Dimensions:{Style.RESET_ALL} {width} x {height} pixels")
            print(f"  {Fore.WHITE}Format:{Style.RESET_ALL} {format_type}")
            if file_size > 0:
                size_kb = file_size / 1024
                size_mb = size_kb / 1024
                if size_mb > 1:
                    print(f"  {Fore.WHITE}File Size:{Style.RESET_ALL} {size_mb:.2f} MB")
                else:
                    print(f"  {Fore.WHITE}File Size:{Style.RESET_ALL} {size_kb:.2f} KB")
                    
        # ASCII Preview
        print(f"\n{Fore.CYAN}[ ASCII PREVIEW ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}{self.get_ascii_representation()}{Style.RESET_ALL}")
        print(f"\n  {Fore.YELLOW}[!] Preview scaled for terminal display{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def interactive_generate(self):
        """Interactive QR code generation mode"""
        print(f"{Fore.GREEN}[*] URL to QR Code Generator initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Create QR codes from URLs, text, or data{Style.RESET_ALL}\n")
        
        # Get URL
        url_input = input(f"{Fore.YELLOW}[?] Enter URL or text to encode: {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No input specified{Style.RESET_ALL}")
            return
            
        if not self.validate_url(url_input):
            print(f"{Fore.RED}[✗] Invalid URL format{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}QR Code Customization:{Style.RESET_ALL}")
        
        # Version
        print(f"\n{Fore.WHITE}QR Version (1-10, higher = more data):{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}1-2:{Style.RESET_ALL} Small (URLs, short text)")
        print(f"  {Fore.WHITE}3-5:{Style.RESET_ALL} Medium (standard URLs)")
        print(f"  {Fore.WHITE}6-10:{Style.RESET_ALL} Large (long text, vCards)")
        
        try:
            version = int(input(f"{Fore.YELLOW}[?] Version (default 3): {Style.RESET_ALL}").strip() or "3")
            version = max(1, min(10, version))
        except:
            version = 3
            
        # Box size
        try:
            box_size = int(input(f"{Fore.YELLOW}[?] Box size in pixels (default 10): {Style.RESET_ALL}").strip() or "10")
            box_size = max(1, min(50, box_size))
        except:
            box_size = 10
            
        # Error correction
        print(f"\n{Fore.WHITE}Error Correction Level:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}L:{Style.RESET_ALL} 7% recovery - Smallest size")
        print(f"  {Fore.WHITE}M:{Style.RESET_ALL} 15% recovery - Default")
        print(f"  {Fore.WHITE}Q:{Style.RESET_ALL} 25% recovery - Recommended")
        print(f"  {Fore.WHITE}H:{Style.RESET_ALL} 30% recovery - Largest size")
        
        ec = input(f"{Fore.YELLOW}[?] Error correction (L/M/Q/H, default Q): {Style.RESET_ALL}").strip().upper() or "Q"
        if ec not in ['L', 'M', 'Q', 'H']:
            ec = 'Q'
            
        # Colors
        print(f"\n{Fore.WHITE}Color Options:{Style.RESET_ALL}")
        fg = input(f"{Fore.YELLOW}[?] Foreground color (default black): {Style.RESET_ALL}").strip() or "black"
        bg = input(f"{Fore.YELLOW}[?] Background color (default white): {Style.RESET_ALL}").strip() or "white"
        
        # Format
        print(f"\n{Fore.WHITE}Output Format:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}PNG:{Style.RESET_ALL} Standard format (default)")
        print(f"  {Fore.WHITE}JPG:{Style.RESET_ALL} Compressed format")
        print(f"  {Fore.WHITE}BMP:{Style.RESET_ALL} Uncompressed bitmap")
        
        format_type = input(f"{Fore.YELLOW}[?] Format (PNG/JPG/BMP, default PNG): {Style.RESET_ALL}").strip().upper() or "PNG"
        if format_type not in ['PNG', 'JPG', 'JPEG', 'BMP']:
            format_type = 'PNG'
            
        # Filename
        filename = input(f"{Fore.YELLOW}[?] Output filename (Enter for auto-generate): {Style.RESET_ALL}").strip()
        
        self.start_time = datetime.now()
        
        # Generate QR code
        try:
            print(f"\n{Fore.CYAN}[*] Generating QR code...{Style.RESET_ALL}")
            self.generate_qr(
                version=version,
                box_size=box_size,
                border=4,
                error_correction=ec,
                fill_color=fg,
                back_color=bg
            )
            
            print(f"{Fore.CYAN}[*] Saving QR code...{Style.RESET_ALL}")
            self.save_qr(filename=filename if filename else None, format=format_type)
            
            print(f"{Fore.CYAN}[*] Displaying preview...{Style.RESET_ALL}")
            self.qr_image.show()  # Open with default image viewer
            
        except Exception as e:
            print(f"{Fore.RED}[✗] QR code generation failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        print(f"\n{Fore.GREEN}[✓] QR code generated successfully: {self.filename}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] File saved to current directory{Style.RESET_ALL}")


def url_to_qr(url=None, filename=None, save=True):
    """Main entry point for CLI compatibility"""
    generator = QRCodeGenerator()
    
    # Display banner
    generator.print_header()
    
    if url:
        # Direct generation mode
        if not generator.validate_url(url):
            print(f"{Fore.RED}[✗] Invalid URL format{Style.RESET_ALL}")
            return
            
        generator.start_time = datetime.now()
        
        try:
            generator.generate_qr(url=url, version=3, box_size=10, error_correction='Q')
            
            if save:
                if filename:
                    generator.save_qr(filename)
                else:
                    generator.save_qr()
                    
            generator.end_time = datetime.now()
            generator.generate_report()
            
            if save:
                print(f"\n{Fore.GREEN}[✓] QR code saved to: {generator.filename}{Style.RESET_ALL}")
                
            # Show image
            generator.qr_image.show()
            
        except Exception as e:
            print(f"{Fore.RED}[✗] QR code generation failed: {e}{Style.RESET_ALL}")
            
    else:
        # Interactive mode
        generator.interactive_generate()


if __name__ == "__main__":
    url_to_qr()
