#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: CORS MISCONFIGURATION CHECKER
Advanced Cross-Origin Resource Sharing Security Auditor
Author: ICAT Project | Linxploit.xyz
"""

import requests
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class CORSChecker:
    """Advanced CORS misconfiguration detection and analysis"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██████╗ ██████╗ ███████╗    ███████╗██╗  ██╗███████╗ ██████╗██╗  ║
    ║  ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║  ║
    ║  ██║     ██║   ██║██████╔╝███████╗    ███████╗███████║█████╗  ██║     ██║  ║
    ║  ██║     ██║   ██║██╔══██╗╚════██║    ╚════██║██╔══██║██╔══╝  ██║     ██║  ║
    ║  ╚██████╗╚██████╔╝██║  ██║███████║    ███████║██║  ██║███████╗╚██████╗███████╗
    ║   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝
    ║                    {Fore.CYAN}CORS MISCONFIGURATION CHECKER v2.0{Fore.RED}            ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Test origins for CORS analysis
    TEST_ORIGINS = [
        'https://evil.com',
        'https://evil.com:8080',
        'null',
        'https://sub.evil.com',
        'https://evil.com.evil.com',
        'https://evil.com:443',
        'https://127.0.0.1',
        'https://localhost',
        'file://',
        'http://evil.com',
        'https://evil.com.evil.com.evil.com',
        'https://attackersite.com',
        'https://sub.attackersite.com',
        'https://evil.com/evil',
        'https://evil.com/?evil',
        'https://evil.com#evil',
    ]
    
    # Dangerous CORS configurations
    DANGEROUS_PATTERNS = [
        ('Access-Control-Allow-Origin: *', 'Wildcard origin - allows any domain'),
        ('Access-Control-Allow-Credentials: true + *', 'Credentials with wildcard - CRITICAL'),
        ('Origin reflected', 'Origin reflection vulnerability'),
        ('Null origin allowed', 'null origin accepted - often exploitable'),
        ('No Vary: Origin', 'Missing Vary header - caching issues'),
    ]
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.results = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.preflight_results = {}
        self.vulnerabilities = []
        
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
        
    def check_cors(self, url, origin):
        """Check CORS headers for a specific origin"""
        headers = {
            'Origin': origin,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # Simple request
            response = requests.options(
                url,
                headers=headers,
                timeout=10,
                verify=False
            )
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Max-Age': response.headers.get('Access-Control-Max-Age'),
                'Access-Control-Expose-Headers': response.headers.get('Access-Control-Expose-Headers'),
                'Vary': response.headers.get('Vary'),
            }
            
            # Also try GET request
            response_get = requests.get(
                url,
                headers=headers,
                timeout=10,
                verify=False
            )
            
            cors_headers_get = {
                'Access-Control-Allow-Origin': response_get.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Credentials': response_get.headers.get('Access-Control-Allow-Credentials'),
            }
            
            # Merge results (GET headers take precedence for simple requests)
            if cors_headers_get['Access-Control-Allow-Origin']:
                cors_headers['Access-Control-Allow-Origin'] = cors_headers_get['Access-Control-Allow-Origin']
            if cors_headers_get['Access-Control-Allow-Credentials']:
                cors_headers['Access-Control-Allow-Credentials'] = cors_headers_get['Access-Control-Allow-Credentials']
                
            return {
                'origin': origin,
                'headers': cors_headers,
                'status_code': response.status_code
            }
            
        except Exception as e:
            return {
                'origin': origin,
                'error': str(e),
                'headers': {}
            }
            
    def analyze_cors_configuration(self):
        """Analyze CORS configuration for vulnerabilities"""
        self.results = []
        self.vulnerabilities = []
        
        print(f"{Fore.CYAN}[*] Testing {len(self.TEST_ORIGINS)} different origins...{Style.RESET_ALL}")
        
        for origin in self.TEST_ORIGINS:
            result = self.check_cors(self.url, origin)
            self.results.append(result)
            
        # Check for baseline (no origin)
        baseline = self.check_cors(self.url, '')
        self.baseline = baseline
        
        return self.results
        
    def detect_vulnerabilities(self):
        """Detect CORS misconfigurations"""
        vulnerabilities = []
        
        # Check if CORS is even configured
        cors_enabled = any(r['headers'].get('Access-Control-Allow-Origin') for r in self.results)
        
        if not cors_enabled:
            vulnerabilities.append({
                'type': 'INFO',
                'severity': 'LOW',
                'description': 'CORS headers not detected',
                'recommendation': 'No action needed if API is same-origin only',
                'cwe': 'CWE-942'
            })
            return vulnerabilities
            
        # Check for wildcard origin
        for result in self.results:
            headers = result['headers']
            allow_origin = headers.get('Access-Control-Allow-Origin')
            allow_creds = headers.get('Access-Control-Allow-Credentials')
            
            if allow_origin == '*':
                vuln = {
                    'type': 'WILDCARD_ORIGIN',
                    'severity': 'MEDIUM',
                    'description': 'Access-Control-Allow-Origin: * - Allows any domain',
                    'evidence': f"Origin '{result['origin']}' returned '*'",
                    'recommendation': 'Restrict to specific trusted domains',
                    'cwe': 'CWE-942'
                }
                
                if allow_creds and allow_creds.lower() == 'true':
                    vuln['severity'] = 'CRITICAL'
                    vuln['description'] = 'CRITICAL: Wildcard origin with credentials - Allows any domain to send authenticated requests'
                    vuln['recommendation'] = 'Remove wildcard origin when using credentials'
                    
                vulnerabilities.append(vuln)
                break
                
        # Check for origin reflection
        for result in self.results:
            headers = result['headers']
            allow_origin = headers.get('Access-Control-Allow-Origin')
            
            if allow_origin and allow_origin == result['origin']:
                vulnerabilities.append({
                    'type': 'ORIGIN_REFLECTION',
                    'severity': 'CRITICAL',
                    'description': 'Origin reflection - Server echoes back the Origin header',
                    'evidence': f"Origin '{result['origin']}' reflected in Access-Control-Allow-Origin",
                    'recommendation': 'Implement proper origin whitelisting, not reflection',
                    'cwe': 'CWE-942'
                })
                break
                
        # Check for null origin
        for result in self.results:
            headers = result['headers']
            allow_origin = headers.get('Access-Control-Allow-Origin')
            
            if allow_origin and 'null' in allow_origin.lower():
                vulnerabilities.append({
                    'type': 'NULL_ORIGIN',
                    'severity': 'HIGH',
                    'description': 'Null origin accepted - Can be spoofed from sandboxed iframes',
                    'evidence': f"Access-Control-Allow-Origin: {allow_origin}",
                    'recommendation': 'Do not accept null origin',
                    'cwe': 'CWE-942'
                })
                break
                
        # Check for missing Vary header
        for result in self.results:
            headers = result['headers']
            vary = headers.get('Vary', '')
            
            if 'origin' not in vary.lower():
                vulnerabilities.append({
                    'type': 'MISSING_VARY',
                    'severity': 'MEDIUM',
                    'description': 'Missing Vary: Origin header - Caching issues possible',
                    'evidence': f"Vary: {vary}",
                    'recommendation': 'Add "Vary: Origin" header',
                    'cwe': 'CWE-942'
                })
                break
                
        # Check for overly permissive methods
        for result in self.results:
            headers = result['headers']
            methods = headers.get('Access-Control-Allow-Methods', '')
            
            dangerous_methods = ['PUT', 'DELETE', 'PATCH', 'TRACE', 'CONNECT']
            allowed_dangerous = [m for m in dangerous_methods if m in methods.upper()]
            
            if allowed_dangerous:
                vulnerabilities.append({
                    'type': 'DANGEROUS_METHODS',
                    'severity': 'HIGH',
                    'description': f"Dangerous HTTP methods allowed: {', '.join(allowed_dangerous)}",
                    'evidence': f"Access-Control-Allow-Methods: {methods}",
                    'recommendation': 'Restrict methods to only necessary ones',
                    'cwe': 'CWE-942'
                })
                
        return vulnerabilities
        
    def generate_report(self):
        """Generate comprehensive CORS report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] CORS SECURITY AUDIT REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ CORS CONFIGURATION SUMMARY ============
        print(f"\n{Fore.CYAN}[ CORS CONFIGURATION SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Check if CORS is enabled
        cors_enabled = any(r['headers'].get('Access-Control-Allow-Origin') for r in self.results)
        
        if cors_enabled:
            print(f"\n  {Fore.YELLOW}[!] CORS is ENABLED on this endpoint{Style.RESET_ALL}")
            
            # Get baseline configuration
            for result in self.results:
                if result['origin'] == '' and result['headers'].get('Access-Control-Allow-Origin'):
                    print(f"  {Fore.WHITE}Default Access-Control-Allow-Origin: {Fore.LIGHTGREEN_EX}{result['headers']['Access-Control-Allow-Origin']}{Style.RESET_ALL}")
                    break
        else:
            print(f"\n  {Fore.GREEN}[✓] CORS headers not detected - no misconfiguration risk{Style.RESET_ALL}")
            
        # ============ VULNERABILITIES ============
        vulnerabilities = self.detect_vulnerabilities()
        
        if vulnerabilities:
            print(f"\n{Fore.CYAN}[ VULNERABILITIES DETECTED ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Sort by severity
            severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
            sorted_vulns = sorted(vulnerabilities, key=lambda x: severity_order.get(x['severity'], 5))
            
            for vuln in sorted_vulns:
                severity = vuln['severity']
                if severity == 'CRITICAL':
                    sev_color = Fore.RED + Style.BRIGHT
                elif severity == 'HIGH':
                    sev_color = Fore.RED
                elif severity == 'MEDIUM':
                    sev_color = Fore.YELLOW
                elif severity == 'LOW':
                    sev_color = Fore.GREEN
                else:
                    sev_color = Fore.CYAN
                    
                print(f"\n  {sev_color}[{severity}]{Style.RESET_ALL} {vuln['type']}")
                print(f"  ├─ Description: {Fore.WHITE}{vuln['description']}{Style.RESET_ALL}")
                print(f"  ├─ CWE: {Fore.WHITE}{vuln.get('cwe', 'CWE-942')}{Style.RESET_ALL}")
                
                if 'evidence' in vuln:
                    print(f"  ├─ Evidence: {Fore.YELLOW}{vuln['evidence']}{Style.RESET_ALL}")
                    
                print(f"  └─ Recommendation: {Fore.GREEN}{vuln['recommendation']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}[ VULNERABILITIES DETECTED ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.GREEN}[✓] No CORS vulnerabilities detected{Style.RESET_ALL}")
            
        # ============ DETAILED ORIGIN TEST RESULTS ============
        print(f"\n{Fore.CYAN}[ ORIGIN TEST RESULTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        for result in self.results[:10]:  # Show first 10 results
            if result['origin']:
                origin_display = result['origin'][:40] + '...' if len(result['origin']) > 40 else result['origin']
            else:
                origin_display = 'No origin (baseline)'
                
            headers = result['headers']
            allow_origin = headers.get('Access-Control-Allow-Origin', 'Not set')
            allow_creds = headers.get('Access-Control-Allow-Credentials', 'Not set')
            
            if allow_origin != 'Not set':
                if allow_origin == '*':
                    status_color = Fore.RED
                elif allow_origin == result['origin']:
                    status_color = Fore.RED
                elif 'evil' in allow_origin:
                    status_color = Fore.RED
                else:
                    status_color = Fore.GREEN
            else:
                status_color = Fore.WHITE
                
            print(f"\n  {Fore.WHITE}Origin: {origin_display}{Style.RESET_ALL}")
            print(f"  ├─ Access-Control-Allow-Origin: {status_color}{allow_origin}{Style.RESET_ALL}")
            print(f"  └─ Access-Control-Allow-Credentials: {Fore.WHITE}{allow_creds}{Style.RESET_ALL}")
            
        if len(self.results) > 10:
            print(f"\n  {Fore.YELLOW}... and {len(self.results) - 10} more origins tested{Style.RESET_ALL}")
            
        # ============ ATTACK SCENARIOS ============
        critical_vulns = [v for v in vulnerabilities if v['severity'] in ['CRITICAL', 'HIGH']]
        
        if critical_vulns:
            print(f"\n{Fore.CYAN}[ POSSIBLE ATTACK SCENARIOS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for vuln in critical_vulns:
                if vuln['type'] == 'ORIGIN_REFLECTION':
                    print(f"\n  {Fore.RED}→ Origin Reflection Attack:{Style.RESET_ALL}")
                    print(f"    1. Attacker tricks user to visit evil.com")
                    print(f"    2. evil.com sends AJAX request with Origin: https://evil.com")
                    print(f"    3. Server reflects origin in ACAO header")
                    print(f"    4. Browser allows cross-origin read of sensitive data")
                    print(f"    5. Attractor exfiltrates user data")
                    
                elif vuln['type'] == 'WILDCARD_ORIGIN' and 'credentials' in vuln['description'].lower():
                    print(f"\n  {Fore.RED}→ Wildcard + Credentials Attack:{Style.RESET_ALL}")
                    print(f"    1. CRITICAL: Access-Control-Allow-Origin: *")
                    print(f"    2. CRITICAL: Access-Control-Allow-Credentials: true")
                    print(f"    3. This combination SHOULD NOT WORK per spec")
                    print(f"    4. If it does, ANY website can make authenticated requests")
                    print(f"    5. Immediate remediation required")
                    
                elif vuln['type'] == 'NULL_ORIGIN':
                    print(f"\n  {Fore.RED}→ Null Origin Attack:{Style.RESET_ALL}")
                    print(f"    1. Attacker creates sandboxed iframe with sandbox='allow-scripts'")
                    print(f"    2. iframe sends request with Origin: null")
                    print(f"    3. Server accepts null origin in ACAO header")
                    print(f"    4. Attractor bypasses CORS restrictions")
                    
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ SECURE CORS CONFIGURATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"""
  {Fore.WHITE}1.{Style.RESET_ALL} Implement strict origin whitelist:
     Access-Control-Allow-Origin: https://trusted-domain.com
     
  {Fore.WHITE}2.{Style.RESET_ALL} Never use wildcard (*) with credentials:
     Access-Control-Allow-Credentials: true
     Access-Control-Allow-Origin: https://trusted-domain.com
     
  {Fore.WHITE}3.{Style.RESET_ALL} Add Vary: Origin header:
     Vary: Origin
     
  {Fore.WHITE}4.{Style.RESET_ALL} Restrict HTTP methods:
     Access-Control-Allow-Methods: GET, POST
     
  {Fore.WHITE}5.{Style.RESET_ALL} Limit preflight cache duration:
     Access-Control-Max-Age: 600 (10 minutes)
        """)
        
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"cors_audit_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'cors_enabled': any(r['headers'].get('Access-Control-Allow-Origin') for r in self.results),
            'vulnerabilities': self.detect_vulnerabilities(),
            'origin_tests': [
                {
                    'origin': r['origin'],
                    'headers': r['headers']
                } for r in self.results
            ]
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive CORS analysis mode"""
        print(f"{Fore.GREEN}[*] CORS Misconfiguration Checker initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced Cross-Origin Resource Sharing security auditor{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter target URL (e.g., https://api.example.com): {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Starting CORS security audit on {self.url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Testing {len(self.TEST_ORIGINS)} different origins...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Perform CORS analysis
        self.analyze_cors_configuration()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if any(r['headers'].get('Access-Control-Allow-Origin') for r in self.results):
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] CORS security audit completed{Style.RESET_ALL}")


def check_cors_misconfig(url=None):
    """Main entry point for CLI compatibility"""
    checker = CORSChecker()
    
    # Display banner
    checker.print_header()
    
    if url:
        # Direct scan mode
        checker.normalize_url(url)
        checker.start_time = datetime.now()
        checker.analyze_cors_configuration()
        checker.end_time = datetime.now()
        checker.generate_report()
    else:
        # Interactive mode
        checker.interactive_scan()


if __name__ == "__main__":
    check_cors_misconfig()
