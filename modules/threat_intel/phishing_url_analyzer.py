#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: PHISHING URL ANALYZER
Advanced URL Phishing Detection & Threat Intelligence
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import socket
import whois
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Style, init
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class PhishingURLAnalyzer:
    """Advanced phishing URL detection with multiple heuristics"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗     ║
    ║  ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝     ║
    ║  ██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║  ███╗    ║
    ║  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║    ║
    ║  ██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╔╝    ║
    ║  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     ║
    ║                    {Fore.CYAN}PHISHING URL ANALYZER v2.0{Fore.RED}                  ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Suspicious TLDs commonly used in phishing
    SUSPICIOUS_TLDS = [
        '.tk', '.ml', '.ga', '.cf', '.gq',  # Free domains
        '.xyz', '.top', '.club', '.online', '.site', '.win', '.bid',  # Cheap domains
        '.work', '.date', '.review', '.trade', '.science', '.party',  # Often abused
        '.click', '.download', '.loan', '.men', '.accountant'        # Phishing favorites
    ]
    
    # Known phishing keywords in URLs
    PHISHING_KEYWORDS = [
        'login', 'signin', 'verify', 'account', 'secure', 'update', 'confirm',
        'banking', 'paypal', 'amazon', 'apple', 'microsoft', 'google', 'facebook',
        'instagram', 'twitter', 'whatsapp', 'netflix', 'spotify', 'ebay', 'alibaba',
        'authenticate', 'validation', 'verification', 'security', 'credential',
        'password', 'username', 'ssn', 'socialsecurity', 'creditcard', 'debit',
        'shipping', 'billing', 'payment', 'wallet', 'bitcoin', 'crypto',
        'recover', 'restore', 'unlock', 'suspend', 'limited', 'unusual'
    ]
    
    # URL shorteners (often used to hide phishing URLs)
    URL_SHORTENERS = [
        'bit.ly', 'tinyurl.com', 'ow.ly', 'tiny.cc', 'is.gd', 'buff.ly',
        'short.link', 'shorturl.com', 'shorte.st', 'shrinke.me', 'link.tl',
        'qr.net', 'adf.ly', 'goo.gl', 'tiny.pl', 'snip.ly', 'short.cm',
        'clck.ru', 'cutt.ly', 'rb.gy', 'short.link', 'gg.gg', 'v.gd',
        'soo.gd', 's.id', 'tiny.ie', 't2m.io', 'shorturl.ink'
    ]
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.whois_info = {}
        self.ip_addresses = []
        self.threat_score = 0
        self.max_score = 100
        self.risk_factors = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.url_reputation = {}
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_url(self, url):
        """Normalize and validate URL"""
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
            
        parsed = urlparse(url)
        self.parsed_url = parsed
        self.domain = parsed.netloc
        self.url = url
        
        return url
        
    def analyze_url_structure(self):
        """Analyze URL structure for phishing indicators"""
        score = 0
        
        # Check for IP address instead of domain
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
        if re.match(ip_pattern, self.parsed_url.netloc.split(':')[0]):
            self.risk_factors.append({
                'factor': 'IP Address URL',
                'details': 'URL uses IP address instead of domain name',
                'severity': 'HIGH',
                'score_impact': 30
            })
            score += 30
            
        # Check for suspicious TLD
        for tld in self.SUSPICIOUS_TLDS:
            if self.domain.endswith(tld):
                self.risk_factors.append({
                    'factor': 'Suspicious TLD',
                    'details': f'Domain uses {tld} - commonly abused for phishing',
                    'severity': 'MEDIUM',
                    'score_impact': 20
                })
                score += 20
                break
                
        # Check for excessive subdomains
        subdomain_count = self.domain.count('.') - 1
        if subdomain_count > 2:
            self.risk_factors.append({
                'factor': 'Excessive Subdomains',
                'details': f'{subdomain_count} subdomains detected - often used for deception',
                'severity': 'MEDIUM',
                'score_impact': 15
            })
            score += 15
            
        # Check for URL shorteners
        for shortener in self.URL_SHORTENERS:
            if shortener in self.domain:
                self.risk_factors.append({
                    'factor': 'URL Shortener',
                    'details': f'URL uses {shortener} - may hide malicious destination',
                    'severity': 'MEDIUM',
                    'score_impact': 25
                })
                score += 25
                break
                
        # Check for suspicious keywords in URL
        url_lower = self.url.lower()
        found_keywords = []
        for keyword in self.PHISHING_KEYWORDS:
            if keyword in url_lower:
                found_keywords.append(keyword)
                
        if found_keywords:
            self.risk_factors.append({
                'factor': 'Phishing Keywords',
                'details': f'Suspicious keywords: {", ".join(found_keywords[:5])}',
                'severity': 'HIGH',
                'score_impact': 25
            })
            score += 25
            
        # Check for '@' symbol (credentials in URL)
        if '@' in self.url:
            self.risk_factors.append({
                'factor': 'Credentials in URL',
                'details': 'URL contains @ symbol - may be attempting credential harvesting',
                'severity': 'CRITICAL',
                'score_impact': 40
            })
            score += 40
            
        # Check for excessive special characters
        special_chars = sum(1 for c in self.url if c in ['-', '_', '.', '~', ':', '/', '?', '#', '[', ']', '@', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '='])
        if special_chars > 20:
            self.risk_factors.append({
                'factor': 'Excessive Special Characters',
                'details': f'{special_chars} special characters - unusual URL pattern',
                'severity': 'LOW',
                'score_impact': 10
            })
            score += 10
            
        # Check for HTTPS
        if self.parsed_url.scheme != 'https':
            self.risk_factors.append({
                'factor': 'No HTTPS',
                'details': 'URL does not use HTTPS encryption',
                'severity': 'MEDIUM',
                'score_impact': 15
            })
            score += 15
        else:
            # Check for valid HTTPS (can't fully verify, but note it)
            self.risk_factors.append({
                'factor': 'HTTPS Enabled',
                'details': 'URL uses HTTPS - positive indicator',
                'severity': 'INFO',
                'score_impact': -10
            })
            score -= 10
            
        return score
        
    def analyze_domain_age(self):
        """Check domain age via WHOIS"""
        score = 0
        
        try:
            w = whois.whois(self.domain)
            
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
                
            if creation_date:
                age_days = (datetime.now() - creation_date).days
                age_years = age_days / 365
                
                self.whois_info = {
                    'creation_date': str(creation_date),
                    'age_days': age_days,
                    'age_years': round(age_years, 1),
                    'registrar': w.registrar,
                    'org': w.org
                }
                
                # New domains are more suspicious
                if age_days < 7:
                    self.risk_factors.append({
                        'factor': 'Newly Registered Domain',
                        'details': f'Domain registered {age_days} days ago - very suspicious',
                        'severity': 'CRITICAL',
                        'score_impact': 40
                    })
                    score += 40
                elif age_days < 30:
                    self.risk_factors.append({
                        'factor': 'Recently Registered Domain',
                        'details': f'Domain registered {age_days} days ago',
                        'severity': 'HIGH',
                        'score_impact': 30
                    })
                    score += 30
                elif age_days < 90:
                    self.risk_factors.append({
                        'factor': 'Moderately New Domain',
                        'details': f'Domain registered {age_days} days ago',
                        'severity': 'MEDIUM',
                        'score_impact': 20
                    })
                    score += 20
                elif age_days < 365:
                    self.risk_factors.append({
                        'factor': 'Domain Under 1 Year',
                        'details': f'Domain registered {age_days} days ago',
                        'severity': 'LOW',
                        'score_impact': 10
                    })
                    score += 10
                else:
                    self.risk_factors.append({
                        'factor': 'Established Domain',
                        'details': f'Domain registered {age_years:.1f} years ago - positive indicator',
                        'severity': 'INFO',
                        'score_impact': -20
                    })
                    score -= 20
            else:
                self.risk_factors.append({
                    'factor': 'WHOIS Privacy',
                    'details': 'Domain registration date hidden - may indicate malicious intent',
                    'severity': 'MEDIUM',
                    'score_impact': 20
                })
                score += 20
                
        except Exception as e:
            self.risk_factors.append({
                'factor': 'WHOIS Lookup Failed',
                'details': f'Unable to retrieve WHOIS information: {str(e)[:50]}',
                'severity': 'INFO',
                'score_impact': 0
            })
            
        return score
        
    def check_ssl_certificate(self):
        """Check SSL certificate validity"""
        score = 0
        
        if self.parsed_url.scheme != 'https':
            return score
            
        try:
            import ssl
            import socket
            
            hostname = self.parsed_url.netloc.split(':')[0]
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiration
                    not_after = cert.get('notAfter')
                    if not_after:
                        expiry_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                        days_remaining = (expiry_date - datetime.now()).days
                        
                        if days_remaining < 0:
                            self.risk_factors.append({
                                'factor': 'Expired SSL Certificate',
                                'details': f'Certificate expired {abs(days_remaining)} days ago',
                                'severity': 'CRITICAL',
                                'score_impact': 30
                            })
                            score += 30
                        elif days_remaining < 30:
                            self.risk_factors.append({
                                'factor': 'SSL Certificate Expiring Soon',
                                'details': f'Certificate expires in {days_remaining} days',
                                'severity': 'MEDIUM',
                                'score_impact': 15
                            })
                            score += 15
                            
                    # Check if certificate is self-signed (basic check)
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    subject = dict(x[0] for x in cert.get('subject', []))
                    
                    if issuer.get('commonName') == subject.get('commonName'):
                        self.risk_factors.append({
                            'factor': 'Self-Signed Certificate',
                            'details': 'Certificate is self-signed - less trustworthy',
                            'severity': 'MEDIUM',
                            'score_impact': 20
                        })
                        score += 20
                        
        except Exception as e:
            self.risk_factors.append({
                'factor': 'SSL Check Failed',
                'details': f'Unable to verify SSL certificate: {str(e)[:50]}',
                'severity': 'INFO',
                'score_impact': 0
            })
            
        return score
        
    def check_google_safe_browsing(self):
        """Check against Google Safe Browsing (requires API key)"""
        # This would require API key - for now, we'll note it's not configured
        self.risk_factors.append({
            'factor': 'Google Safe Browsing',
            'details': 'API key not configured - skipping check',
            'severity': 'INFO',
            'score_impact': 0
        })
        return 0
        
    def resolve_domain(self):
        """Resolve domain to IP addresses"""
        try:
            hostname = self.parsed_url.netloc.split(':')[0]
            ips = socket.gethostbyname_ex(hostname)[2]
            self.ip_addresses = ips
            
            if len(ips) > 1:
                self.risk_factors.append({
                    'factor': 'Multiple IP Addresses',
                    'details': f'Domain resolves to {len(ips)} IP addresses - may use CDN',
                    'severity': 'INFO',
                    'score_impact': 0
                })
                
        except socket.gaierror:
            self.risk_factors.append({
                'factor': 'Domain Resolution Failed',
                'details': 'Unable to resolve domain to IP address',
                'severity': 'HIGH',
                'score_impact': 25
            })
            return 25
            
        return 0
        
    def calculate_threat_score(self):
        """Calculate overall threat score"""
        self.threat_score = 0
        
        # Run all checks
        self.threat_score += self.analyze_url_structure()
        self.threat_score += self.analyze_domain_age()
        self.threat_score += self.check_ssl_certificate()
        self.threat_score += self.resolve_domain()
        
        # Normalize score to 0-100
        self.threat_score = min(100, max(0, self.threat_score))
        
        return self.threat_score
        
    def generate_report(self):
        """Generate comprehensive phishing analysis report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] PHISHING URL ANALYSIS REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Analyzed URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ THREAT SCORE ============
        print(f"\n{Fore.CYAN}[ THREAT SCORE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Visual score bar
        bar_length = 40
        filled_length = int(bar_length * self.threat_score / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if self.threat_score >= 80:
            score_color = Fore.RED + Style.BRIGHT
            threat_level = 'CRITICAL'
        elif self.threat_score >= 60:
            score_color = Fore.RED
            threat_level = 'HIGH'
        elif self.threat_score >= 40:
            score_color = Fore.YELLOW
            threat_level = 'MEDIUM'
        elif self.threat_score >= 20:
            score_color = Fore.CYAN
            threat_level = 'LOW'
        else:
            score_color = Fore.GREEN
            threat_level = 'CLEAN'
            
        print(f"\n  Score: {score_color}{self.threat_score}/100{Style.RESET_ALL}")
        print(f"  Bar:   {score_color}[{bar}]{Style.RESET_ALL}")
        print(f"  Level: {score_color}{threat_level}{Style.RESET_ALL}")
        
        if threat_level == 'CRITICAL':
            print(f"\n  {Fore.RED}{Style.BRIGHT}[!] THIS URL IS HIGHLY SUSPICIOUS - DO NOT VISIT{Style.RESET_ALL}")
        elif threat_level == 'HIGH':
            print(f"\n  {Fore.RED}[!] This URL shows strong phishing indicators{Style.RESET_ALL}")
        elif threat_level == 'MEDIUM':
            print(f"\n  {Fore.YELLOW}[!] This URL has some suspicious characteristics{Style.RESET_ALL}")
            
        # ============ URL ANALYSIS ============
        print(f"\n{Fore.CYAN}[ URL STRUCTURE ANALYSIS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}Scheme: {self.parsed_url.scheme.upper()}{Style.RESET_ALL}")
        print(f"  Domain: {self.parsed_url.netloc}")
        print(f"  Path: {self.parsed_url.path or '/'}")
        print(f"  Query Parameters: {len(parse_qs(self.parsed_url.query)) if self.parsed_url.query else 0}")
        print(f"  Fragment: {self.parsed_url.fragment or 'None'}")
        
        # ============ DOMAIN INFORMATION ============
        print(f"\n{Fore.CYAN}[ DOMAIN INTELLIGENCE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.whois_info:
            print(f"\n  {Fore.WHITE}Creation Date: {self.whois_info.get('creation_date', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Domain Age: {self.whois_info.get('age_days', 'Unknown')} days ({self.whois_info.get('age_years', 'Unknown')} years)")
            print(f"  Registrar: {self.whois_info.get('registrar', 'Unknown')[:50] if self.whois_info.get('registrar') else 'Unknown'}")
            print(f"  Organization: {self.whois_info.get('org', 'Unknown')[:50] if self.whois_info.get('org') else 'Unknown'}")
        else:
            print(f"\n  {Fore.YELLOW}[!] WHOIS information unavailable{Style.RESET_ALL}")
            
        if self.ip_addresses:
            print(f"\n  {Fore.WHITE}IP Addresses:{Style.RESET_ALL}")
            for ip in self.ip_addresses[:3]:
                print(f"    └─ {ip}")
                
        # ============ RISK FACTORS ============
        print(f"\n{Fore.CYAN}[ IDENTIFIED RISK FACTORS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.risk_factors:
            # Sort by severity
            severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
            sorted_factors = sorted(
                [f for f in self.risk_factors if f['score_impact'] > 0],
                key=lambda x: severity_order.get(x['severity'], 5)
            )
            
            for factor in sorted_factors:
                severity = factor['severity']
                if severity == 'CRITICAL':
                    sev_color = Fore.RED + Style.BRIGHT
                elif severity == 'HIGH':
                    sev_color = Fore.RED
                elif severity == 'MEDIUM':
                    sev_color = Fore.YELLOW
                elif severity == 'LOW':
                    sev_color = Fore.CYAN
                else:
                    sev_color = Fore.GREEN
                    
                print(f"\n  {sev_color}[{severity}]{Style.RESET_ALL} {factor['factor']}")
                print(f"      └─ {Fore.WHITE}{factor['details']}{Style.RESET_ALL}")
                print(f"      └─ Impact: {sev_color}{factor['score_impact']} points{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.GREEN}[✓] No significant risk factors identified{Style.RESET_ALL}")
            
        # ============ POSITIVE INDICATORS ============
        positive_factors = [f for f in self.risk_factors if f['score_impact'] < 0]
        
        if positive_factors:
            print(f"\n{Fore.CYAN}[ POSITIVE INDICATORS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for factor in positive_factors:
                print(f"\n  {Fore.GREEN}[✓]{Style.RESET_ALL} {factor['factor']}")
                print(f"      └─ {Fore.WHITE}{factor['details']}{Style.RESET_ALL}")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.threat_score >= 60:
            print(f"""
  {Fore.RED}1. DO NOT VISIT THIS URL{Style.RESET_ALL}
  {Fore.RED}2. Report to Google Safe Browsing{Style.RESET_ALL}
  {Fore.RED}3. Block at network level{Style.RESET_ALL}
  {Fore.RED}4. Educate users about this threat{Style.RESET_ALL}
            """)
        elif self.threat_score >= 40:
            print(f"""
  {Fore.YELLOW}1. Exercise extreme caution{Style.RESET_ALL}
  {Fore.YELLOW}2. Verify domain ownership{Style.RESET_ALL}
  {Fore.YELLOW}3. Check for HTTPS validity{Style.RESET_ALL}
  {Fore.YELLOW}4. Monitor for similar domains{Style.RESET_ALL}
            """)
        elif self.threat_score >= 20:
            print(f"""
  {Fore.CYAN}1. Verify the URL carefully{Style.RESET_ALL}
  {Fore.CYAN}2. Check for typosquatting{Style.RESET_ALL}
  {Fore.CYAN}3. Enable phishing protection{Style.RESET_ALL}
            """)
        else:
            print(f"""
  {Fore.GREEN}1. URL appears legitimate{Style.RESET_ALL}
  {Fore.GREEN}2. Maintain normal security practices{Style.RESET_ALL}
  {Fore.GREEN}3. Still verify before entering credentials{Style.RESET_ALL}
            """)
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] This is a heuristic analysis - false positives possible{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Always verify URLs through official channels{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"phishing_scan_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'url': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'threat_score': self.threat_score,
            'threat_level': self.get_threat_level(self.threat_score),
            'risk_factors': self.risk_factors,
            'whois_info': self.whois_info,
            'ip_addresses': self.ip_addresses,
            'parsed_url': {
                'scheme': self.parsed_url.scheme,
                'netloc': self.parsed_url.netloc,
                'path': self.parsed_url.path,
                'params': self.parsed_url.params,
                'query': self.parsed_url.query,
                'fragment': self.parsed_url.fragment
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def get_threat_level(self, score):
        """Get threat level from score"""
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'LOW'
        else:
            return 'CLEAN'
            
    def interactive_scan(self):
        """Interactive phishing URL analysis mode"""
        print(f"{Fore.GREEN}[*] Phishing URL Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multi-heuristic detection engine{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter URL to analyze: {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No URL specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Analyzing URL for phishing indicators...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take a few seconds...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Calculate threat score
        self.calculate_threat_score()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Phishing URL analysis completed{Style.RESET_ALL}")


def phishing_check(url=None):
    """Main entry point for CLI compatibility"""
    analyzer = PhishingURLAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if url:
        # Direct scan mode
        analyzer.normalize_url(url)
        analyzer.start_time = datetime.now()
        analyzer.calculate_threat_score()
        analyzer.end_time = datetime.now()
        analyzer.generate_report()
    else:
        # Interactive mode
        analyzer.interactive_scan()


if __name__ == "__main__":
    phishing_check()
