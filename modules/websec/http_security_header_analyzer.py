#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: HTTP SECURITY HEADER ANALYZER
Advanced Web Security Headers Audit & Compliance Testing
Author: ICAT Project | Linxploit.xyz
"""

import requests
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import urllib3
import sys
import time

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class HTTPSecurityHeaderAnalyzer:
    """Advanced HTTP security headers analyzer with compliance checking"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗  ██╗████████╗████████╗██████╗     ███████╗███████╗ ██████╗██╗  ║
    ║  ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗    ██╔════╝██╔════╝██╔════╝██║  ║
    ║  ███████║   ██║      ██║   ██████╔╝    ███████╗█████╗  ██║     ██║  ║
    ║  ██╔══██║   ██║      ██║   ██╔═══╝     ╚════██║██╔══╝  ██║     ██║  ║
    ║  ██║  ██║   ██║      ██║   ██║         ███████║███████╗╚██████╗███████╗
    ║  ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝         ╚══════╝╚══════╝ ╚═════╝╚══════╝
    ║                    {Fore.CYAN}SECURITY HEADER ANALYZER v2.0{Fore.RED}                 ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Comprehensive security headers database with descriptions and recommendations
    SECURITY_HEADERS = {
        'Content-Security-Policy': {
            'description': 'Prevents XSS and data injection attacks',
            'recommendation': "Implement CSP header with 'default-src https:'",
            'severity': 'CRITICAL',
            'score': 20,
            'cwe': 'CWE-79',
            'owasp': 'A7:2017-Cross-Site Scripting (XSS)'
        },
        'Strict-Transport-Security': {
            'description': 'Enforces HTTPS connections',
            'recommendation': "Set 'max-age=31536000; includeSubDomains'",
            'severity': 'CRITICAL',
            'score': 20,
            'cwe': 'CWE-319',
            'owasp': 'A3:2017-Sensitive Data Exposure'
        },
        'X-Content-Type-Options': {
            'description': 'Prevents MIME type sniffing',
            'recommendation': "Set to 'nosniff'",
            'severity': 'HIGH',
            'score': 15,
            'cwe': 'CWE-16',
            'owasp': 'A6:2017-Security Misconfiguration'
        },
        'X-Frame-Options': {
            'description': 'Prevents clickjacking attacks',
            'recommendation': "Set to 'DENY' or 'SAMEORIGIN'",
            'severity': 'HIGH',
            'score': 15,
            'cwe': 'CWE-693',
            'owasp': 'A6:2017-Security Misconfiguration'
        },
        'X-XSS-Protection': {
            'description': 'Enables browser XSS filter',
            'recommendation': "Set to '1; mode=block'",
            'severity': 'MEDIUM',
            'score': 10,
            'cwe': 'CWE-79',
            'owasp': 'A7:2017-Cross-Site Scripting (XSS)'
        },
        'Referrer-Policy': {
            'description': 'Controls referrer information',
            'recommendation': "Set to 'strict-origin-when-cross-origin'",
            'severity': 'MEDIUM',
            'score': 10,
            'cwe': 'CWE-200',
            'owasp': 'A3:2017-Sensitive Data Exposure'
        },
        'Permissions-Policy': {
            'description': 'Controls browser features',
            'recommendation': "Restrict features like camera, microphone, geolocation",
            'severity': 'MEDIUM',
            'score': 10,
            'cwe': 'CWE-693',
            'owasp': 'A6:2017-Security Misconfiguration'
        },
        'Cache-Control': {
            'description': 'Prevents sensitive data caching',
            'recommendation': "Set to 'no-store, no-cache, must-revalidate'",
            'severity': 'MEDIUM',
            'score': 8,
            'cwe': 'CWE-525',
            'owasp': 'A3:2017-Sensitive Data Exposure'
        },
        'Clear-Site-Data': {
            'description': 'Clears browser data on logout',
            'recommendation': "Implement on logout endpoints",
            'severity': 'LOW',
            'score': 5,
            'cwe': 'CWE-613',
            'owasp': 'A3:2017-Sensitive Data Exposure'
        },
        'Cross-Origin-Embedder-Policy': {
            'description': 'Controls cross-origin resource loading',
            'recommendation': "Set to 'require-corp'",
            'severity': 'LOW',
            'score': 5,
            'cwe': 'CWE-693',
            'owasp': 'A6:2017-Security Misconfiguration'
        },
        'Cross-Origin-Opener-Policy': {
            'description': 'Isolates browsing contexts',
            'recommendation': "Set to 'same-origin'",
            'severity': 'LOW',
            'score': 5,
            'cwe': 'CWE-693',
            'owasp': 'A6:2017-Security Misconfiguration'
        },
        'Cross-Origin-Resource-Policy': {
            'description': 'Controls cross-origin resource access',
            'recommendation': "Set to 'same-origin'",
            'severity': 'LOW',
            'score': 5,
            'cwe': 'CWE-693',
            'owasp': 'A6:2017-Security Misconfiguration'
        }
    }
    
    # Additional headers to check (non-security but informative)
    INFO_HEADERS = [
        'Server',
        'X-Powered-By',
        'Via',
        'X-AspNet-Version',
        'X-AspNetMvc-Version',
        'X-Generator',
        'X-Drupal-Cache',
        'X-Drupal-Dynamic-Cache',
        'X-Varnish',
        'X-Cache',
        'X-Cache-Hits',
        'X-Backend-Server',
        'X-Proxy-Cache'
    ]
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.response = None
        self.headers = {}
        self.security_score = 0
        self.max_score = 0
        self.results = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.compliance_standards = {
            'OWASP': 0,
            'NIST': 0,
            'PCI_DSS': 0
        }
        
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
        
    def fetch_headers(self, url):
        """Fetch HTTP headers from target URL"""
        try:
            print(f"{Fore.CYAN}[*] Sending request to {url}{Style.RESET_ALL}")
            
            # Try HTTPS first, then fallback to HTTP
            try:
                response = requests.get(
                    url.replace('http://', 'https://'),
                    timeout=15,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    allow_redirects=True
                )
                self.url = url.replace('http://', 'https://')
            except:
                response = requests.get(
                    url,
                    timeout=15,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    allow_redirects=True
                )
                
            self.response = response
            self.headers = response.headers
            
            return True
            
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[✗] Connection timeout{Style.RESET_ALL}")
            return False
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}[✗] Connection error - host unreachable{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to fetch headers: {e}{Style.RESET_ALL}")
            return False
            
    def analyze_security_headers(self):
        """Analyze security headers and calculate score"""
        self.results = []
        self.security_score = 0
        self.max_score = sum(header['score'] for header in self.SECURITY_HEADERS.values())
        
        for header, info in self.SECURITY_HEADERS.items():
            value = self.headers.get(header)
            
            result = {
                'header': header,
                'present': value is not None,
                'value': value,
                'description': info['description'],
                'recommendation': info['recommendation'],
                'severity': info['severity'],
                'score': info['score'] if value is not None else 0,
                'cwe': info['cwe'],
                'owasp': info['owasp']
            }
            
            if value is not None:
                self.security_score += info['score']
                
                # Additional checks for specific headers
                if header == 'Strict-Transport-Security':
                    if 'max-age=31536000' not in value and 'max-age=31536000' not in value:
                        result['warning'] = 'HSTS max-age should be at least 31536000 seconds (1 year)'
                    if 'includeSubDomains' not in value:
                        result['warning'] = 'HSTS should include includeSubDomains directive'
                        
                elif header == 'X-Frame-Options':
                    if value not in ['DENY', 'SAMEORIGIN']:
                        result['warning'] = 'X-Frame-Options should be DENY or SAMEORIGIN'
                        
                elif header == 'X-Content-Type-Options':
                    if value != 'nosniff':
                        result['warning'] = 'X-Content-Type-Options should be set to nosniff'
                        
            self.results.append(result)
            
        return self.results
        
    def analyze_info_headers(self):
        """Analyze informational headers for fingerprinting risks"""
        info_results = []
        
        for header in self.INFO_HEADERS:
            value = self.headers.get(header)
            if value:
                info_results.append({
                    'header': header,
                    'value': value,
                    'risk': self.assess_info_header_risk(header, value)
                })
                
        return info_results
        
    def assess_info_header_risk(self, header, value):
        """Assess risk level of information disclosure headers"""
        risk_level = 'LOW'
        
        if header in ['Server', 'X-Powered-By']:
            risk_level = 'MEDIUM'
            
        if 'ASP.NET' in value or 'PHP' in value or 'Apache' in value or 'nginx' in value:
            risk_level = 'MEDIUM'
            
        if 'version' in value.lower() or 'ver.' in value.lower():
            risk_level = 'HIGH'
            
        return risk_level
        
    def calculate_compliance(self):
        """Calculate compliance with security standards"""
        total_headers = len(self.SECURITY_HEADERS)
        present_headers = sum(1 for r in self.results if r['present'])
        compliance_percentage = (present_headers / total_headers) * 100
        
        self.compliance_standards = {
            'OWASP': min(100, (self.security_score / 50) * 100),  # OWASP Top 10 compliance
            'NIST': min(100, (self.security_score / 60) * 100),   # NIST guidelines
            'PCI_DSS': min(100, (present_headers / 8) * 100)      # PCI DSS v4.0 requirements
        }
        
        return self.compliance_standards
        
    def generate_report(self):
        """Generate comprehensive security header report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] SECURITY HEADER AUDIT REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Status Code: {Fore.LIGHTGREEN_EX}{self.response.status_code if self.response else 'N/A'}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Server: {Fore.LIGHTGREEN_EX}{self.headers.get('Server', 'Unknown')}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SECURITY SCORE ============
        print(f"\n{Fore.CYAN}[ SECURITY HEADER SCORE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        percentage = (self.security_score / self.max_score) * 100 if self.max_score > 0 else 0
        
        # Visual score bar
        bar_length = 40
        filled_length = int(bar_length * percentage / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if percentage >= 80:
            score_color = Fore.GREEN
            rating = 'A - EXCELLENT'
        elif percentage >= 60:
            score_color = Fore.GREEN
            rating = 'B - GOOD'
        elif percentage >= 40:
            score_color = Fore.YELLOW
            rating = 'C - FAIR'
        elif percentage >= 20:
            score_color = Fore.RED
            rating = 'D - POOR'
        else:
            score_color = Fore.RED
            rating = 'F - CRITICAL'
            
        print(f"\n  Overall Score: {score_color}{self.security_score}/{self.max_score} ({percentage:.1f}%){Style.RESET_ALL}")
        print(f"  Security Grade: {score_color}{rating}{Style.RESET_ALL}")
        print(f"  {score_color}[{bar}] {percentage:.1f}%{Style.RESET_ALL}")
        
        # ============ SECURITY HEADERS ANALYSIS ============
        print(f"\n{Fore.CYAN}[ SECURITY HEADERS ANALYSIS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
        
        # Sort results: missing critical first, then present
        sorted_results = sorted(
            self.results,
            key=lambda x: (x['present'], 
                         0 if x['severity'] == 'CRITICAL' else 
                         1 if x['severity'] == 'HIGH' else 
                         2 if x['severity'] == 'MEDIUM' else 3)
        )
        
        for result in sorted_results:
            header = result['header']
            present = result['present']
            severity = result['severity']
            
            if present:
                status = f"{Fore.GREEN}[✓] PRESENT{Style.RESET_ALL}"
                value_display = f"{Fore.WHITE}{result['value'][:80]}{'...' if len(result['value']) > 80 else ''}{Style.RESET_ALL}"
            else:
                status = f"{Fore.RED}[✗] MISSING{Style.RESET_ALL}"
                value_display = ""
                
            # Severity color
            if severity == 'CRITICAL':
                sev_color = Fore.RED + Style.BRIGHT
            elif severity == 'HIGH':
                sev_color = Fore.RED
            elif severity == 'MEDIUM':
                sev_color = Fore.YELLOW
            else:
                sev_color = Fore.GREEN
                
            print(f"\n  {sev_color}{header}{Style.RESET_ALL}")
            print(f"  ├─ Status: {status}")
            if value_display:
                print(f"  ├─ Value: {value_display}")
            print(f"  ├─ Severity: {sev_color}{severity}{Style.RESET_ALL}")
            print(f"  ├─ CWE: {Fore.WHITE}{result['cwe']}{Style.RESET_ALL}")
            print(f"  ├─ OWASP: {Fore.WHITE}{result['owasp']}{Style.RESET_ALL}")
            print(f"  ├─ Description: {Fore.WHITE}{result['description']}{Style.RESET_ALL}")
            
            if not present:
                print(f"  └─ Recommendation: {Fore.YELLOW}{result['recommendation']}{Style.RESET_ALL}")
            elif 'warning' in result:
                print(f"  └─ {Fore.YELLOW}⚠ Warning: {result['warning']}{Style.RESET_ALL}")
                
        # ============ INFORMATION DISCLOSURE ============
        info_results = self.analyze_info_headers()
        
        if info_results:
            print(f"\n{Fore.CYAN}[ INFORMATION DISCLOSURE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] These headers reveal server/framework information{Style.RESET_ALL}\n")
            
            for info in info_results:
                risk = info['risk']
                if risk == 'HIGH':
                    risk_color = Fore.RED
                elif risk == 'MEDIUM':
                    risk_color = Fore.YELLOW
                else:
                    risk_color = Fore.GREEN
                    
                print(f"  {risk_color}[{risk} RISK]{Style.RESET_ALL} {info['header']}: {Fore.WHITE}{info['value']}{Style.RESET_ALL}")
                
        # ============ COMPLIANCE STANDARDS ============
        self.calculate_compliance()
        
        print(f"\n{Fore.CYAN}[ COMPLIANCE STANDARDS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        for standard, score in self.compliance_standards.items():
            if score >= 80:
                std_color = Fore.GREEN
            elif score >= 60:
                std_color = Fore.YELLOW
            else:
                std_color = Fore.RED
                
            print(f"  {Fore.WHITE}{standard}:{Style.RESET_ALL} {std_color}{score:.1f}% compliant{Style.RESET_ALL}")
            
        # ============ EXECUTIVE SUMMARY ============
        print(f"\n{Fore.CYAN}[ EXECUTIVE SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        critical_missing = sum(1 for r in self.results if not r['present'] and r['severity'] == 'CRITICAL')
        high_missing = sum(1 for r in self.results if not r['present'] and r['severity'] == 'HIGH')
        medium_missing = sum(1 for r in self.results if not r['present'] and r['severity'] == 'MEDIUM')
        
        print(f"\n  {Fore.WHITE}Missing Critical Headers:{Style.RESET_ALL} {Fore.RED}{critical_missing}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Missing High Severity Headers:{Style.RESET_ALL} {Fore.RED}{high_missing}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Missing Medium Severity Headers:{Style.RESET_ALL} {Fore.YELLOW}{medium_missing}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Total Security Score:{Style.RESET_ALL} {score_color}{self.security_score}/{self.max_score}{Style.RESET_ALL}")
        
        # ============ TOP RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ TOP PRIORITY RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        recommendations = []
        for result in self.results:
            if not result['present'] and result['severity'] in ['CRITICAL', 'HIGH']:
                recommendations.append(f"Add {result['header']}: {result['recommendation']}")
                
        if recommendations:
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {Fore.RED}{i}.{Style.RESET_ALL} {rec}")
        else:
            print(f"  {Fore.GREEN}[✓] No critical recommendations - excellent security posture!{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"header_audit_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'status_code': self.response.status_code if self.response else None,
            'security_score': self.security_score,
            'max_score': self.max_score,
            'percentage': (self.security_score / self.max_score) * 100 if self.max_score > 0 else 0,
            'headers': dict(self.headers),
            'security_headers_analysis': self.results,
            'info_disclosure': self.analyze_info_headers(),
            'compliance': self.compliance_standards
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive header analysis mode"""
        print(f"{Fore.GREEN}[*] HTTP Security Header Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Comprehensive security headers audit & compliance checking{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter target URL (e.g., https://example.com): {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Starting security header analysis on {self.url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Fetching HTTP headers...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Fetch headers
        if not self.fetch_headers(self.url):
            return
            
        # Analyze security headers
        print(f"{Fore.CYAN}[*] Analyzing {len(self.SECURITY_HEADERS)} security headers...{Style.RESET_ALL}")
        time.sleep(0.5)  # Small delay for effect
        self.analyze_security_headers()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Security header analysis completed{Style.RESET_ALL}")


def analyze_headers(url=None):
    """Main entry point for CLI compatibility"""
    analyzer = HTTPSecurityHeaderAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if url:
        # Direct scan mode
        analyzer.normalize_url(url)
        analyzer.start_time = datetime.now()
        
        if analyzer.fetch_headers(analyzer.url):
            analyzer.analyze_security_headers()
            analyzer.end_time = datetime.now()
            analyzer.generate_report()
    else:
        # Interactive mode
        analyzer.interactive_scan()


if __name__ == "__main__":
    analyze_headers()
