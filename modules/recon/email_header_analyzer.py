#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: EMAIL HEADER ANALYZER
Advanced Email Forensics & Header Analysis
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import socket
from datetime import datetime
from colorama import Fore, Style, init
import dns.resolver

init(autoreset=True)

class EmailHeaderAnalyzer:
    """Advanced email header analysis for forensics and security"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗███╗   ███╗ █████╗ ██╗██╗     ██╗  ██╗███████╗ █████╗ ██████╗ ███████╗██████╗      ║
    ║  ██╔════╝████╗ ████║██╔══██╗██║██║     ██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗     ║
    ║  █████╗  ██╔████╔██║███████║██║██║     ███████║█████╗  ███████║██║  ██║█████╗  ██████╔╝     ║
    ║  ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██╔══██║██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗     ║
    ║  ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗██║  ██║███████╗██║  ██║██████╔╝███████╗██║  ██║     ║
    ║  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝     ║
    ║  {Fore.CYAN}████████╗ ██████╗  ██████╗ ██╗     ███████╗███╗   ██╗███████╗██╗ ██████╗ ███████╗{Fore.RED}   ║
    ║  {Fore.CYAN}╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝████╗  ██║██╔════╝██║██╔════╝ ██╔════╝{Fore.RED}   ║
    ║  {Fore.CYAN}   ██║   ██║   ██║██║   ██║██║     █████╗  ██╔██╗ ██║█████╗  ██║██║  ███╗███████╗{Fore.RED}   ║
    ║  {Fore.CYAN}   ██║   ██║   ██║██║   ██║██║     ██╔══╝  ██║╚██╗██║██╔══╝  ██║██║   ██║╚════██║{Fore.RED}   ║
    ║  {Fore.CYAN}   ██║   ╚██████╔╝╚██████╔╝███████╗███████╗██║ ╚████║██║     ██║╚██████╔╝███████║{Fore.RED}   ║
    ║  {Fore.CYAN}   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝{Fore.RED}   ║
    ║                    {Fore.CYAN}EMAIL HEADER ANALYZER & FORENSICS v2.0{Fore.RED}              ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Authentication result keywords
    AUTH_RESULTS = {
        'spf': ['spf=pass', 'spf=fail', 'spf=softfail', 'spf=neutral', 'spf=none', 'spf=temperror', 'spf=permerror'],
        'dkim': ['dkim=pass', 'dkim=fail', 'dkim=neutral', 'dkim=none', 'dkim=policy', 'dkim=permerror', 'dkim=temperror'],
        'dmarc': ['dmarc=pass', 'dmarc=fail', 'dmarc=bestguesspass', 'dmarc=none', 'dmarc=temperror', 'dmarc=permerror'],
    }
    
    # Suspicious keywords
    SUSPICIOUS_KEYWORDS = [
        'urgent', 'verify', 'account', 'suspended', 'limited', 'unusual',
        'login', 'credential', 'password', 'bank', 'paypal', 'apple',
        'microsoft', 'amazon', 'secure', 'update', 'confirm', 'invoice'
    ]
    
    def __init__(self):
        self.raw_headers = None
        self.parsed_headers = {}
        self.authentication_results = {}
        self.received_chain = []
        self.security_evaluation = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def parse_headers(self, headers_text):
        """Parse raw email headers into structured format"""
        self.raw_headers = headers_text
        lines = headers_text.split('\n')
        
        current_key = None
        current_value = []
        
        for line in lines:
            line = line.rstrip('\r')
            
            # Continuation line starts with space or tab
            if line and (line[0] in (' ', '\t')):
                if current_key:
                    current_value.append(line.strip())
            else:
                # Save previous header
                if current_key:
                    self.parsed_headers[current_key] = ' '.join(current_value)
                    
                # Start new header
                if ':' in line:
                    parts = line.split(':', 1)
                    current_key = parts[0].strip()
                    current_value = [parts[1].strip()] if len(parts) > 1 else ['']
                    
        # Save last header
        if current_key:
            self.parsed_headers[current_key] = ' '.join(current_value)
            
        # Parse received chain
        self.parse_received_chain()
        
        # Parse authentication results
        self.parse_authentication_results()
        
        return self.parsed_headers
        
    def parse_received_chain(self):
        """Parse and order Received headers chronologically"""
        received_headers = []
        
        for key, value in self.parsed_headers.items():
            if key.lower() == 'received':
                received_headers.append(value)
                
        # Parse each Received header
        self.received_chain = []
        
        for received in received_headers:
            entry = {
                'raw': received,
                'from': None,
                'by': None,
                'with': None,
                'via': None,
                'id': None,
                'for': None,
                'timestamp': None,
                'ip': None,
                'helo': None
            }
            
            # Extract IP address
            ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
            ip_match = re.search(ip_pattern, received)
            if ip_match:
                entry['ip'] = ip_match.group(0)
                
            # Extract from
            from_match = re.search(r'from\s+([^\s]+)', received, re.IGNORECASE)
            if from_match:
                entry['from'] = from_match.group(1)
                
            # Extract by
            by_match = re.search(r'by\s+([^\s]+)', received, re.IGNORECASE)
            if by_match:
                entry['by'] = by_match.group(1)
                
            # Extract with
            with_match = re.search(r'with\s+([^\s]+)', received, re.IGNORECASE)
            if with_match:
                entry['with'] = with_match.group(1)
                
            # Extract for
            for_match = re.search(r'for\s+<([^>]+)>', received, re.IGNORECASE)
            if for_match:
                entry['for'] = for_match.group(1)
                
            # Extract ID
            id_match = re.search(r'id\s+([^\s]+)', received, re.IGNORECASE)
            if id_match:
                entry['id'] = id_match.group(1)
                
            self.received_chain.append(entry)
            
        # Reverse to get chronological order (oldest first)
        self.received_chain.reverse()
        
        return self.received_chain
        
    def parse_authentication_results(self):
        """Parse Authentication-Results headers"""
        self.authentication_results = {
            'spf': None,
            'dkim': None,
            'dmarc': None
        }
        
        for key, value in self.parsed_headers.items():
            if key.lower() == 'authentication-results':
                value_lower = value.lower()
                
                for auth_type, patterns in self.AUTH_RESULTS.items():
                    for pattern in patterns:
                        if pattern in value_lower:
                            self.authentication_results[auth_type] = pattern.split('=')[1]
                            break
                            
        return self.authentication_results
        
    def extract_email_addresses(self):
        """Extract from, to, cc, bcc, reply-to addresses"""
        addresses = {}
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        for field in ['From', 'To', 'Cc', 'Bcc', 'Reply-To', 'Return-Path', 'Sender']:
            if field in self.parsed_headers:
                value = self.parsed_headers[field]
                emails = re.findall(email_pattern, value)
                if emails:
                    addresses[field] = emails
                    
        return addresses
        
    def extract_message_id(self):
        """Extract Message-ID"""
        for key in ['Message-ID', 'Message-Id']:
            if key in self.parsed_headers:
                return self.parsed_headers[key]
        return None
        
    def extract_subject(self):
        """Extract email subject"""
        if 'Subject' in self.parsed_headers:
            return self.parsed_headers['Subject']
        return None
        
    def extract_date(self):
        """Extract email date"""
        if 'Date' in self.parsed_headers:
            return self.parsed_headers['Date']
        return None
        
    def evaluate_security(self):
        """Evaluate email security posture"""
        self.security_evaluation = {
            'spf_valid': False,
            'dkim_valid': False,
            'dmarc_valid': False,
            'tls_used': False,
            'suspicious_subject': False,
            'spoofing_risk': 'UNKNOWN',
            'warnings': []
        }
        
        # Check authentication
        if self.authentication_results.get('spf') == 'pass':
            self.security_evaluation['spf_valid'] = True
        elif self.authentication_results.get('spf'):
            self.security_evaluation['warnings'].append(f"SPF failed: {self.authentication_results['spf']}")
            
        if self.authentication_results.get('dkim') == 'pass':
            self.security_evaluation['dkim_valid'] = True
        elif self.authentication_results.get('dkim'):
            self.security_evaluation['warnings'].append(f"DKIM failed: {self.authentication_results['dkim']}")
            
        if self.authentication_results.get('dmarc') == 'pass':
            self.security_evaluation['dmarc_valid'] = True
        elif self.authentication_results.get('dmarc'):
            self.security_evaluation['warnings'].append(f"DMARC failed: {self.authentication_results['dmarc']}")
            
        # Check for TLS
        for entry in self.received_chain:
            if entry['with'] and 'tls' in entry['with'].lower():
                self.security_evaluation['tls_used'] = True
                break
                
        # Check subject for suspicious keywords
        subject = self.extract_subject()
        if subject:
            subject_lower = subject.lower()
            for keyword in self.SUSPICIOUS_KEYWORDS:
                if keyword in subject_lower:
                    self.security_evaluation['suspicious_subject'] = True
                    self.security_evaluation['warnings'].append(f"Suspicious keyword in subject: '{keyword}'")
                    break
                    
        # Assess spoofing risk
        if not self.security_evaluation['spf_valid'] and not self.security_evaluation['dkim_valid']:
            self.security_evaluation['spoofing_risk'] = 'HIGH'
        elif not self.security_evaluation['spf_valid'] or not self.security_evaluation['dkim_valid']:
            self.security_evaluation['spoofing_risk'] = 'MEDIUM'
        else:
            self.security_evaluation['spoofing_risk'] = 'LOW'
            
        return self.security_evaluation
        
    def lookup_ip_reputation(self, ip):
        """Quick IP reputation check via DNSBL (simplified)"""
        try:
            # Reverse IP for DNSBL query
            ip_parts = ip.split('.')
            reversed_ip = '.'.join(reversed(ip_parts))
            
            # Check Spamhaus
            try:
                socket.gethostbyname(f"{reversed_ip}.zen.spamhaus.org")
                return 'BLACKLISTED'
            except:
                pass
                
            # Check Spamcop
            try:
                socket.gethostbyname(f"{reversed_ip}.bl.spamcop.net")
                return 'SUSPICIOUS'
            except:
                pass
                
            return 'CLEAN'
        except:
            return 'UNKNOWN'
            
    def generate_report(self):
        """Generate comprehensive email header analysis report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] EMAIL HEADER ANALYSIS REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        # ============ BASIC INFORMATION ============
        print(f"\n{Fore.CYAN}[ BASIC INFORMATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        subject = self.extract_subject()
        date = self.extract_date()
        message_id = self.extract_message_id()
        
        if subject:
            print(f"\n  {Fore.WHITE}Subject:{Style.RESET_ALL} {subject[:100]}{'...' if len(subject) > 100 else ''}")
        if date:
            print(f"  {Fore.WHITE}Date:{Style.RESET_ALL} {date}")
        if message_id:
            print(f"  {Fore.WHITE}Message-ID:{Style.RESET_ALL} {message_id[:80]}{'...' if len(message_id) > 80 else ''}")
            
        # ============ ADDRESSES ============
        addresses = self.extract_email_addresses()
        
        if addresses:
            print(f"\n{Fore.CYAN}[ EMAIL ADDRESSES ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for field, emails in addresses.items():
                print(f"\n  {Fore.WHITE}{field}:{Style.RESET_ALL}")
                for email in emails:
                    print(f"    └─ {email}")
                    
        # ============ RECEIVED CHAIN ============
        if self.received_chain:
            print(f"\n{Fore.CYAN}[ RECEIVED CHAIN ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}Chronological order (oldest to newest):{Style.RESET_ALL}\n")
            
            for i, entry in enumerate(self.received_chain, 1):
                print(f"  {Fore.YELLOW}Hop {i}:{Style.RESET_ALL}")
                if entry['from']:
                    print(f"    ├─ From: {entry['from']}")
                if entry['by']:
                    print(f"    ├─ By: {entry['by']}")
                if entry['with']:
                    print(f"    ├─ Protocol: {entry['with']}")
                if entry['ip']:
                    # Check reputation
                    reputation = self.lookup_ip_reputation(entry['ip'])
                    if reputation == 'BLACKLISTED':
                        rep_color = Fore.RED
                    elif reputation == 'SUSPICIOUS':
                        rep_color = Fore.YELLOW
                    else:
                        rep_color = Fore.GREEN
                        
                    print(f"    ├─ IP: {entry['ip']} [{rep_color}{reputation}{Style.RESET_ALL}]")
                if entry['helo']:
                    print(f"    ├─ HELO: {entry['helo']}")
                if entry['id']:
                    print(f"    └─ ID: {entry['id']}")
                    
        # ============ AUTHENTICATION RESULTS ============
        print(f"\n{Fore.CYAN}[ AUTHENTICATION RESULTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        for auth_type, result in self.authentication_results.items():
            if result:
                if result == 'pass':
                    color = Fore.GREEN
                    status = '✓ PASS'
                elif result in ['fail', 'softfail', 'permerror']:
                    color = Fore.RED
                    status = '✗ FAIL'
                elif result == 'neutral':
                    color = Fore.YELLOW
                    status = '○ NEUTRAL'
                else:
                    color = Fore.YELLOW
                    status = f'? {result.upper()}'
                    
                print(f"\n  {Fore.WHITE}{auth_type.upper()}:{Style.RESET_ALL} {color}{status}{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.WHITE}{auth_type.upper()}:{Style.RESET_ALL} {Fore.YELLOW}? NOT FOUND{Style.RESET_ALL}")
                
        # ============ SECURITY EVALUATION ============
        self.evaluate_security()
        
        print(f"\n{Fore.CYAN}[ SECURITY EVALUATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Authentication summary
        auth_status = []
        if self.security_evaluation['spf_valid']:
            auth_status.append(f"{Fore.GREEN}SPF✓{Style.RESET_ALL}")
        else:
            auth_status.append(f"{Fore.RED}SPF✗{Style.RESET_ALL}")
            
        if self.security_evaluation['dkim_valid']:
            auth_status.append(f"{Fore.GREEN}DKIM✓{Style.RESET_ALL}")
        else:
            auth_status.append(f"{Fore.RED}DKIM✗{Style.RESET_ALL}")
            
        if self.security_evaluation['dmarc_valid']:
            auth_status.append(f"{Fore.GREEN}DMARC✓{Style.RESET_ALL}")
        else:
            auth_status.append(f"{Fore.RED}DMARC✗{Style.RESET_ALL}")
            
        print(f"\n  {Fore.WHITE}Authentication:{Style.RESET_ALL} {' '.join(auth_status)}")
        
        # TLS status
        tls_status = f"{Fore.GREEN}✓ TLS Used{Style.RESET_ALL}" if self.security_evaluation['tls_used'] else f"{Fore.YELLOW}✗ No TLS{Style.RESET_ALL}"
        print(f"  {Fore.WHITE}Encryption:{Style.RESET_ALL} {tls_status}")
        
        # Spoofing risk
        risk = self.security_evaluation['spoofing_risk']
        if risk == 'HIGH':
            risk_color = Fore.RED + Style.BRIGHT
        elif risk == 'MEDIUM':
            risk_color = Fore.RED
        elif risk == 'LOW':
            risk_color = Fore.GREEN
        else:
            risk_color = Fore.YELLOW
            
        print(f"  {Fore.WHITE}Spoofing Risk:{Style.RESET_ALL} {risk_color}{risk}{Style.RESET_ALL}")
        
        # Warnings
        if self.security_evaluation['warnings']:
            print(f"\n  {Fore.WHITE}Warnings:{Style.RESET_ALL}")
            for warning in self.security_evaluation['warnings']:
                print(f"    {Fore.YELLOW}• {warning}{Style.RESET_ALL}")
                
        # ============ SUSPICIOUS INDICATORS ============
        suspicious_indicators = []
        
        # Check for mismatch between From and Return-Path
        from_emails = addresses.get('From', [])
        return_path = addresses.get('Return-Path', [])
        
        if from_emails and return_path:
            from_domain = from_emails[0].split('@')[-1] if '@' in from_emails[0] else ''
            return_domain = return_path[0].split('@')[-1] if '@' in return_path[0] else ''
            
            if from_domain and return_domain and from_domain != return_domain:
                suspicious_indicators.append({
                    'type': 'Domain Mismatch',
                    'details': f"From domain '{from_domain}' differs from Return-Path '{return_domain}'",
                    'severity': 'HIGH'
                })
                
        # Check for missing authentication
        if not self.security_evaluation['spf_valid'] and not self.security_evaluation['dkim_valid']:
            suspicious_indicators.append({
                'type': 'No Authentication',
                'details': 'Email lacks both SPF and DKIM authentication',
                'severity': 'HIGH'
            })
            
        # Check for blacklisted IPs
        for entry in self.received_chain:
            if entry['ip']:
                reputation = self.lookup_ip_reputation(entry['ip'])
                if reputation == 'BLACKLISTED':
                    suspicious_indicators.append({
                        'type': 'Blacklisted IP',
                        'details': f"Server IP {entry['ip']} is blacklisted",
                        'severity': 'CRITICAL'
                    })
                    break
                    
        if suspicious_indicators:
            print(f"\n{Fore.CYAN}[ SUSPICIOUS INDICATORS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for indicator in suspicious_indicators:
                severity = indicator['severity']
                if severity == 'CRITICAL':
                    color = Fore.RED + Style.BRIGHT
                elif severity == 'HIGH':
                    color = Fore.RED
                else:
                    color = Fore.YELLOW
                    
                print(f"\n  {color}[{severity}]{Style.RESET_ALL} {indicator['type']}")
                print(f"      └─ {Fore.WHITE}{indicator['details']}{Style.RESET_ALL}")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if not self.security_evaluation['spf_valid']:
            print(f"\n  {Fore.YELLOW}• Implement SPF record to prevent spoofing{Style.RESET_ALL}")
        if not self.security_evaluation['dkim_valid']:
            print(f"\n  {Fore.YELLOW}• Implement DKIM signing for outgoing emails{Style.RESET_ALL}")
        if not self.security_evaluation['dmarc_valid']:
            print(f"\n  {Fore.YELLOW}• Implement DMARC policy to protect your domain{Style.RESET_ALL}")
        if not self.security_evaluation['tls_used']:
            print(f"\n  {Fore.YELLOW}• Configure TLS for email transmission{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"email_header_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'headers': self.parsed_headers,
            'received_chain': self.received_chain,
            'authentication': self.authentication_results,
            'security_evaluation': self.security_evaluation,
            'addresses': self.extract_email_addresses()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_analyze(self):
        """Interactive email header analysis mode"""
        print(f"{Fore.GREEN}[*] Email Header Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced email forensics and security analysis{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Input Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Paste email headers")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Load from file")
        
        choice = input(f"\n{Fore.YELLOW}[?] Select input method: {Style.RESET_ALL}").strip()
        
        headers_text = ""
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}[?] Paste email headers (Ctrl+D to finish):{Style.RESET_ALL}")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except (EOFError, KeyboardInterrupt):
                headers_text = '\n'.join(lines)
                
        elif choice == "2":
            filename = input(f"{Fore.YELLOW}[?] Enter file path: {Style.RESET_ALL}").strip()
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    headers_text = f.read()
                print(f"{Fore.GREEN}[✓] Loaded {len(headers_text)} characters from {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        if not headers_text.strip():
            print(f"{Fore.RED}[✗] No headers provided{Style.RESET_ALL}")
            return
            
        self.start_time = datetime.now()
        
        # Parse headers
        self.parse_headers(headers_text)
        
        # Evaluate security
        self.evaluate_security()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Email header analysis completed{Style.RESET_ALL}")


def analyze_email_headers(header_file=None):
    """Main entry point for CLI compatibility"""
    analyzer = EmailHeaderAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if header_file:
        # File analysis mode
        try:
            with open(header_file, 'r', encoding='utf-8', errors='ignore') as f:
                headers_text = f.read()
                
            analyzer.start_time = datetime.now()
            analyzer.parse_headers(headers_text)
            analyzer.evaluate_security()
            analyzer.end_time = datetime.now()
            analyzer.generate_report()
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
    else:
        # Interactive mode
        analyzer.interactive_analyze()


if __name__ == "__main__":
    analyze_email_headers()
