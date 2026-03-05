#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: PASSWORD STRENGTH ANALYZER
Advanced Password Security & Complexity Assessment
Author: ICAT Project | Linxploit.xyz
"""

import re
import math
import json
import hashlib
import requests
from datetime import datetime
from colorama import Fore, Style, init
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class PasswordStrengthAnalyzer:
    """Advanced password strength analyzer with breach checking"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗      ║
    ║  ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗     ║
    ║  ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║     ║
    ║  ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║     ║
    ║  ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝     ║
    ║  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝      ║
    ║                    {Fore.GREEN}███████╗████████╗██████╗ ███████╗███╗   ██╗ ██████╗ ████████╗██╗  ██╗{Fore.CYAN} ║
    ║                    {Fore.GREEN}██╔════╝╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔═══██╗╚══██╔══╝██║  ██║{Fore.CYAN} ║
    ║                    {Fore.GREEN}███████╗   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║   ██║   ██║   ███████║{Fore.CYAN} ║
    ║                    {Fore.GREEN}╚════██║   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║   ██║   ██╔══██║{Fore.CYAN} ║
    ║                    {Fore.GREEN}███████║   ██║   ██║  ██║███████╗██║ ╚████║╚██████╔╝   ██║   ██║  ██║{Fore.CYAN} ║
    ║                    {Fore.GREEN}╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝{Fore.CYAN} ║
    ║                    {Fore.GREEN}PASSWORD STRENGTH ANALYZER v2.0{Fore.CYAN}                       ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Common password blacklist (top 100 worst passwords)
    COMMON_PASSWORDS = [
        '123456', 'password', '12345678', 'qwerty', '123456789', '12345', '1234', '111111',
        '1234567', 'dragon', '123123', 'baseball', 'abc123', 'football', 'monkey', 'letmein',
        '696969', 'shadow', 'master', '666666', 'qwertyuiop', '123321', 'mustang', '1234567890',
        'michael', '654321', 'superman', '1qaz2wsx', '7777777', '121212', '000000', 'qazwsx',
        '123qwe', 'killer', 'trustno1', 'jordan', 'jennifer', 'zxcvbnm', 'asdfgh', 'hunter',
        'buster', 'soccer', 'harley', 'batman', 'andrew', 'tigger', 'sunshine', 'iloveyou',
        '2000', 'charlie', 'robert', 'thomas', 'hockey', 'ranger', 'daniel', 'starwars',
        'klaster', '112233', 'george', 'computer', 'michelle', 'jessica', 'pepper', '1111',
        'zxcvbn', '555555', '11111111', '131313', 'freedom', '777777', 'pass', 'maggie',
        '159753', 'aaaaaa', 'ginger', 'princess', 'joshua', 'cheese', 'amanda', 'summer',
        'love', 'ashley', 'nicole', 'chelsea', 'biteme', 'matthew', 'access', 'yankees',
        '987654321', 'dallas', 'austin', 'thunder', 'taylor', 'matrix', 'mobilemail',
        'mom', 'monitor', 'monitoring', 'montana', 'moon', 'moscow',
    ]
    
    # Character set definitions
    CHARACTER_SETS = {
        'lowercase': (r'[a-z]', 26),
        'uppercase': (r'[A-Z]', 26),
        'digits': (r'[0-9]', 10),
        'special': (r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?`~]', 33),
        'space': (r'\s', 1)
    }
    
    def __init__(self):
        self.password = None
        self.password_hash = None
        self.entropy = 0
        self.strength_score = 0
        self.strength_label = ''
        self.crack_time = ''
        self.feedback = []
        self.warnings = []
        self.suggestions = []
        self.breach_check = False
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def calculate_entropy(self, password):
        """Calculate password entropy in bits"""
        charset_size = 0
        
        # Determine character set size
        for name, (pattern, size) in self.CHARACTER_SETS.items():
            if re.search(pattern, password):
                charset_size += size
                
        if charset_size == 0:
            return 0
            
        # Shannon entropy: log2(charset_size) * length
        entropy = math.log2(charset_size) * len(password)
        return round(entropy, 2)
        
    def check_composition(self, password):
        """Check password composition requirements"""
        checks = {
            'length': len(password) >= 12,
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?`~]', password)),
            'no_spaces': ' ' not in password,
            'no_repeating': not re.search(r'(.)\1{2,}', password),
            'no_sequential': not self.has_sequential_chars(password),
            'no_keyboard_pattern': not self.has_keyboard_pattern(password),
        }
        
        return checks
        
    def has_sequential_chars(self, password):
        """Check for sequential characters (abc, 123, etc.)"""
        password = password.lower()
        sequences = [
            'abcdefghijklmnopqrstuvwxyz',
            '0123456789',
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
        ]
        
        for seq in sequences:
            for i in range(len(seq) - 2):
                if seq[i:i+3] in password:
                    return True
        return False
        
    def has_keyboard_pattern(self, password):
        """Check for keyboard patterns (qwerty, asdf, etc.)"""
        password = password.lower()
        patterns = [
            'qwerty', 'asdf', 'zxcv', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm', '8ik,', '9ol.', '0p;/',
            'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm', 'ik,', 'ol.', 'p;/'
        ]
        
        for pattern in patterns:
            if pattern in password:
                return True
        return False
        
    def check_common_password(self, password):
        """Check if password is in common passwords list"""
        return password.lower() in self.COMMON_PASSWORDS
        
    def check_pwned_password(self, password):
        """Check if password has been breached (HIBP API)"""
        try:
            # SHA-1 hash of password
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query HIBP API
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                hashes = response.text.split('\r\n')
                for h in hashes:
                    if h.split(':')[0] == suffix:
                        count = int(h.split(':')[1])
                        return count
        except:
            pass
            
        return 0
        
    def estimate_crack_time(self, entropy, hash_type='bcrypt'):
        """Estimate time to crack password"""
        # Guessing speeds (guesses per second)
        speeds = {
            'md5': 1e10,        # 10 billion/sec - GPU
            'sha1': 5e9,        # 5 billion/sec - GPU
            'sha256': 1e9,      # 1 billion/sec - GPU
            'bcrypt': 1000,     # 1k/sec - GPU
            'pbkdf2': 1e5,      # 100k/sec - GPU
            'scrypt': 5000,     # 5k/sec - GPU
        }
        
        speed = speeds.get(hash_type, 1e9)
        guesses_per_second = speed
        
        # Total guesses needed = 2^(entropy-1) (average case)
        total_guesses = 2 ** (entropy - 1)
        seconds = total_guesses / guesses_per_second
        
        # Convert to human-readable format
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        elif seconds < 31536000 * 100:
            return f"{seconds/31536000:.1f} years"
        else:
            return "centuries"
            
    def analyze_strength(self, password):
        """Complete password strength analysis"""
        self.password = password
        self.feedback = []
        self.warnings = []
        self.suggestions = []
        
        # Calculate entropy
        self.entropy = self.calculate_entropy(password)
        
        # Check composition
        checks = self.check_composition(password)
        
        # Calculate score (0-100)
        score = 0
        
        # Length score (max 30)
        length_score = min(30, len(password) * 2.5)
        score += length_score
        
        # Character variety score (max 40)
        variety_score = 0
        if checks['lowercase']: variety_score += 8
        if checks['uppercase']: variety_score += 8
        if checks['digits']: variety_score += 8
        if checks['special']: variety_score += 8
        if checks['no_spaces']: variety_score += 8
        score += variety_score
        
        # Pattern penalties
        if not checks['no_repeating']:
            score -= 15
            self.warnings.append('Contains repeating characters')
            
        if self.has_sequential_chars(password):
            score -= 15
            self.warnings.append('Contains sequential characters (abc, 123)')
            
        if self.has_keyboard_pattern(password):
            score -= 15
            self.warnings.append('Contains keyboard pattern (qwerty, asdf)')
            
        # Common password penalty
        if self.check_common_password(password):
            score -= 50
            self.warnings.append('Password is too common - easily guessed')
            
        # Entropy bonus
        if self.entropy >= 80:
            score += 20
        elif self.entropy >= 60:
            score += 10
            
        # Clamp score
        self.strength_score = max(0, min(100, score))
        
        # Determine strength label
        if self.strength_score >= 80:
            self.strength_label = 'VERY STRONG'
            strength_color = Fore.GREEN + Style.BRIGHT
            self.feedback.append('Excellent password - highly secure')
        elif self.strength_score >= 60:
            self.strength_label = 'STRONG'
            strength_color = Fore.GREEN
            self.feedback.append('Good password - sufficiently secure')
        elif self.strength_score >= 40:
            self.strength_label = 'MEDIUM'
            strength_color = Fore.YELLOW
            self.feedback.append('Moderate password - could be stronger')
        elif self.strength_score >= 20:
            self.strength_label = 'WEAK'
            strength_color = Fore.RED
            self.feedback.append('Weak password - easily cracked')
        else:
            self.strength_label = 'VERY WEAK'
            strength_color = Fore.RED + Style.BRIGHT
            self.feedback.append('Very weak password - immediately change')
            
        # Crack time estimates
        self.crack_times = {
            'md5': self.estimate_crack_time(self.entropy, 'md5'),
            'sha1': self.estimate_crack_time(self.entropy, 'sha1'),
            'sha256': self.estimate_crack_time(self.entropy, 'sha256'),
            'bcrypt': self.estimate_crack_time(self.entropy, 'bcrypt'),
        }
        
        # Generate suggestions
        if not checks['length']:
            self.suggestions.append('Use at least 12 characters')
        if not checks['lowercase']:
            self.suggestions.append('Add lowercase letters')
        if not checks['uppercase']:
            self.suggestions.append('Add uppercase letters')
        if not checks['digits']:
            self.suggestions.append('Add numbers')
        if not checks['special']:
            self.suggestions.append('Add special characters')
        if checks['no_spaces'] is False:
            self.suggestions.append('Remove spaces')
        if not checks['no_repeating']:
            self.suggestions.append('Avoid repeating characters')
        if self.has_sequential_chars(password):
            self.suggestions.append('Avoid sequential characters (abc, 123)')
        if self.has_keyboard_pattern(password):
            self.suggestions.append('Avoid keyboard patterns (qwerty, asdf)')
        if self.check_common_password(password):
            self.suggestions.append('Choose a less common password')
            
        # Check if password has been pwned
        print(f"{Fore.CYAN}[*] Checking against breach database...{Style.RESET_ALL}")
        breach_count = self.check_pwned_password(password)
        if breach_count > 0:
            self.breach_check = True
            self.warnings.append(f'Password has been seen {breach_count:,} times in data breaches!')
            self.suggestions.append('IMMEDIATELY change this password - it has been compromised')
            
        return {
            'score': self.strength_score,
            'label': self.strength_label,
            'entropy': self.entropy,
            'crack_times': self.crack_times,
            'checks': checks,
            'warnings': self.warnings,
            'suggestions': self.suggestions,
            'breached': self.breach_check
        }
        
    def generate_report(self):
        """Generate comprehensive password strength report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] PASSWORD STRENGTH REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Password Length: {Fore.LIGHTGREEN_EX}{len(self.password)} characters{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ STRENGTH SCORE ============
        print(f"\n{Fore.CYAN}[ STRENGTH ASSESSMENT ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Visual score bar
        bar_length = 40
        filled_length = int(bar_length * self.strength_score / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if self.strength_score >= 80:
            score_color = Fore.GREEN + Style.BRIGHT
        elif self.strength_score >= 60:
            score_color = Fore.GREEN
        elif self.strength_score >= 40:
            score_color = Fore.YELLOW
        elif self.strength_score >= 20:
            score_color = Fore.RED
        else:
            score_color = Fore.RED + Style.BRIGHT
            
        print(f"\n  Score: {score_color}{self.strength_score}/100{Style.RESET_ALL}")
        print(f"  Bar:   {score_color}[{bar}]{Style.RESET_ALL}")
        print(f"  Level: {score_color}{self.strength_label}{Style.RESET_ALL}")
        
        # ============ ENTROPY ANALYSIS ============
        print(f"\n{Fore.CYAN}[ ENTROPY ANALYSIS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}Information Entropy:{Style.RESET_ALL} {self.entropy} bits")
        
        if self.entropy < 30:
            entropy_status = Fore.RED + 'Very Low'
        elif self.entropy < 50:
            entropy_status = Fore.YELLOW + 'Low'
        elif self.entropy < 70:
            entropy_status = Fore.GREEN + 'Moderate'
        elif self.entropy < 90:
            entropy_status = Fore.GREEN + 'High'
        else:
            entropy_status = Fore.GREEN + Style.BRIGHT + 'Very High'
            
        print(f"  {Fore.WHITE}Entropy Level:{Style.RESET_ALL} {entropy_status}{Style.RESET_ALL}")
        
        # ============ CRACK TIME ESTIMATES ============
        print(f"\n{Fore.CYAN}[ CRACK TIME ESTIMATES ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}MD5 (fast hash):{Style.RESET_ALL} {Fore.RED if 'seconds' in self.crack_times['md5'] else Fore.YELLOW}{self.crack_times['md5']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}SHA-1:{Style.RESET_ALL} {Fore.RED if 'seconds' in self.crack_times['sha1'] else Fore.YELLOW}{self.crack_times['sha1']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}SHA-256:{Style.RESET_ALL} {Fore.RED if 'seconds' in self.crack_times['sha256'] else Fore.YELLOW}{self.crack_times['sha256']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}bcrypt (slow hash):{Style.RESET_ALL} {Fore.GREEN}{self.crack_times['bcrypt']}{Style.RESET_ALL}")
        
        # ============ COMPOSITION CHECK ============
        print(f"\n{Fore.CYAN}[ COMPOSITION CHECK ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        checks = self.check_composition(self.password)
        
        check_items = [
            ('Length ≥ 12', checks['length']),
            ('Lowercase', checks['lowercase']),
            ('Uppercase', checks['uppercase']),
            ('Digits', checks['digits']),
            ('Special Characters', checks['special']),
            ('No Spaces', checks['no_spaces']),
            ('No Repeating', checks['no_repeating']),
            ('No Sequential', not self.has_sequential_chars(self.password)),
            ('No Keyboard Pattern', not self.has_keyboard_pattern(self.password)),
        ]
        
        for label, passed in check_items:
            if passed:
                print(f"  {Fore.GREEN}[✓]{Style.RESET_ALL} {label}")
            else:
                print(f"  {Fore.RED}[✗]{Style.RESET_ALL} {label}")
                
        # ============ WARNINGS ============
        if self.warnings:
            print(f"\n{Fore.CYAN}[ SECURITY WARNINGS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for warning in self.warnings:
                if 'breach' in warning.lower():
                    print(f"\n  {Fore.RED}{Style.BRIGHT}[!] {warning}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.YELLOW}[!] {warning}{Style.RESET_ALL}")
                    
        # ============ SUGGESTIONS ============
        if self.suggestions:
            print(f"\n{Fore.CYAN}[ IMPROVEMENT SUGGESTIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for i, suggestion in enumerate(self.suggestions[:8], 1):
                if 'IMMEDIATELY' in suggestion:
                    print(f"\n  {Fore.RED}{i}. {suggestion}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.YELLOW}{i}. {suggestion}{Style.RESET_ALL}")
                    
        # ============ PASSWORD TIPS ============
        print(f"\n{Fore.CYAN}[ PASSWORD BEST PRACTICES ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print("""
  • Use passphrases: "correct-horse-battery-staple"
  • Minimum 12-16 characters
  • Unique for each account/service
  • Enable 2FA/MFA where available
  • Use a password manager
  • Change immediately if compromised
        """)
        
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Password never stored or transmitted{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Analysis performed locally{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON (without password)"""
        if not filename:
            filename = f"password_analysis_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'password_length': len(self.password),
            'strength_score': self.strength_score,
            'strength_label': self.strength_label,
            'entropy': self.entropy,
            'crack_times': self.crack_times,
            'checks': self.check_composition(self.password),
            'warnings': self.warnings,
            'suggestions': self.suggestions,
            'breached': self.breach_check
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_analyze(self):
        """Interactive password analysis mode"""
        print(f"{Fore.GREEN}[*] Password Strength Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced entropy & breach checking{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[!] Password will NOT be stored or transmitted{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Analysis performed entirely locally{Style.RESET_ALL}\n")
        
        # Get password
        import getpass
        password = getpass.getpass(f"{Fore.YELLOW}[?] Enter password to analyze: {Style.RESET_ALL}")
        
        if not password:
            print(f"{Fore.RED}[✗] No password entered{Style.RESET_ALL}")
            return
            
        # Confirm (masked)
        print(f"\n{Fore.CYAN}[*] Analyzing password of length {len(password)}...{Style.RESET_ALL}")
        
        self.start_time = datetime.now()
        
        # Analyze password
        self.analyze_strength(password)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Password analysis completed{Style.RESET_ALL}")


def password_strength_check(password=None):
    """Main entry point for CLI compatibility"""
    analyzer = PasswordStrengthAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if password:
        # Direct analysis mode
        analyzer.start_time = datetime.now()
        analyzer.analyze_strength(password)
        analyzer.end_time = datetime.now()
        analyzer.generate_report()
    else:
        # Interactive mode
        analyzer.interactive_analyze()


if __name__ == "__main__":
    password_strength_check()
