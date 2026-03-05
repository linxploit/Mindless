#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: BASE64 ENCODER/DECODER
Advanced Base64 Encoding/Decoding with Multiple Variants
Author: ICAT Project | Linxploit.xyz
"""

import base64
import json
import binascii
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Base64Tool:
    """Advanced Base64 encoding/decoding with multiple variants"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗  █████╗ ███████╗███████╗ ██████╗  ██████╗             ║
    ║  ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔════╝             ║
    ║  ██████╔╝███████║███████╗█████╗  ██║   ██║██║  ███╗            ║
    ║  ██╔══██╗██╔══██║╚════██║██╔══╝  ██║   ██║██║   ██║            ║
    ║  ██████╔╝██║  ██║███████║███████╗╚██████╔╝╚██████╔╝            ║
    ║  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝             ║
    ║  {Fore.GREEN}███████╗███╗   ██╗ ██████╗ ██████╗ ███████╗██████╗ ███████╗██████╗ {Fore.CYAN} ║
    ║  {Fore.GREEN}██╔════╝████╗  ██║██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗{Fore.CYAN} ║
    ║  {Fore.GREEN}█████╗  ██╔██╗ ██║██║   ██║██║  ██║█████╗  ██████╔╝█████╗  ██║  ██║{Fore.CYAN} ║
    ║  {Fore.GREEN}██╔══╝  ██║╚██╗██║██║   ██║██║  ██║██╔══╝  ██╔══██╗██╔══╝  ██║  ██║{Fore.CYAN} ║
    ║  {Fore.GREEN}███████╗██║ ╚████║╚██████╔╝██████╔╝███████╗██║  ██║███████╗██████╔╝{Fore.CYAN} ║
    ║  {Fore.GREEN}╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ {Fore.CYAN} ║
    ║                    {Fore.GREEN}BASE64 ENCODER/DECODER v2.0{Fore.CYAN}                  ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Base64 variants
    VARIANTS = {
        'standard': {
            'name': 'Standard Base64',
            'encode': base64.b64encode,
            'decode': base64.b64decode,
            'charset': 'A-Z a-z 0-9 + /',
            'padding': '='
        },
        'urlsafe': {
            'name': 'URL-Safe Base64',
            'encode': base64.urlsafe_b64encode,
            'decode': base64.urlsafe_b64decode,
            'charset': 'A-Z a-z 0-9 - _',
            'padding': '='
        },
        'base32': {
            'name': 'Base32',
            'encode': base64.b32encode,
            'decode': base64.b32decode,
            'charset': 'A-Z 2-7',
            'padding': '='
        },
        'base16': {
            'name': 'Base16 (Hex)',
            'encode': base64.b16encode,
            'decode': base64.b16decode,
            'charset': '0-9 A-F',
            'padding': 'none'
        },
        'base85': {
            'name': 'Base85 (ASCII85)',
            'encode': base64.a85encode,
            'decode': base64.a85decode,
            'charset': 'ASCII printable',
            'padding': 'none'
        },
    }
    
    def __init__(self):
        self.input_text = None
        self.input_bytes = None
        self.encoded_results = {}
        self.decoded_results = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.input_type = 'text'  # text, hex, base64, file
        self.input_size = 0
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def set_input(self, text, input_type='text'):
        """Set input text and convert to bytes"""
        self.input_text = text
        self.input_type = input_type
        self.input_size = len(text)
        
        # Convert to bytes based on input type
        if input_type == 'hex':
            try:
                # Remove spaces and convert hex to bytes
                clean_hex = text.replace(' ', '').replace('\n', '').replace('\r', '')
                self.input_bytes = bytes.fromhex(clean_hex)
            except ValueError as e:
                raise ValueError(f"Invalid hexadecimal input: {e}")
        elif input_type == 'base64':
            try:
                self.input_bytes = base64.b64decode(text)
            except:
                try:
                    self.input_bytes = base64.urlsafe_b64decode(text)
                except:
                    raise ValueError("Invalid Base64 input")
        else:
            # Default: treat as UTF-8 text
            self.input_bytes = text.encode('utf-8')
            
        return self.input_bytes
        
    def encode_all(self):
        """Encode input using all Base64 variants"""
        self.encoded_results = {}
        
        for key, variant in self.VARIANTS.items():
            try:
                encoded = variant['encode'](self.input_bytes)
                encoded_str = encoded.decode('ascii')
                self.encoded_results[key] = {
                    'name': variant['name'],
                    'encoded': encoded_str,
                    'length': len(encoded_str),
                    'charset': variant['charset'],
                    'padding': variant['padding']
                }
            except Exception as e:
                self.encoded_results[key] = {
                    'name': variant['name'],
                    'error': str(e)
                }
                
        return self.encoded_results
        
    def decode(self, encoded_str, variant='standard'):
        """Decode Base64 string using specified variant"""
        if variant not in self.VARIANTS:
            raise ValueError(f"Unknown variant: {variant}")
            
        variant_info = self.VARIANTS[variant]
        
        try:
            decoded = variant_info['decode'](encoded_str)
            
            # Try to decode as UTF-8
            try:
                decoded_text = decoded.decode('utf-8')
                is_text = True
            except UnicodeDecodeError:
                decoded_text = str(decoded)[2:-1]  # Binary representation
                is_text = False
                
            result = {
                'decoded_bytes': decoded,
                'decoded_text': decoded_text,
                'is_text': is_text,
                'length': len(decoded),
                'hex': decoded.hex()
            }
            
            return result
        except Exception as e:
            raise ValueError(f"Decoding failed: {e}")
            
    def detect_encoding(self, encoded_str):
        """Attempt to detect Base64 encoding variant"""
        results = {}
        
        for key, variant in self.VARIANTS.items():
            try:
                decoded = variant['decode'](encoded_str)
                # Try to decode as UTF-8
                try:
                    text = decoded.decode('utf-8')
                    is_valid = True
                except:
                    is_valid = True  # Binary data is still valid
                    
                results[key] = {
                    'success': True,
                    'decoded_length': len(decoded)
                }
            except:
                results[key] = {
                    'success': False
                }
                
        # Find successful decodings
        successful = [k for k, v in results.items() if v['success']]
        
        if successful:
            # Prefer standard or URL-safe if both work
            if 'standard' in successful:
                return 'standard'
            elif 'urlsafe' in successful:
                return 'urlsafe'
            else:
                return successful[0]
        else:
            return None
            
    def generate_report(self, mode='encode'):
        """Generate comprehensive encoding/decoding report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] BASE64 TOOL REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        if mode == 'encode':
            self._generate_encode_report()
        else:
            self._generate_decode_report()
            
    def _generate_encode_report(self):
        """Generate encoding report"""
        print(f"\n{Fore.WHITE}Input Type: {Fore.LIGHTGREEN_EX}{self.input_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Input Size: {Fore.LIGHTGREEN_EX}{self.input_size} characters{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Bytes: {Fore.LIGHTGREEN_EX}{len(self.input_bytes)} bytes{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ INPUT PREVIEW ============
        print(f"\n{Fore.CYAN}[ INPUT PREVIEW ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        preview = self.input_text[:100] + '...' if len(self.input_text) > 100 else self.input_text
        print(f"\n  {Fore.WHITE}{preview}{Style.RESET_ALL}")
        
        # Hex dump
        hex_preview = self.input_bytes[:20].hex()
        print(f"\n  {Fore.WHITE}Hex (first 20 bytes): {hex_preview}{Style.RESET_ALL}")
        
        # ============ ENCODING RESULTS ============
        print(f"\n{Fore.CYAN}[ ENCODING RESULTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
        
        for key, result in self.encoded_results.items():
            if 'error' in result:
                print(f"\n  {Fore.RED}[✗] {result['name']}{Style.RESET_ALL}")
                print(f"      └─ Error: {result['error']}")
            else:
                # Calculate overhead
                original_size = len(self.input_bytes)
                encoded_size = result['length']
                overhead = ((encoded_size - original_size) / original_size) * 100 if original_size > 0 else 0
                
                print(f"\n  {Fore.GREEN}[✓] {result['name']}{Style.RESET_ALL}")
                print(f"      ├─ Encoded: {Fore.CYAN}{result['encoded'][:80]}{'...' if len(result['encoded']) > 80 else ''}{Style.RESET_ALL}")
                print(f"      ├─ Length: {result['length']} characters")
                print(f"      ├─ Overhead: {overhead:.1f}%")
                print(f"      ├─ Charset: {result['charset']}")
                print(f"      └─ Padding: {result['padding']}")
                
                # Copy option
                print(f"      └─ Copy: {Fore.YELLOW}base64_tool.py --decode --{key} \"{result['encoded'][:30]}...\"{Style.RESET_ALL}")
                
    def _generate_decode_report(self):
        """Generate decoding report"""
        print(f"\n{Fore.WHITE}Decoded: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ DECODING RESULTS ============
        for variant, result in self.decoded_results.items():
            print(f"\n{Fore.CYAN}[ {self.VARIANTS[variant]['name']} DECODING ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            if 'error' in result:
                print(f"\n  {Fore.RED}[✗] Decoding failed{Style.RESET_ALL}")
                print(f"      └─ {result['error']}")
            else:
                print(f"\n  {Fore.GREEN}[✓] Successfully decoded{Style.RESET_ALL}")
                print(f"      ├─ Bytes: {result['length']} bytes")
                print(f"      ├─ Hex: {result['hex'][:50]}{'...' if len(result['hex']) > 50 else ''}")
                
                if result['is_text']:
                    print(f"      ├─ Text: {Fore.CYAN}{result['decoded_text'][:100]}{'...' if len(result['decoded_text']) > 100 else ''}{Style.RESET_ALL}")
                    print(f"      └─ Encoding: UTF-8")
                else:
                    print(f"      └─ Binary data - not valid UTF-8 text")
                    
    def export_report(self, filename=None, mode='encode'):
        """Export results to JSON"""
        if not filename:
            filename = f"base64_{mode}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'mode': mode,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'input_type': self.input_type,
            'input_size': self.input_size,
            'input_preview': self.input_text[:200] if self.input_text else None
        }
        
        if mode == 'encode':
            report['encoding_results'] = self.encoded_results
        else:
            report['decoding_results'] = self.decoded_results
            
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_encode(self):
        """Interactive encoding mode"""
        print(f"{Fore.GREEN}[*] Base64 Encoder initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multiple encoding variants supported{Style.RESET_ALL}\n")
        
        # Get input method
        print(f"{Fore.CYAN}Input Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Text string")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Hexadecimal")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Base64 (re-encode)")
        print(f"  {Fore.WHITE}[4]{Style.RESET_ALL} Load from file")
        
        choice = input(f"\n{Fore.YELLOW}[?] Select input type: {Style.RESET_ALL}").strip()
        
        input_text = ""
        input_type = "text"
        
        if choice == "1":
            input_text = input(f"{Fore.YELLOW}[?] Enter text to encode: {Style.RESET_ALL}").strip()
            input_type = "text"
        elif choice == "2":
            input_text = input(f"{Fore.YELLOW}[?] Enter hexadecimal string: {Style.RESET_ALL}").strip()
            input_type = "hex"
        elif choice == "3":
            input_text = input(f"{Fore.YELLOW}[?] Enter Base64 string: {Style.RESET_ALL}").strip()
            input_type = "base64"
        elif choice == "4":
            filename = input(f"{Fore.YELLOW}[?] Enter file path: {Style.RESET_ALL}").strip()
            try:
                with open(filename, 'rb') as f:
                    file_bytes = f.read()
                input_text = file_bytes.hex()
                input_type = "hex"
                print(f"{Fore.GREEN}[✓] Loaded {len(file_bytes)} bytes from {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        if not input_text:
            print(f"{Fore.RED}[✗] No input provided{Style.RESET_ALL}")
            return
            
        self.start_time = datetime.now()
        
        try:
            # Set input
            self.set_input(input_text, input_type)
            
            # Encode all variants
            self.encode_all()
            
        except ValueError as e:
            print(f"{Fore.RED}[✗] {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report(mode='encode')
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report(mode='encode')
            
        print(f"\n{Fore.GREEN}[✓] Encoding completed{Style.RESET_ALL}")
        
    def interactive_decode(self):
        """Interactive decoding mode"""
        print(f"{Fore.GREEN}[*] Base64 Decoder initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Automatic variant detection{Style.RESET_ALL}\n")
        
        # Get encoded string
        encoded = input(f"{Fore.YELLOW}[?] Enter Base64 string to decode: {Style.RESET_ALL}").strip()
        
        if not encoded:
            print(f"{Fore.RED}[✗] No input provided{Style.RESET_ALL}")
            return
            
        # Auto-detect encoding
        print(f"\n{Fore.CYAN}[*] Detecting encoding variant...{Style.RESET_ALL}")
        detected = self.detect_encoding(encoded)
        
        if detected:
            print(f"{Fore.GREEN}[✓] Detected variant: {self.VARIANTS[detected]['name']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Could not detect variant{Style.RESET_ALL}")
            
        self.start_time = datetime.now()
        
        # Try to decode with all variants
        self.decoded_results = {}
        
        for variant in self.VARIANTS.keys():
            try:
                result = self.decode(encoded, variant)
                self.decoded_results[variant] = result
            except Exception as e:
                self.decoded_results[variant] = {'error': str(e)}
                
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report(mode='decode')
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report(mode='decode')
            
        print(f"\n{Fore.GREEN}[✓] Decoding completed{Style.RESET_ALL}")
        
    def interactive_menu(self):
        """Interactive main menu"""
        print(f"{Fore.GREEN}[*] Base64 Tool initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced encoding/decoding utility{Style.RESET_ALL}\n")
        
        while True:
            print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Encode")
            print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Decode")
            print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Auto-detect & Decode")
            print(f"  {Fore.WHITE}[0]{Style.RESET_ALL} Back to main menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.interactive_encode()
            elif choice == "2":
                self.interactive_decode()
            elif choice == "3":
                self.interactive_decode()  # Auto-detect is built-in
            elif choice == "0":
                break
            else:
                print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")


def base64_encode(text=None):
    """Encode text to Base64"""
    tool = Base64Tool()
    tool.print_header()
    
    if text:
        tool.start_time = datetime.now()
        try:
            tool.set_input(text, 'text')
            tool.encode_all()
            tool.end_time = datetime.now()
            tool.generate_report(mode='encode')
        except Exception as e:
            print(f"{Fore.RED}[✗] Encoding failed: {e}{Style.RESET_ALL}")
    else:
        tool.interactive_menu()


def base64_decode(encoded=None):
    """Decode Base64 string"""
    tool = Base64Tool()
    tool.print_header()
    
    if encoded:
        tool.start_time = datetime.now()
        
        # Try to decode with all variants
        tool.decoded_results = {}
        for variant in tool.VARIANTS.keys():
            try:
                result = tool.decode(encoded, variant)
                tool.decoded_results[variant] = result
            except:
                tool.decoded_results[variant] = {'error': 'Decoding failed'}
                
        tool.end_time = datetime.now()
        tool.generate_report(mode='decode')
    else:
        tool.interactive_decode()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--encode':
            text = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else None
            base64_encode(text)
        elif sys.argv[1] == '--decode':
            encoded = sys.argv[2] if len(sys.argv) > 2 else None
            base64_decode(encoded)
        else:
            base64_encode(sys.argv[1])
    else:
        base64_encode()
