#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: SSL/TLS SECURITY INSPECTOR
Advanced Certificate Analysis & Protocol Security Scanner
Author: ICAT Project | Linxploit.xyz
"""

import ssl
import socket
import certifi
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import json
import hashlib
import base64
import re
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class SSLTLSInspector:
    """Advanced SSL/TLS security analysis tool"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗███████╗██╗         ████████╗██╗     ███████╗         ║
    ║  ██╔════╝██╔════╝██║         ╚══██╔══╝██║     ██╔════╝         ║
    ║  ███████╗███████╗██║            ██║   ██║     ███████╗         ║
    ║  ╚════██║╚════██║██║            ██║   ██║     ╚════██║         ║
    ║  ███████║███████║███████╗       ██║   ███████╗███████║         ║
    ║  ╚══════╝╚══════╝╚══════╝       ╚═╝   ╚══════╝╚══════╝         ║
    ║                    {Fore.CYAN}SSL/TLS SECURITY INSPECTOR v2.0{Fore.RED}            ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Protocol security ratings
    PROTOCOL_SCORES = {
        'SSLv3': {'score': 0, 'risk': 'CRITICAL', 'color': Fore.RED, 'deprecated': True},
        'TLSv1.0': {'score': 1, 'risk': 'HIGH', 'color': Fore.RED, 'deprecated': True},
        'TLSv1.1': {'score': 2, 'risk': 'HIGH', 'color': Fore.YELLOW, 'deprecated': True},
        'TLSv1.2': {'score': 3, 'risk': 'MEDIUM', 'color': Fore.GREEN, 'deprecated': False},
        'TLSv1.3': {'score': 4, 'risk': 'LOW', 'color': Fore.CYAN, 'deprecated': False},
    }
    
    def __init__(self):
        self.host = None
        self.port = 443
        self.cert_data = {}
        self.protocols = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.security_headers = {}
        self.vulnerabilities = []
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def resolve_host(self, host):
        """Resolve hostname to IP"""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return None
            
    def get_certificate_info(self, host, port=443):
        """Retrieve and parse SSL certificate"""
        cert_info = {}
        
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Basic certificate info
                    cert_info['subject'] = {}
                    for item in cert.get('subject', []):
                        for key, value in item:
                            cert_info['subject'][key] = value
                            
                    cert_info['issuer'] = {}
                    for item in cert.get('issuer', []):
                        for key, value in item:
                            cert_info['issuer'][key] = value
                            
                    cert_info['not_before'] = cert.get('notBefore', 'Unknown')
                    cert_info['not_after'] = cert.get('notAfter', 'Unknown')
                    cert_info['serial_number'] = cert.get('serialNumber', 'Unknown')
                    cert_info['version'] = cert.get('version', 'Unknown')
                    
                    # SAN (Subject Alternative Names)
                    cert_info['san'] = []
                    for ext in cert.get('subjectAltName', []):
                        if ext[0] == 'DNS':
                            cert_info['san'].append(ext[1])
                            
                    # Get raw certificate for fingerprinting
                    der_cert = ssock.getpeercert(binary_form=True)
                    cert_info['fingerprint_sha1'] = hashlib.sha1(der_cert).hexdigest()
                    cert_info['fingerprint_sha256'] = hashlib.sha256(der_cert).hexdigest()
                    
                    # Try to get key details from cert info
                    if 'subject' in cert_info and 'commonName' in cert_info['subject']:
                        cert_info['cn'] = cert_info['subject']['commonName']
                        
                    # Parse validity period
                    if cert_info['not_after'] != 'Unknown':
                        try:
                            expiry_date = datetime.strptime(cert_info['not_after'], "%b %d %H:%M:%S %Y %Z")
                            now = datetime.utcnow()
                            days_remaining = (expiry_date - now).days
                            cert_info['days_remaining'] = days_remaining
                            cert_info['expiry_date'] = str(expiry_date)
                        except:
                            pass
                            
        except Exception as e:
            cert_info['error'] = str(e)
            
        return cert_info
        
    def check_protocol_support(self, host, port=443):
        """Check which TLS protocols are supported"""
        protocols = {}
        
        # Test SSLv3
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            context.options |= ssl.OP_NO_TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    protocols['SSLv3'] = {'supported': True, 'version': 'SSLv3'}
        except:
            protocols['SSLv3'] = {'supported': False}
            
        # Test TLSv1.0
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    protocols['TLSv1.0'] = {'supported': True, 'version': ssock.version()}
        except:
            protocols['TLSv1.0'] = {'supported': False}
            
        # Test TLSv1.1
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    protocols['TLSv1.1'] = {'supported': True, 'version': ssock.version()}
        except:
            protocols['TLSv1.1'] = {'supported': False}
            
        # Test TLSv1.2
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    protocols['TLSv1.2'] = {'supported': True, 'version': ssock.version()}
        except:
            protocols['TLSv1.2'] = {'supported': False}
            
        # Test TLSv1.3
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    protocols['TLSv1.3'] = {'supported': True, 'version': ssock.version()}
        except:
            protocols['TLSv1.3'] = {'supported': False}
            
        return protocols
        
    def check_security_headers(self, host):
        """Check HTTP security headers over HTTPS"""
        try:
            import requests
            url = f"https://{host}"
            response = requests.get(url, timeout=10, verify=False)
            
            security_headers = {
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security'),
                'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                'X-Frame-Options': response.headers.get('X-Frame-Options'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
                'Referrer-Policy': response.headers.get('Referrer-Policy'),
            }
            
            return security_headers
        except Exception as e:
            return {'error': str(e)}
            
    def analyze_certificate_security(self, cert_info):
        """Analyze certificate for security issues"""
        issues = []
        
        # Check expiration
        if 'days_remaining' in cert_info:
            days = cert_info['days_remaining']
            if days < 0:
                issues.append({'severity': 'CRITICAL', 'issue': f'Certificate EXPIRED {abs(days)} days ago'})
            elif days < 7:
                issues.append({'severity': 'CRITICAL', 'issue': f'Certificate expires in {days} days - URGENT'})
            elif days < 30:
                issues.append({'severity': 'HIGH', 'issue': f'Certificate expires in {days} days'})
            elif days < 90:
                issues.append({'severity': 'MEDIUM', 'issue': f'Certificate expires in {days} days'})
                
        # Check for self-signed certificate (basic heuristic)
        if 'issuer' in cert_info and 'subject' in cert_info:
            issuer_cn = cert_info.get('issuer', {}).get('commonName', '')
            subject_cn = cert_info.get('subject', {}).get('commonName', '')
            if issuer_cn == subject_cn:
                issues.append({'severity': 'MEDIUM', 'issue': 'Self-signed certificate detected'})
                
        return issues
        
    def generate_report(self):
        """Generate comprehensive security report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] SSL/TLS SECURITY REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target: {Fore.LIGHTGREEN_EX}{self.host}:{self.port}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ CERTIFICATE DETAILS ============
        print(f"\n{Fore.CYAN}[ CERTIFICATE DETAILS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if 'error' in self.cert_data:
            print(f"{Fore.RED}  [!] Failed to retrieve certificate: {self.cert_data['error']}{Style.RESET_ALL}")
        else:
            # Subject
            if 'subject' in self.cert_data and self.cert_data['subject']:
                print(f"\n{Fore.YELLOW}  Subject:{Style.RESET_ALL}")
                for key, value in self.cert_data['subject'].items():
                    print(f"    {key}: {Fore.WHITE}{value}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}  Subject: {Fore.RED}Not Available{Style.RESET_ALL}")
                    
            # Issuer
            if 'issuer' in self.cert_data and self.cert_data['issuer']:
                print(f"\n{Fore.YELLOW}  Issuer:{Style.RESET_ALL}")
                for key, value in self.cert_data['issuer'].items():
                    print(f"    {key}: {Fore.WHITE}{value}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}  Issuer: {Fore.RED}Not Available{Style.RESET_ALL}")
                    
            # Validity
            if 'not_before' in self.cert_data and self.cert_data['not_before'] != 'Unknown':
                print(f"\n{Fore.YELLOW}  Valid From: {Fore.WHITE}{self.cert_data['not_before']}{Style.RESET_ALL}")
                
            if 'not_after' in self.cert_data and self.cert_data['not_after'] != 'Unknown':
                expiry_date = self.cert_data['not_after']
                
                if 'days_remaining' in self.cert_data:
                    days = self.cert_data['days_remaining']
                    if days < 0:
                        status_color = Fore.RED
                        status = f"EXPIRED ({abs(days)} days ago)"
                    elif days < 7:
                        status_color = Fore.RED + Style.BRIGHT
                        status = f"EXPIRING IMMINENTLY ({days} days)"
                    elif days < 30:
                        status_color = Fore.YELLOW
                        status = f"EXPIRING SOON ({days} days)"
                    else:
                        status_color = Fore.GREEN
                        status = f"VALID ({days} days remaining)"
                        
                    print(f"{Fore.YELLOW}  Valid Until: {Fore.WHITE}{expiry_date}{Style.RESET_ALL}")
                    print(f"    └─ Status: {status_color}{status}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}  Valid Until: {Fore.WHITE}{expiry_date}{Style.RESET_ALL}")
                    
            # Fingerprints
            if 'fingerprint_sha256' in self.cert_data:
                print(f"\n{Fore.YELLOW}  SHA-256 Fingerprint:{Style.RESET_ALL}")
                fp = self.cert_data['fingerprint_sha256']
                print(f"    {Fore.WHITE}{fp[:32]}{Style.RESET_ALL}")
                print(f"    {Fore.WHITE}{fp[32:]}{Style.RESET_ALL}")
                
            # SAN
            if 'san' in self.cert_data and self.cert_data['san']:
                print(f"\n{Fore.YELLOW}  Subject Alternative Names:{Style.RESET_ALL}")
                for name in self.cert_data['san'][:10]:
                    print(f"    {Fore.WHITE}├─ {name}{Style.RESET_ALL}")
                if len(self.cert_data['san']) > 10:
                    print(f"    {Fore.WHITE}└─ ... and {len(self.cert_data['san']) - 10} more{Style.RESET_ALL}")
                    
        # ============ PROTOCOL SUPPORT ============
        print(f"\n{Fore.CYAN}[ PROTOCOL SUPPORT ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        for protocol, info in self.protocols.items():
            if info.get('supported', False):
                if 'SSL' in protocol:
                    color = Fore.RED
                    risk = 'CRITICAL'
                elif 'TLSv1.0' in protocol or 'TLSv1.1' in protocol:
                    color = Fore.YELLOW
                    risk = 'HIGH'
                elif 'TLSv1.2' in protocol:
                    color = Fore.GREEN
                    risk = 'GOOD'
                else:
                    color = Fore.CYAN
                    risk = 'BEST'
                    
                print(f"  {color}[✓] {protocol}{Style.RESET_ALL} - Risk: {color}{risk}{Style.RESET_ALL}")
            else:
                if 'SSL' in protocol or 'TLSv1.0' in protocol or 'TLSv1.1' in protocol:
                    print(f"  {Fore.GREEN}[✗] {protocol} (disabled - GOOD){Style.RESET_ALL}")
                else:
                    print(f"  {Fore.YELLOW}[✗] {protocol} (not supported){Style.RESET_ALL}")
                    
        # ============ SECURITY ISSUES ============
        print(f"\n{Fore.CYAN}[ SECURITY ANALYSIS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        certificate_issues = self.analyze_certificate_security(self.cert_data)
        
        if certificate_issues:
            for issue in certificate_issues:
                severity = issue['severity']
                if severity == 'CRITICAL':
                    print(f"  {Fore.RED}[CRITICAL] {issue['issue']}{Style.RESET_ALL}")
                elif severity == 'HIGH':
                    print(f"  {Fore.RED}[HIGH] {issue['issue']}{Style.RESET_ALL}")
                elif severity == 'MEDIUM':
                    print(f"  {Fore.YELLOW}[MEDIUM] {issue['issue']}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.YELLOW}[LOW] {issue['issue']}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}[✓] No certificate issues found{Style.RESET_ALL}")
            
        # ============ SECURITY HEADERS ============
        print(f"\n{Fore.CYAN}[ HTTP SECURITY HEADERS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.security_headers:
            if 'error' in self.security_headers:
                print(f"  {Fore.YELLOW}[!] Could not fetch headers: {self.security_headers['error']}{Style.RESET_ALL}")
            else:
                for header, value in self.security_headers.items():
                    if value:
                        print(f"  {Fore.GREEN}[✓] {header}: {Fore.WHITE}{value[:50]}{'...' if len(value) > 50 else ''}{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.RED}[✗] {header} - MISSING{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}[!] No header data available{Style.RESET_ALL}")
                    
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        recommendations = []
        
        # Check for weak protocols
        for protocol, info in self.protocols.items():
            if info.get('supported', False):
                if 'SSL' in protocol:
                    recommendations.append(f"DISABLE {protocol} immediately - CRITICAL vulnerability")
                elif 'TLSv1.0' in protocol:
                    recommendations.append(f"DISABLE {protocol} - deprecated and insecure")
                elif 'TLSv1.1' in protocol:
                    recommendations.append(f"DISABLE {protocol} - deprecated, upgrade to TLSv1.2/1.3")
                    
        # Check HSTS
        if self.security_headers and not self.security_headers.get('error'):
            if not self.security_headers.get('Strict-Transport-Security'):
                recommendations.append("Enable HSTS (Strict-Transport-Security) header")
            if not self.security_headers.get('Content-Security-Policy'):
                recommendations.append("Implement Content-Security-Policy header")
            if not self.security_headers.get('X-Frame-Options'):
                recommendations.append("Add X-Frame-Options header to prevent clickjacking")
                
        # Check certificate expiry
        if 'days_remaining' in self.cert_data:
            days = self.cert_data['days_remaining']
            if days < 30:
                recommendations.append(f"RENEW SSL CERTIFICATE - expires in {days} days")
                
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {Fore.YELLOW}{i}. {Fore.WHITE}{rec}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}[✓] No critical recommendations - SSL/TLS configuration is secure{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"ssl_scan_{self.host}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.host,
            'port': self.port,
            'timestamp': str(self.start_time),
            'certificate': self.cert_data,
            'protocols': self.protocols,
            'security_headers': self.security_headers
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive scanning mode"""
        print(f"{Fore.GREEN}[*] SSL/TLS Security Inspector initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Certificate and protocol analysis{Style.RESET_ALL}\n")
        
        # Get target
        self.host = input(f"{Fore.YELLOW}[?] Enter hostname or IP: {Style.RESET_ALL}").strip()
        
        if not self.host:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        # Resolve host
        ip = self.resolve_host(self.host)
        if not ip:
            print(f"{Fore.RED}[✗] Could not resolve hostname: {self.host}{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}[✓] Resolved: {self.host} -> {ip}{Style.RESET_ALL}")
        
        # Get port
        try:
            port_input = input(f"{Fore.YELLOW}[?] Port (default 443): {Style.RESET_ALL}").strip()
            if port_input:
                self.port = int(port_input)
        except:
            self.port = 443
            
        print(f"\n{Fore.YELLOW}[*] Starting SSL/TLS security scan on {self.host}:{self.port}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take 10-20 seconds...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Perform scans
        print(f"{Fore.CYAN}[1/3] Retrieving certificate information...{Style.RESET_ALL}")
        self.cert_data = self.get_certificate_info(self.host, self.port)
        
        print(f"{Fore.CYAN}[2/3] Testing protocol support...{Style.RESET_ALL}")
        self.protocols = self.check_protocol_support(self.host, self.port)
        
        print(f"{Fore.CYAN}[3/3] Checking security headers...{Style.RESET_ALL}")
        self.security_headers = self.check_security_headers(self.host)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] SSL/TLS inspection completed{Style.RESET_ALL}")


def inspect_ssl_tls(host=None):
    """Main entry point for CLI compatibility"""
    inspector = SSLTLSInspector()
    
    # Display banner
    inspector.print_header()
    
    if host:
        # Direct scan mode
        inspector.host = host
        inspector.port = 443
        
        ip = inspector.resolve_host(host)
        if not ip:
            print(f"{Fore.RED}[✗] Could not resolve hostname: {host}{Style.RESET_ALL}")
            return
            
        inspector.start_time = datetime.now()
        inspector.cert_data = inspector.get_certificate_info(host)
        inspector.protocols = inspector.check_protocol_support(host)
        inspector.security_headers = inspector.check_security_headers(host)
        inspector.end_time = datetime.now()
        
        inspector.generate_report()
    else:
        # Interactive mode
        inspector.interactive_scan()


if __name__ == "__main__":
    inspect_ssl_tls()
