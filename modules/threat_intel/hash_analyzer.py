#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: HASH ANALYZER
Advanced Cryptographic Hash Identification & Analysis
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import hashlib
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class HashAnalyzer:
    """Advanced hash identification and analysis tool"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗  ██╗ █████╗ ███████╗██╗  ██╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗███████╗███████╗██╗  ██╗ ║
    ║  ██║  ██║██╔══██╗██╔════╝██║  ██║    ██╔══██╗████╗  ██║██╔══██╗██║ ██╔╝██╔════╝██╔════╝██║  ██║ ║
    ║  ███████║███████║███████╗███████║    ███████║██╔██╗ ██║███████║█████╔╝ █████╗  ███████╗███████║ ║
    ║  ██╔══██║██╔══██║╚════██║██╔══██║    ██╔══██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ╚════██║██╔══██║ ║
    ║  ██║  ██║██║  ██║███████║██║  ██║    ██║  ██║██║ ╚████║██║  ██║██║  ██╗███████╗███████║██║  ██║ ║
    ║  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ║
    ║                    {Fore.CYAN}HASH ANALYZER & IDENTIFIER v2.0{Fore.RED}                 ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Hash signature database
    HASH_SIGNATURES = {
        # MD Family
        'MD2': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'Message Digest 2 - deprecated'},
        'MD4': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'Message Digest 4 - deprecated'},
        'MD5': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'Message Digest 5 - insecure, collisions found'},
        
        # SHA Family
        'SHA-1': {'length': 40, 'pattern': r'^[a-f0-9]{40}$', 'bits': 160, 'description': 'Secure Hash Algorithm 1 - deprecated, collisions found'},
        'SHA-224': {'length': 56, 'pattern': r'^[a-f0-9]{56}$', 'bits': 224, 'description': 'SHA-2 family, 224-bit'},
        'SHA-256': {'length': 64, 'pattern': r'^[a-f0-9]{64}$', 'bits': 256, 'description': 'SHA-2 family, 256-bit - currently secure'},
        'SHA-384': {'length': 96, 'pattern': r'^[a-f0-9]{96}$', 'bits': 384, 'description': 'SHA-2 family, 384-bit'},
        'SHA-512': {'length': 128, 'pattern': r'^[a-f0-9]{128}$', 'bits': 512, 'description': 'SHA-2 family, 512-bit'},
        'SHA-512/224': {'length': 56, 'pattern': r'^[a-f0-9]{56}$', 'bits': 224, 'description': 'SHA-2 family, truncated'},
        'SHA-512/256': {'length': 64, 'pattern': r'^[a-f0-9]{64}$', 'bits': 256, 'description': 'SHA-2 family, truncated'},
        
        # SHA-3 Family
        'SHA3-224': {'length': 56, 'pattern': r'^[a-f0-9]{56}$', 'bits': 224, 'description': 'SHA-3 family, 224-bit'},
        'SHA3-256': {'length': 64, 'pattern': r'^[a-f0-9]{64}$', 'bits': 256, 'description': 'SHA-3 family, 256-bit'},
        'SHA3-384': {'length': 96, 'pattern': r'^[a-f0-9]{96}$', 'bits': 384, 'description': 'SHA-3 family, 384-bit'},
        'SHA3-512': {'length': 128, 'pattern': r'^[a-f0-9]{128}$', 'bits': 512, 'description': 'SHA-3 family, 512-bit'},
        
        # BLAKE Family
        'BLAKE2b': {'length': 128, 'pattern': r'^[a-f0-9]{128}$', 'bits': 512, 'description': 'BLAKE2b - optimized for 64-bit platforms'},
        'BLAKE2s': {'length': 64, 'pattern': r'^[a-f0-9]{64}$', 'bits': 256, 'description': 'BLAKE2s - optimized for 8-32 bit platforms'},
        
        # RIPEMD Family
        'RIPEMD-128': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'RACE Integrity Primitives Evaluation Message Digest'},
        'RIPEMD-160': {'length': 40, 'pattern': r'^[a-f0-9]{40}$', 'bits': 160, 'description': 'RIPEMD-160 - used in Bitcoin'},
        'RIPEMD-256': {'length': 64, 'pattern': r'^[a-f0-9]{64}$', 'bits': 256, 'description': 'RIPEMD-256'},
        'RIPEMD-320': {'length': 80, 'pattern': r'^[a-f0-9]{80}$', 'bits': 320, 'description': 'RIPEMD-320'},
        
        # CRC Family
        'CRC32': {'length': 8, 'pattern': r'^[a-f0-9]{8}$', 'bits': 32, 'description': 'Cyclic Redundancy Check - not cryptographic'},
        'CRC64': {'length': 16, 'pattern': r'^[a-f0-9]{16}$', 'bits': 64, 'description': 'Cyclic Redundancy Check - not cryptographic'},
        
        # NTLM
        'NTLM': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'Windows NTLM hash'},
        
        # MySQL
        'MySQL': {'length': 16, 'pattern': r'^[a-f0-9]{16}$', 'bits': 64, 'description': 'MySQL pre-4.1 password hash'},
        'MySQL5': {'length': 40, 'pattern': r'^[a-f0-9]{40}$', 'bits': 160, 'description': 'MySQL 5 password hash (SHA-1)'},
        
        # PostgreSQL
        'PostgreSQL': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'PostgreSQL MD5 password hash'},
        
        # BSD
        'BSD_NT': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'BSD NT-style hash'},
        
        # Others
        'LM': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'Windows LM hash - very weak'},
        'Double MD5': {'length': 32, 'pattern': r'^[a-f0-9]{32}$', 'bits': 128, 'description': 'MD5(MD5($pass))'},
        'MD5 Crypt': {'length': 34, 'pattern': r'^\$1\$[a-zA-Z0-9./]{1,8}\$[a-zA-Z0-9./]{22}$', 'description': 'MD5-based crypt (Unix)'},
        'SHA256 Crypt': {'length': 63, 'pattern': r'^\$5\$[a-zA-Z0-9./]{1,16}\$[a-zA-Z0-9./]{43}$', 'description': 'SHA-256 crypt (Unix)'},
        'SHA512 Crypt': {'length': 106, 'pattern': r'^\$6\$[a-zA-Z0-9./]{1,16}\$[a-zA-Z0-9./]{86}$', 'description': 'SHA-512 crypt (Unix)'},
        'bcrypt': {'length': 60, 'pattern': r'^\$2[ayb]\$[0-9]{2}\$[a-zA-Z0-9./]{53}$', 'description': 'bcrypt - Blowfish-based hash'},
        'scrypt': {'length': 116, 'pattern': r'^\$7\$[a-zA-Z0-9./]+$', 'description': 'scrypt - memory-hard function'},
    }
    
    # Uppercase hash patterns
    UPPERCASE_HASHES = ['NTLM', 'MySQL', 'PostgreSQL', 'BSD_NT', 'LM']
    
    def __init__(self):
        self.hash_string = None
        self.hash_length = 0
        self.possible_matches = []
        self.exact_match = None
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.hash_samples = {}
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_hash(self, hash_string):
        """Normalize hash string for analysis"""
        self.hash_string = hash_string.strip()
        self.hash_length = len(self.hash_string)
        
        # Convert to lowercase for pattern matching (except for uppercase-specific hashes)
        self.hash_lower = self.hash_string.lower()
        
        return self.hash_string
        
    def identify_hash(self):
        """Identify possible hash types"""
        self.possible_matches = []
        
        # Check for obvious non-hash
        if not re.match(r'^[a-fA-F0-9$./]+$', self.hash_string):
            self.possible_matches.append({
                'hash_type': 'UNKNOWN',
                'confidence': 'LOW',
                'reason': 'Contains non-hexadecimal characters',
                'description': 'May be encoded or non-hash data'
            })
            return self.possible_matches
            
        # Check each signature
        for hash_type, signature in self.HASH_SIGNATURES.items():
            # Check length first (fast filter)
            if 'length' in signature and self.hash_length != signature['length']:
                continue
                
            # Check pattern
            if 'pattern' in signature:
                # For uppercase hashes, test original case
                if hash_type in self.UPPERCASE_HASHES:
                    if re.match(signature['pattern'], self.hash_string):
                        self.add_match(hash_type, signature, 'HIGH')
                # For lowercase hashes, test lowercase version
                else:
                    if re.match(signature['pattern'], self.hash_lower):
                        self.add_match(hash_type, signature, 'HIGH')
                        
        # If no matches found
        if not self.possible_matches:
            self.possible_matches.append({
                'hash_type': 'UNKNOWN',
                'confidence': 'LOW',
                'reason': 'No matching hash signature found',
                'description': 'Unknown hash format or custom implementation',
                'length': self.hash_length,
                'bits': self.hash_length * 4 if self.hash_length else 0
            })
            
        return self.possible_matches
        
    def add_match(self, hash_type, signature, confidence):
        """Add a matched hash type"""
        match = {
            'hash_type': hash_type,
            'confidence': confidence,
            'length': signature.get('length', self.hash_length),
            'bits': signature.get('bits', self.hash_length * 4),
            'description': signature.get('description', 'No description available'),
            'security_status': self.get_security_status(hash_type)
        }
        self.possible_matches.append(match)
        
        # Check for exact match (first match considered primary)
        if not self.exact_match:
            self.exact_match = match
            
    def get_security_status(self, hash_type):
        """Get security status of hash algorithm"""
        insecure_hashes = ['MD2', 'MD4', 'MD5', 'SHA-1', 'LM', 'NTLM', 'CRC32', 'CRC64', 'MySQL', 'PostgreSQL']
        deprecated_hashes = ['RIPEMD-128', 'RIPEMD-160', 'BSD_NT']
        
        if hash_type in insecure_hashes:
            return 'INSECURE - Do not use for security'
        elif hash_type in deprecated_hashes:
            return 'DEPRECATED - Consider upgrading'
        elif 'SHA-2' in hash_type or 'SHA-3' in hash_type or 'BLAKE' in hash_type:
            return 'SECURE - Currently considered safe'
        else:
            return 'UNKNOWN - Verify algorithm strength'
            
    def compute_hash_samples(self):
        """Compute common hash types from sample text"""
        if not self.hash_string or len(self.hash_string) > 64:
            return
            
        # Try to see if this hash is a known sample
        self.hash_samples = {
            'MD5': hashlib.md5(b'sample').hexdigest(),
            'SHA-1': hashlib.sha1(b'sample').hexdigest(),
            'SHA-256': hashlib.sha256(b'sample').hexdigest(),
            'SHA-512': hashlib.sha512(b'sample').hexdigest(),
        }
        
    def analyze_hash_strength(self):
        """Analyze the cryptographic strength of the hash"""
        if not self.exact_match:
            return None
            
        hash_type = self.exact_match['hash_type']
        bits = self.exact_match.get('bits', 0)
        
        analysis = {
            'hash_type': hash_type,
            'bits': bits,
            'collision_resistance': 'Good' if bits >= 256 else 'Weak' if bits >= 128 else 'Very Weak',
            'preimage_resistance': 'Good' if bits >= 256 else 'Moderate' if bits >= 128 else 'Poor',
            'recommended': bits >= 256,
            'cryptographic': hash_type not in ['CRC32', 'CRC64']
        }
        
        return analysis
        
    def generate_report(self):
        """Generate comprehensive hash analysis report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] HASH ANALYSIS REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Analyzed Hash: {Fore.LIGHTGREEN_EX}{self.hash_string}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Hash Length: {Fore.LIGHTGREEN_EX}{self.hash_length} characters{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ HASH IDENTIFICATION ============
        print(f"\n{Fore.CYAN}[ HASH IDENTIFICATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.exact_match:
            hash_type = self.exact_match['hash_type']
            bits = self.exact_match.get('bits', 'Unknown')
            description = self.exact_match.get('description', '')
            security = self.exact_match.get('security_status', '')
            
            # Color code based on security
            if 'INSECURE' in security or 'DEPRECATED' in security:
                type_color = Fore.RED
            elif 'SECURE' in security:
                type_color = Fore.GREEN
            else:
                type_color = Fore.YELLOW
                
            print(f"\n  {Fore.WHITE}Primary Match:{Style.RESET_ALL}")
            print(f"    ├─ Algorithm: {type_color}{hash_type}{Style.RESET_ALL}")
            print(f"    ├─ Bit Length: {Fore.WHITE}{bits} bits{Style.RESET_ALL}")
            print(f"    ├─ Description: {Fore.WHITE}{description}{Style.RESET_ALL}")
            print(f"    └─ Security: {type_color}{security}{Style.RESET_ALL}")
            
        # ============ POSSIBLE MATCHES ============
        if len(self.possible_matches) > 1:
            print(f"\n{Fore.CYAN}[ POSSIBLE MATCHES ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}This hash could be one of:{Style.RESET_ALL}")
            
            for i, match in enumerate(self.possible_matches[:5], 1):
                if match['hash_type'] == 'UNKNOWN':
                    continue
                    
                if 'INSECURE' in match.get('security_status', ''):
                    status_color = Fore.RED
                elif 'DEPRECATED' in match.get('security_status', ''):
                    status_color = Fore.YELLOW
                elif 'SECURE' in match.get('security_status', ''):
                    status_color = Fore.GREEN
                else:
                    status_color = Fore.WHITE
                    
                print(f"\n    {i}. {status_color}{match['hash_type']}{Style.RESET_ALL}")
                print(f"       ├─ Bits: {match.get('bits', 'Unknown')}")
                print(f"       ├─ Confidence: {Fore.WHITE}{match['confidence']}{Style.RESET_ALL}")
                print(f"       └─ Description: {Fore.WHITE}{match['description']}{Style.RESET_ALL}")
                
        # ============ SECURITY ANALYSIS ============
        strength = self.analyze_hash_strength()
        
        if strength:
            print(f"\n{Fore.CYAN}[ SECURITY ANALYSIS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            collision_color = Fore.GREEN if 'Good' in strength['collision_resistance'] else Fore.RED if 'Weak' in strength['collision_resistance'] else Fore.YELLOW
            preimage_color = Fore.GREEN if 'Good' in strength['preimage_resistance'] else Fore.RED if 'Poor' in strength['preimage_resistance'] else Fore.YELLOW
            
            print(f"\n  {Fore.WHITE}Collision Resistance:{Style.RESET_ALL} {collision_color}{strength['collision_resistance']}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Preimage Resistance:{Style.RESET_ALL} {preimage_color}{strength['preimage_resistance']}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Cryptographic Hash:{Style.RESET_ALL} {Fore.GREEN if strength['cryptographic'] else Fore.RED}{strength['cryptographic']}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Recommended:{Style.RESET_ALL} {Fore.GREEN if strength['recommended'] else Fore.RED}{strength['recommended']}{Style.RESET_ALL}")
            
        # ============ USAGE CONTEXT ============
        print(f"\n{Fore.CYAN}[ TYPICAL USAGE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.exact_match:
            hash_type = self.exact_match['hash_type']
            
            usage_map = {
                'MD5': 'Checksums, legacy applications, malware hashes',
                'SHA-1': 'Git commits, legacy SSL certs, malware hashes',
                'SHA-256': 'SSL/TLS certificates, digital signatures, file integrity',
                'SHA-512': 'High-security applications, password hashing',
                'NTLM': 'Windows authentication, password cracking targets',
                'LM': 'Legacy Windows authentication (pre-Vista)',
                'bcrypt': 'Password storage, web applications',
                'MySQL5': 'MySQL user passwords',
                'PostgreSQL': 'PostgreSQL user passwords',
            }
            
            usage = usage_map.get(hash_type, 'General purpose hashing')
            print(f"\n  {Fore.WHITE}→ {usage}{Style.RESET_ALL}")
            
        # ============ CRACKING INFORMATION ============
        if self.exact_match and self.exact_match['hash_type'] not in ['SHA-256', 'SHA-512', 'SHA3-256', 'SHA3-512', 'bcrypt', 'scrypt']:
            print(f"\n{Fore.CYAN}[ CRACKING INFORMATION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            hash_type = self.exact_match['hash_type']
            
            if hash_type in ['MD5', 'NTLM', 'LM']:
                print(f"\n  {Fore.RED}[!] This hash type is EASILY CRACKABLE{Style.RESET_ALL}")
                print(f"      └─ Rate: billions/sec on modern GPU")
                print(f"      └─ Tool: hashcat -m 0 (MD5), -m 1000 (NTLM)")
            elif hash_type in ['SHA-1', 'MySQL5', 'PostgreSQL']:
                print(f"\n  {Fore.YELLOW}[!] This hash type is CRACKABLE{Style.RESET_ALL}")
                print(f"      └─ Rate: millions/sec on modern GPU")
                print(f"      └─ Tool: hashcat -m 100 (SHA-1)")
            elif hash_type in ['SHA-256', 'SHA-512']:
                print(f"\n  {Fore.YELLOW}[!] This hash type is SLOW to crack{Style.RESET_ALL}")
                print(f"      └─ Rate: thousands/sec on modern GPU")
                print(f"      └─ Still feasible for weak passwords")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.exact_match:
            hash_type = self.exact_match['hash_type']
            
            if hash_type in ['MD5', 'SHA-1', 'LM', 'NTLM', 'CRC32']:
                print(f"""
  {Fore.RED}1. DO NOT USE {hash_type} for security purposes{Style.RESET_ALL}
  {Fore.RED}2. Upgrade to SHA-256, SHA-3, or bcrypt{Style.RESET_ALL}
  {Fore.RED}3. Use salted hashes for password storage{Style.RESET_ALL}
  {Fore.RED}4. Consider key derivation functions (PBKDF2, scrypt, Argon2){Style.RESET_ALL}
                """)
            elif hash_type in ['SHA-256', 'SHA-512']:
                print(f"""
  {Fore.GREEN}1. {hash_type} is currently considered secure{Style.RESET_ALL}
  {Fore.GREEN}2. Use with salts for password storage{Style.RESET_ALL}
  {Fore.GREEN}3. Consider key stretching for password hashing{Style.RESET_ALL}
  {Fore.GREEN}4. SHA-3 provides alternative if needed{Style.RESET_ALL}
                """)
            elif hash_type in ['bcrypt', 'scrypt']:
                print(f"""
  {Fore.GREEN}1. {hash_type} is excellent for password storage{Style.RESET_ALL}
  {Fore.GREEN}2. Ensure work factor is appropriate{Style.RESET_ALL}
  {Fore.GREEN}3. Consider Argon2 for new implementations{Style.RESET_ALL}
                """)
                
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"hash_analysis_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'hash': self.hash_string,
            'hash_length': self.hash_length,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'exact_match': self.exact_match,
            'possible_matches': self.possible_matches,
            'security_analysis': self.analyze_hash_strength()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive hash analysis mode"""
        print(f"{Fore.GREEN}[*] Hash Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Cryptographic hash identification and security analysis{Style.RESET_ALL}\n")
        
        # Get target
        hash_input = input(f"{Fore.YELLOW}[?] Enter hash to analyze: {Style.RESET_ALL}").strip()
        
        if not hash_input:
            print(f"{Fore.RED}[✗] No hash specified{Style.RESET_ALL}")
            return
            
        self.normalize_hash(hash_input)
        
        print(f"\n{Fore.YELLOW}[*] Analyzing hash...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Identify hash
        self.identify_hash()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Hash analysis completed{Style.RESET_ALL}")


def hash_analysis(hash_str=None):
    """Main entry point for CLI compatibility"""
    analyzer = HashAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if hash_str:
        # Direct scan mode
        analyzer.normalize_hash(hash_str)
        analyzer.start_time = datetime.now()
        analyzer.identify_hash()
        analyzer.end_time = datetime.now()
        analyzer.generate_report()
    else:
        # Interactive mode
        analyzer.interactive_scan()


if __name__ == "__main__":
    hash_analysis()
