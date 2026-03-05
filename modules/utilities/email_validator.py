#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: EMAIL VALIDATOR
Advanced Email Address Syntax & Domain Validation
Author: ICAT Project | Linxploit.xyz
"""

import re
import socket
import dns.resolver
import json
from datetime import datetime
from colorama import Fore, Style, init
import smtplib

init(autoreset=True)

class EmailValidator:
    """Advanced email address validation with MX record checking"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗███╗   ███╗ █████╗ ██╗██╗         ██╗   ██╗ █████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗  ║
    ║  ██╔════╝████╗ ████║██╔══██╗██║██║         ██║   ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗ ║
    ║  █████╗  ██╔████╔██║███████║██║██║         ██║   ██║███████║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝ ║
    ║  ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗ ║
    ║  ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗     ╚████╔╝ ██║  ██║███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║ ║
    ║  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝      ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ║
    ║                    {Fore.GREEN}EMAIL VALIDATOR & VERIFIER v2.0{Fore.CYAN}                ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Email syntax regex (RFC 5322 compliant simplified)
    EMAIL_REGEX = r"^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$"
    
    # Disposable email domains
    DISPOSABLE_DOMAINS = [
        'mailinator.com', 'guerrillamail.com', 'guerrillamail.net', 'guerrillamail.org',
        'guerrillamail.biz', 'guerrillamail.de', 'sharklasers.com', 'grr.la',
        'temp-mail.org', 'temp-mail.ru', '10minutemail.com', '10minutemail.net',
        'yopmail.com', 'yopmail.fr', 'yopmail.net', 'throwawaymail.com',
        'trashmail.com', 'trashmail.net', 'trashmail.org', 'maildrop.cc',
        'getnada.com', 'nada.email', 'discard.email', 'discardmail.com',
        'spambox.us', 'spambox.info', 'spamgourmet.com', 'spamhole.com',
        'throwaway.email', 'tempmail.com', 'tempmail.net', 'tempmail.org',
        'tempmail.de', 'tempemail.com', 'tempemail.net', 'tempemail.org',
        'tempemail.co', 'fakeinbox.com', 'fake-mail.net', 'fakemail.net',
        'fakemailgenerator.com', 'mailcatch.com', 'mailinator2.com',
        'mailinator3.com', 'mailinator4.com', 'mailinator5.com',
        'mailinator6.com', 'mailinator7.com', 'mailinator8.com',
        'mailinator9.com', 'mailinator10.com',
    ]
    
    # Role-based email patterns
    ROLE_PATTERNS = [
        r'^admin@', r'^webmaster@', r'^postmaster@', r'^hostmaster@',
        r'^abuse@', r'^info@', r'^contact@', r'^support@', r'^sales@',
        r'^marketing@', r'^help@', r'^enquiries@', r'^feedback@',
        r'^noreply@', r'^no-reply@', r'^donotreply@', r'^no.reply@',
        r'^subscribe@', r'^unsubscribe@', r'^billing@', r'^accounts@',
        r'^newsletter@', r'^news@', r'^press@', r'^media@', r'^jobs@',
        r'^hr@', r'^careers@', r'^recruitment@', r'^recruiting@',
        r'^privacy@', r'^legal@', r'^copyright@', r'^dmca@',
    ]
    
    # Common domain typos
    COMMON_TYPOS = {
        'gmail.com': ['gmai.com', 'gmil.com', 'gmal.com', 'gmail.co', 'gamil.com', 'gmial.com'],
        'yahoo.com': ['yaho.com', 'yahooo.com', 'yhoo.com', 'yahoo.co', 'yahooo.com'],
        'hotmail.com': ['hotmal.com', 'hotmil.com', 'hotmail.co', 'hotmial.com'],
        'outlook.com': ['outlok.com', 'outloo.com', 'outlook.co', 'outllok.com'],
        'aol.com': ['aol.co', 'ol.com', 'aol.com'],
        'icloud.com': ['icloud.co', 'iclud.com', 'iclod.com'],
    }
    
    def __init__(self):
        self.email = None
        self.local_part = None
        self.domain = None
        self.syntax_valid = False
        self.mx_records = []
        self.disposable = False
        self.role_account = False
        self.typo_suggestions = []
        self.validation_results = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def validate_syntax(self, email):
        """Validate email syntax"""
        self.email = email.strip().lower()
        
        # Basic format check
        if not re.match(self.EMAIL_REGEX, self.email, re.IGNORECASE):
            self.syntax_valid = False
            return False
            
        # Split into local and domain
        try:
            self.local_part, self.domain = self.email.split('@')
            self.syntax_valid = True
            return True
        except:
            self.syntax_valid = False
            return False
            
    def check_disposable(self, domain):
        """Check if domain is disposable"""
        return domain.lower() in self.DISPOSABLE_DOMAINS
        
    def check_role_account(self, local_part):
        """Check if local part indicates role account"""
        for pattern in self.ROLE_PATTERNS:
            if re.match(pattern, local_part, re.IGNORECASE):
                return True
        return False
        
    def check_mx_records(self, domain):
        """Check MX records for domain"""
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_list = []
            for rdata in answers:
                mx_list.append({
                    'preference': rdata.preference,
                    'exchange': str(rdata.exchange).rstrip('.')
                })
            
            # Sort by preference (lowest first)
            mx_list.sort(key=lambda x: x['preference'])
            self.mx_records = mx_list
            return len(mx_list) > 0
        except:
            self.mx_records = []
            return False
            
    def check_a_record(self, domain):
        """Check A records for domain (fallback if no MX)"""
        try:
            dns.resolver.resolve(domain, 'A')
            return True
        except:
            return False
            
    def suggest_typo_fixes(self, domain):
        """Suggest common typo fixes for domains"""
        suggestions = []
        
        # Check against known typos
        for correct_domain, typos in self.COMMON_TYPOS.items():
            if domain in typos:
                suggestions.append({
                    'suggested': correct_domain,
                    'original': domain,
                    'confidence': 'HIGH'
                })
                
        # Check for missing dot
        if '.' not in domain:
            suggestions.append({
                'suggested': f"{domain}.com",
                'original': domain,
                'confidence': 'MEDIUM'
            })
            
        # Check for common TLD mistakes
        if domain.endswith('.con'):
            suggestions.append({
                'suggested': domain.replace('.con', '.com'),
                'original': domain,
                'confidence': 'HIGH'
            })
        elif domain.endswith('.cmo'):
            suggestions.append({
                'suggested': domain.replace('.cmo', '.com'),
                'original': domain,
                'confidence': 'HIGH'
            })
        elif domain.endswith('.ocm'):
            suggestions.append({
                'suggested': domain.replace('.ocm', '.com'),
                'original': domain,
                'confidence': 'HIGH'
            })
            
        self.typo_suggestions = suggestions
        return suggestions
        
    def validate_email(self, email):
        """Complete email validation workflow"""
        results = {
            'email': email,
            'syntax_valid': False,
            'domain_valid': False,
            'mx_exists': False,
            'disposable': False,
            'role_account': False,
            'typo_suggestions': [],
            'mx_records': []
        }
        
        # Step 1: Syntax validation
        if not self.validate_syntax(email):
            results['syntax_valid'] = False
            results['error'] = 'Invalid email syntax'
            self.validation_results = results
            return results
            
        results['syntax_valid'] = True
        results['local_part'] = self.local_part
        results['domain'] = self.domain
        
        # Step 2: Check disposable
        results['disposable'] = self.check_disposable(self.domain)
        
        # Step 3: Check role account
        results['role_account'] = self.check_role_account(self.local_part)
        
        # Step 4: Check MX records
        if self.check_mx_records(self.domain):
            results['mx_exists'] = True
            results['mx_records'] = self.mx_records
            results['domain_valid'] = True
        else:
            # Fallback to A record
            if self.check_a_record(self.domain):
                results['mx_exists'] = False
                results['domain_valid'] = True
                results['note'] = 'No MX records found, but domain has A record'
            else:
                results['domain_valid'] = False
                results['error'] = 'Domain does not exist or has no mail servers'
                
        # Step 5: Check for typos
        results['typo_suggestions'] = self.suggest_typo_fixes(self.domain)
        
        self.validation_results = results
        return results
        
    def generate_report(self):
        """Generate comprehensive email validation report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] EMAIL VALIDATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Email Address: {Fore.LIGHTGREEN_EX}{self.email}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Local Part: {Fore.LIGHTGREEN_EX}{self.local_part}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SYNTAX VALIDATION ============
        print(f"\n{Fore.CYAN}[ SYNTAX VALIDATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.validation_results.get('syntax_valid'):
            print(f"\n  {Fore.GREEN}[✓] Valid email format{Style.RESET_ALL}")
            print(f"      ├─ Local part: {self.local_part}")
            print(f"      └─ Domain: {self.domain}")
        else:
            print(f"\n  {Fore.RED}[✗] Invalid email format{Style.RESET_ALL}")
            print(f"      └─ {self.validation_results.get('error', 'Syntax error')}")
            print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
            return
            
        # ============ DOMAIN VALIDATION ============
        print(f"\n{Fore.CYAN}[ DOMAIN VALIDATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.validation_results.get('domain_valid'):
            print(f"\n  {Fore.GREEN}[✓] Domain is valid and accepts email{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}[✗] Domain does not accept email{Style.RESET_ALL}")
            print(f"      └─ {self.validation_results.get('error', 'No mail servers found')}")
            
        # MX Records
        if self.mx_records:
            print(f"\n  {Fore.WHITE}MX Records (priority order):{Style.RESET_ALL}")
            for i, mx in enumerate(self.mx_records[:5], 1):
                print(f"    {i}. Priority {mx['preference']}: {mx['exchange']}")
        elif self.validation_results.get('domain_valid'):
            print(f"\n  {Fore.YELLOW}[!] No MX records found, but domain has A record{Style.RESET_ALL}")
            print(f"      └─ Email may still work, but not guaranteed")
            
        # ============ EMAIL CLASSIFICATION ============
        print(f"\n{Fore.CYAN}[ EMAIL CLASSIFICATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Disposable check
        if self.validation_results.get('disposable'):
            print(f"\n  {Fore.YELLOW}[!] Disposable email address detected{Style.RESET_ALL}")
            print(f"      └─ Often used for temporary accounts and spam")
        else:
            print(f"\n  {Fore.GREEN}[✓] Not a disposable email address{Style.RESET_ALL}")
            
        # Role account check
        if self.validation_results.get('role_account'):
            print(f"\n  {Fore.YELLOW}[!] Role-based email account{Style.RESET_ALL}")
            print(f"      └─ Not associated with a specific person")
        else:
            print(f"\n  {Fore.GREEN}[✓] Personal email address{Style.RESET_ALL}")
            
        # ============ TYPO SUGGESTIONS ============
        if self.typo_suggestions:
            print(f"\n{Fore.CYAN}[ TYPO SUGGESTIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for suggestion in self.typo_suggestions:
                print(f"\n  {Fore.YELLOW}[!] Did you mean: {suggestion['suggested']}{Style.RESET_ALL}")
                print(f"      └─ Confidence: {suggestion['confidence']}")
                
        # ============ EMAIL SCORING ============
        print(f"\n{Fore.CYAN}[ EMAIL SCORING ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        score = 100
        deductions = []
        
        if self.validation_results.get('disposable'):
            score -= 40
            deductions.append('Disposable email (-40)')
            
        if self.validation_results.get('role_account'):
            score -= 20
            deductions.append('Role account (-20)')
            
        if not self.mx_records:
            score -= 15
            deductions.append('No MX records (-15)')
            
        if self.typo_suggestions:
            score -= 25
            deductions.append('Possible typo (-25)')
            
        score = max(0, score)
        
        if score >= 80:
            score_color = Fore.GREEN
            rating = 'Excellent'
        elif score >= 60:
            score_color = Fore.YELLOW
            rating = 'Good'
        elif score >= 40:
            score_color = Fore.YELLOW
            rating = 'Fair'
        elif score >= 20:
            score_color = Fore.RED
            rating = 'Poor'
        else:
            score_color = Fore.RED
            rating = 'Very Poor'
            
        print(f"\n  {Fore.WHITE}Email Quality Score:{Style.RESET_ALL} {score_color}{score}/100{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Rating:{Style.RESET_ALL} {score_color}{rating}{Style.RESET_ALL}")
        
        if deductions:
            print(f"\n  {Fore.WHITE}Deductions:{Style.RESET_ALL}")
            for deduction in deductions:
                print(f"    • {deduction}")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.validation_results.get('disposable'):
            print(f"\n  {Fore.YELLOW}• Use a permanent email address for important communications{Style.RESET_ALL}")
            
        if self.validation_results.get('role_account'):
            print(f"\n  {Fore.YELLOW}• Consider using a personal email for account registration{Style.RESET_ALL}")
            
        if self.typo_suggestions:
            print(f"\n  {Fore.YELLOW}• Verify the domain spelling - possible typo detected{Style.RESET_ALL}")
            
        if not self.mx_records and self.validation_results.get('domain_valid'):
            print(f"\n  {Fore.YELLOW}• Domain has no MX records - email delivery not guaranteed{Style.RESET_ALL}")
            
        if score >= 80:
            print(f"\n  {Fore.GREEN}• Email address appears valid and well-formed{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"email_validation_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'email': self.email,
            'local_part': self.local_part,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'validation_results': self.validation_results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_validate(self):
        """Interactive email validation mode"""
        print(f"{Fore.GREEN}[*] Email Validator initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Syntax validation + MX record checking{Style.RESET_ALL}\n")
        
        # Get email
        email_input = input(f"{Fore.YELLOW}[?] Enter email address to validate: {Style.RESET_ALL}").strip()
        
        if not email_input:
            print(f"{Fore.RED}[✗] No email specified{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.YELLOW}[*] Validating email: {email_input}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Checking syntax and mail servers...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Validate email
        self.validate_email(email_input)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Email validation completed{Style.RESET_ALL}")


def email_validator(email=None):
    """Main entry point for CLI compatibility"""
    validator = EmailValidator()
    
    # Display banner
    validator.print_header()
    
    if email:
        # Direct validation mode
        validator.start_time = datetime.now()
        validator.validate_email(email)
        validator.end_time = datetime.now()
        validator.generate_report()
    else:
        # Interactive mode
        validator.interactive_validate()


if __name__ == "__main__":
    email_validator()
