#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: CERTIFICATE INTELLIGENCE
Advanced TLS/SSL Certificate Analysis & Transparency Logs
Author: ICAT Project | Linxploit.xyz
"""

import requests
import json
import socket
import ssl
import hashlib
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import certifi
import re

init(autoreset=True)

class CertificateIntelligence:
    """Advanced TLS/SSL certificate analysis and CT log intelligence"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗███████╗██████╗ ████████╗██╗███████╗██╗ ██████╗ █████╗ ████████╗███████╗     ║
    ║  ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝     ║
    ║  ██║     █████╗  ██████╔╝   ██║   ██║█████╗  ██║██║     ███████║   ██║   █████╗       ║
    ║  ██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝  ██║██║     ██╔══██║   ██║   ██╔══╝       ║
    ║  ╚██████╗███████╗██║  ██║   ██║   ██║██║     ██║╚██████╗██║  ██║   ██║   ███████╗     ║
    ║   ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝     ║
    ║                    {Fore.CYAN}CERTIFICATE INTELLIGENCE & CT LOGS v2.0{Fore.RED}        ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Certificate Transparency log sources
    CRT_SH_URL = "https://crt.sh/?q={}&output=json"
    CRT_SH_ID_URL = "https://crt.sh/?id={}"
    
    def __init__(self):
        self.domain = None
        self.port = 443
        self.live_cert = None
        self.ct_logs = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_domain(self, domain):
        """Normalize domain input"""
        domain = domain.strip().lower()
        domain = re.sub(r'^https?://', '', domain)
        domain = domain.split('/')[0]
        domain = re.sub(r'^www\.', '', domain)
        self.domain = domain
        return domain
        
    def get_live_certificate(self, domain, port=443):
        """Retrieve live TLS certificate from domain"""
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    der_cert = ssock.getpeercert(binary_form=True)
                    
                    cert_info = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'serial_number': cert.get('serialNumber'),
                        'version': cert.get('version'),
                        'fingerprint_sha1': hashlib.sha1(der_cert).hexdigest(),
                        'fingerprint_sha256': hashlib.sha256(der_cert).hexdigest(),
                    }
                    
                    # Subject Alternative Names
                    san = []
                    for ext in cert.get('subjectAltName', []):
                        if ext[0] == 'DNS':
                            san.append(ext[1])
                    cert_info['san'] = san
                    
                    self.live_cert = cert_info
                    return cert_info
                    
        except Exception as e:
            return {'error': str(e)}
            
    def query_crt_sh(self, domain):
        """Query crt.sh Certificate Transparency logs"""
        certificates = []
        
        try:
            url = self.CRT_SH_URL.format(domain)
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                for entry in data[:100]:  # Limit to 100 entries
                    cert = {
                        'id': entry.get('id'),
                        'issuer_name': entry.get('issuer_name'),
                        'name_value': entry.get('name_value'),
                        'not_before': entry.get('not_before'),
                        'not_after': entry.get('not_after'),
                        'serial_number': entry.get('serial_number'),
                    }
                    certificates.append(cert)
                    
            self.ct_logs = certificates
            return certificates
            
        except Exception as e:
            return []
            
    def extract_subdomains_from_ct(self):
        """Extract unique subdomains from CT logs"""
        subdomains = set()
        
        for cert in self.ct_logs:
            name_value = cert.get('name_value', '')
            # Split multi-domain entries
            for name in name_value.split('\n'):
                name = name.strip().lower()
                if name.endswith(self.domain) and name != self.domain:
                    subdomains.add(name)
                    
        return sorted(list(subdomains))
        
    def analyze_certificate_security(self, cert):
        """Analyze certificate for security issues"""
        issues = []
        
        if not cert or 'error' in cert:
            return issues
            
        # Check expiration
        if 'not_after' in cert:
            try:
                expiry_date = datetime.strptime(cert['not_after'], "%b %d %H:%M:%S %Y %Z")
                days_remaining = (expiry_date - datetime.now()).days
                
                if days_remaining < 0:
                    issues.append({
                        'severity': 'CRITICAL',
                        'issue': f'Certificate EXPIRED {abs(days_remaining)} days ago'
                    })
                elif days_remaining < 7:
                    issues.append({
                        'severity': 'CRITICAL',
                        'issue': f'Certificate expires in {days_remaining} days - RENEW IMMEDIATELY'
                    })
                elif days_remaining < 30:
                    issues.append({
                        'severity': 'HIGH',
                        'issue': f'Certificate expires in {days_remaining} days'
                    })
                elif days_remaining < 90:
                    issues.append({
                        'severity': 'MEDIUM',
                        'issue': f'Certificate expires in {days_remaining} days'
                    })
            except:
                pass
                
        # Check for self-signed
        if 'issuer' in cert and 'subject' in cert:
            issuer_cn = cert['issuer'].get('commonName', '')
            subject_cn = cert['subject'].get('commonName', '')
            
            if issuer_cn == subject_cn:
                issues.append({
                    'severity': 'HIGH',
                    'issue': 'Self-signed certificate detected'
                })
                
        return issues
        
    def generate_report(self):
        """Generate comprehensive certificate intelligence report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] CERTIFICATE INTELLIGENCE REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ LIVE CERTIFICATE ============
        print(f"\n{Fore.CYAN}[ LIVE CERTIFICATE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.live_cert and 'error' not in self.live_cert:
            # Subject
            if 'subject' in self.live_cert:
                print(f"\n  {Fore.WHITE}Subject:{Style.RESET_ALL}")
                for key, value in self.live_cert['subject'].items():
                    print(f"    {key}: {Fore.CYAN}{value}{Style.RESET_ALL}")
                    
            # Issuer
            if 'issuer' in self.live_cert:
                print(f"\n  {Fore.WHITE}Issuer:{Style.RESET_ALL}")
                for key, value in self.live_cert['issuer'].items():
                    print(f"    {key}: {Fore.CYAN}{value}{Style.RESET_ALL}")
                    
            # Validity
            if 'not_before' in self.live_cert:
                print(f"\n  {Fore.WHITE}Valid From:{Style.RESET_ALL} {self.live_cert['not_before']}")
            if 'not_after' in self.live_cert:
                print(f"  {Fore.WHITE}Valid Until:{Style.RESET_ALL} {self.live_cert['not_after']}")
                
                # Calculate days remaining
                try:
                    expiry = datetime.strptime(self.live_cert['not_after'], "%b %d %H:%M:%S %Y %Z")
                    days = (expiry - datetime.now()).days
                    
                    if days < 0:
                        print(f"  {Fore.WHITE}Status:{Style.RESET_ALL} {Fore.RED}EXPIRED ({abs(days)} days ago){Style.RESET_ALL}")
                    elif days < 7:
                        print(f"  {Fore.WHITE}Status:{Style.RESET_ALL} {Fore.RED}EXPIRING IN {days} DAYS{Style.RESET_ALL}")
                    elif days < 30:
                        print(f"  {Fore.WHITE}Status:{Style.RESET_ALL} {Fore.YELLOW}Expires in {days} days{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.WHITE}Status:{Style.RESET_ALL} {Fore.GREEN}Valid ({days} days remaining){Style.RESET_ALL}")
                except:
                    pass
                    
            # Fingerprints
            if 'fingerprint_sha256' in self.live_cert:
                fp = self.live_cert['fingerprint_sha256']
                print(f"\n  {Fore.WHITE}SHA-256 Fingerprint:{Style.RESET_ALL}")
                print(f"    {fp[:32]}")
                print(f"    {fp[32:]}")
                
            # Subject Alternative Names
            if 'san' in self.live_cert and self.live_cert['san']:
                print(f"\n  {Fore.WHITE}Subject Alternative Names:{Style.RESET_ALL}")
                for name in self.live_cert['san'][:20]:
                    print(f"    • {name}")
                if len(self.live_cert['san']) > 20:
                    print(f"    ... and {len(self.live_cert['san']) - 20} more")
                    
            # Security analysis
            issues = self.analyze_certificate_security(self.live_cert)
            if issues:
                print(f"\n  {Fore.WHITE}Security Issues:{Style.RESET_ALL}")
                for issue in issues:
                    severity = issue['severity']
                    if severity == 'CRITICAL':
                        color = Fore.RED + Style.BRIGHT
                    elif severity == 'HIGH':
                        color = Fore.RED
                    elif severity == 'MEDIUM':
                        color = Fore.YELLOW
                    else:
                        color = Fore.CYAN
                        
                    print(f"    {color}[{severity}]{Style.RESET_ALL} {issue['issue']}")
                    
        else:
            print(f"\n  {Fore.YELLOW}[!] Could not retrieve live certificate{Style.RESET_ALL}")
            if self.live_cert and 'error' in self.live_cert:
                print(f"      └─ {self.live_cert['error']}")
                
        # ============ CERTIFICATE TRANSPARENCY LOGS ============
        print(f"\n{Fore.CYAN}[ CERTIFICATE TRANSPARENCY LOGS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.ct_logs:
            print(f"\n  {Fore.WHITE}Found {len(self.ct_logs)} certificates in CT logs{Style.RESET_ALL}")
            
            # Show recent certificates
            print(f"\n  {Fore.WHITE}Recent certificates (first 10):{Style.RESET_ALL}")
            for i, cert in enumerate(self.ct_logs[:10], 1):
                print(f"\n    {i}. Certificate ID: {cert.get('id')}")
                print(f"       ├─ Issuer: {cert.get('issuer_name', 'Unknown')[:60]}...")
                print(f"       ├─ Not Before: {cert.get('not_before', 'Unknown')}")
                print(f"       └─ Not After: {cert.get('not_after', 'Unknown')}")
                
            # Extract subdomains
            subdomains = self.extract_subdomains_from_ct()
            if subdomains:
                print(f"\n  {Fore.WHITE}Discovered Subdomains from CT logs:{Style.RESET_ALL}")
                for subdomain in subdomains[:30]:
                    print(f"    • {subdomain}")
                if len(subdomains) > 30:
                    print(f"    ... and {len(subdomains) - 30} more")
                    
        else:
            print(f"\n  {Fore.YELLOW}[!] No certificates found in CT logs{Style.RESET_ALL}")
            
        # ============ CERTIFICATE TIMELINE ============
        if self.ct_logs:
            print(f"\n{Fore.CYAN}[ CERTIFICATE TIMELINE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Extract issuance dates
            dates = []
            for cert in self.ct_logs:
                if cert.get('not_before'):
                    try:
                        date = datetime.strptime(cert['not_before'], "%Y-%m-%dT%H:%M:%S")
                        dates.append(date)
                    except:
                        pass
                        
            if dates:
                dates.sort()
                first_issuance = dates[0]
                last_issuance = dates[-1]
                
                print(f"\n  {Fore.WHITE}First certificate issued:{Style.RESET_ALL} {first_issuance.strftime('%Y-%m-%d')}")
                print(f"  {Fore.WHITE}Latest certificate issued:{Style.RESET_ALL} {last_issuance.strftime('%Y-%m-%d')}")
                print(f"  {Fore.WHITE}Total certificates over time:{Style.RESET_ALL} {len(dates)}")
                
                # Calculate frequency
                days_span = (last_issuance - first_issuance).days
                if days_span > 0:
                    certs_per_day = len(dates) / days_span
                    print(f"  {Fore.WHITE}Average certificates per day:{Style.RESET_ALL} {certs_per_day:.2f}")
                    
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.live_cert and 'error' not in self.live_cert:
            issues = self.analyze_certificate_security(self.live_cert)
            if issues:
                for issue in issues:
                    if 'EXPIRED' in issue['issue'] or 'expires' in issue['issue']:
                        print(f"\n  {Fore.RED}• {issue['issue']}{Style.RESET_ALL}")
                        print(f"    └─ Renew certificate immediately")
            else:
                print(f"\n  {Fore.GREEN}• Certificate is valid and properly configured{Style.RESET_ALL}")
                
        if self.ct_logs:
            print(f"\n  {Fore.CYAN}• CT logs indicate active certificate issuance{Style.RESET_ALL}")
            print(f"    └─ Monitor for unauthorized certificates")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"cert_intel_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'live_certificate': self.live_cert,
            'ct_logs': self.ct_logs[:500],  # Limit size
            'discovered_subdomains': self.extract_subdomains_from_ct()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_analyze(self):
        """Interactive certificate intelligence mode"""
        print(f"{Fore.GREEN}[*] Certificate Intelligence initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced TLS/SSL analysis & CT log mining{Style.RESET_ALL}\n")
        
        # Get domain
        domain_input = input(f"{Fore.YELLOW}[?] Enter domain to analyze: {Style.RESET_ALL}").strip()
        
        if not domain_input:
            print(f"{Fore.RED}[✗] No domain specified{Style.RESET_ALL}")
            return
            
        self.normalize_domain(domain_input)
        
        # Get port
        try:
            port_input = input(f"{Fore.YELLOW}[?] Port (default 443): {Style.RESET_ALL}").strip()
            self.port = int(port_input) if port_input else 443
        except:
            self.port = 443
            
        print(f"\n{Fore.YELLOW}[*] Retrieving live certificate from {self.domain}:{self.port}...{Style.RESET_ALL}")
        
        self.start_time = datetime.now()
        
        # Get live certificate
        self.get_live_certificate(self.domain, self.port)
        
        print(f"{Fore.YELLOW}[*] Querying Certificate Transparency logs...{Style.RESET_ALL}")
        
        # Query CT logs
        self.query_crt_sh(self.domain)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Certificate intelligence completed{Style.RESET_ALL}")


def crtsh_certificate_intel(domain, limit=30):
    """Simplified function for certificate intelligence (for whois_integration)"""
    analyzer = CertificateIntelligence()
    analyzer.normalize_domain(domain)
    certificates = analyzer.query_crt_sh(domain)
    
    # Extract subdomains
    subdomains = analyzer.extract_subdomains_from_ct()
    return subdomains[:limit]


def certificate_intelligence(domain=None):
    """Main entry point for CLI compatibility"""
    analyzer = CertificateIntelligence()
    
    # Display banner
    analyzer.print_header()
    
    if domain:
        # Direct scan mode
        analyzer.normalize_domain(domain)
        analyzer.start_time = datetime.now()
        
        print(f"\n  {Fore.YELLOW}[*] Gathering certificate intelligence for {domain}...{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] Querying live certificate and CT logs{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] This may take 5-15 seconds{Style.RESET_ALL}\n")
        
        try:
            analyzer.get_live_certificate(analyzer.domain)
            analyzer.query_crt_sh(analyzer.domain)
            analyzer.end_time = datetime.now()
            analyzer.generate_report()
        except Exception as e:
            print(f"{Fore.RED}[✗] Certificate intelligence failed: {e}{Style.RESET_ALL}")
    else:
        # Interactive mode
        analyzer.interactive_analyze()


if __name__ == "__main__":
    certificate_intelligence()