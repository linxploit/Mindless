#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: XSS REFLECTION DETECTOR
Advanced Cross-Site Scripting Vulnerability Scanner (Read-Only)
Author: ICAT Project | Linxploit.xyz
"""

import requests
import re
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs, urlencode
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class XSSReflectionDetector:
    """Advanced XSS reflection detection with context analysis"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗  ██╗███████╗███████╗     ██████╗██████╗ ███████╗██╗     ███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗  ║
    ║  ╚██╗██╔╝██╔════╝██╔════╝    ██╔════╝██╔══██╗██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║  ║
    ║   ╚███╔╝ ███████╗███████╗    ██║     ██████╔╝█████╗  ██║     █████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║  ║
    ║   ██╔██╗ ╚════██║╚════██║    ██║     ██╔══██╗██╔══╝  ██║     ██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║  ║
    ║  ██╔╝ ██╗███████║███████║    ╚██████╗██║  ██║███████╗███████╗███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║  ║
    ║  ╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝  ║
    ║                    {Fore.CYAN}XSS REFLECTION DETECTOR v2.0{Fore.RED}                    ║
    ║                    {Fore.YELLOW}[ SAFE - READ ONLY MODE ]{Fore.RED}                      ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # XSS test payloads (non-executable markers)
    TEST_PAYLOADS = [
        # Basic reflection markers
        'XSS_TEST_MARKER_123',
        'XSS_REFLECTED_456',
        'XSS_PAYLOAD_789',
        'XXS_TEST_ABC',
        
        # HTML context markers
        '<div>XSS_TEST</div>',
        '<span>XSS_MARKER</span>',
        '<p>XSS_REFLECTED</p>',
        
        # Attribute context markers
        '"XSS_TEST"',
        "'XSS_TEST'",
        'javascript:alert(1)//',
        
        # Script context markers
        '"; XSS_TEST; "',
        "'; XSS_TEST; '",
        '// XSS_TEST //',
        
        # URL context markers
        'http://xss.test',
        'https://xss.test',
        '//xss.test',
        
        # Event handler markers
        'onload="XSS_TEST"',
        'onerror="XSS_TEST"',
        'onclick="XSS_TEST"',
    ]
    
    # Context signatures
    CONTEXT_SIGNATURES = {
        'html': ['<div>', '<span>', '<p>', '<a>', '<h1>', '<h2>', '<h3>', '<b>', '<i>', '<u>'],
        'attribute': ['"XSS_', "'XSS_", '=XSS_', 'javascript:'],
        'script': ['"; XSS_', "'; XSS_", '// XSS_', '/* XSS_'],
        'url': ['http://', 'https://', '//', 'ftp://'],
        'event': ['onload=', 'onerror=', 'onclick=', 'onmouseover=', 'onfocus='],
    }
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.params = {}
        self.results = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.reflection_points = []
        
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
        
        # Parse existing query parameters
        self.params = parse_qs(parsed.query)
        
        # Store base URL without query
        base_path = parsed.path if parsed.path else '/'
        self.base_url = f"{parsed.scheme}://{parsed.netloc}{base_path}"
        self.url = url
        
        return url
        
    def extract_parameters(self):
        """Extract parameters from URL and forms"""
        parameters = []
        
        # Add query parameters
        for param in self.params.keys():
            parameters.append({
                'name': param,
                'location': 'url_query',
                'current_value': self.params[param][0] if self.params[param] else ''
            })
            
        # Try to parse forms
        try:
            response = requests.get(self.url, timeout=10, verify=False)
            forms = re.findall(r'<form.*?</form>', response.text, re.DOTALL)
            
            for form in forms:
                # Extract form action
                action_match = re.search(r'action=[\'"](.*?)[\'"]', form)
                action = action_match.group(1) if action_match else ''
                
                # Extract input fields
                inputs = re.findall(r'<input.*?>', form)
                for inp in inputs:
                    name_match = re.search(r'name=[\'"](.*?)[\'"]', inp)
                    type_match = re.search(r'type=[\'"](.*?)[\'"]', inp)
                    
                    if name_match:
                        parameters.append({
                            'name': name_match.group(1),
                            'location': 'form',
                            'form_action': action,
                            'input_type': type_match.group(1) if type_match else 'text'
                        })
        except:
            pass
            
        return parameters
        
    def test_parameter(self, param_name, payload, location='url_query'):
        """Test single parameter for XSS reflection"""
        test_params = self.params.copy()
        test_params[param_name] = payload
        
        # Build test URL
        test_url = f"{self.base_url}?{urlencode(test_params, doseq=True)}"
        
        try:
            response = requests.get(
                test_url,
                timeout=10,
                verify=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            # Check if payload is reflected
            if payload in response.text:
                reflection = {
                    'parameter': param_name,
                    'payload': payload,
                    'url': test_url,
                    'status_code': response.status_code,
                    'reflection_context': self.detect_context(response.text, payload),
                    'reflection_count': response.text.count(payload),
                    'response_preview': self.get_context_preview(response.text, payload)
                }
                
                return reflection
                
        except Exception as e:
            return None
            
        return None
        
    def detect_context(self, html, payload):
        """Detect the context where payload is reflected"""
        contexts = []
        
        # Find payload position
        pos = html.find(payload)
        if pos == -1:
            return ['unknown']
            
        # Check surrounding context (200 chars before and after)
        start = max(0, pos - 100)
        end = min(len(html), pos + len(payload) + 100)
        context = html[start:end]
        
        for ctx, signatures in self.CONTEXT_SIGNATURES.items():
            for sig in signatures:
                if sig in context:
                    contexts.append(ctx)
                    break
                    
        return contexts if contexts else ['unknown']
        
    def get_context_preview(self, html, payload):
        """Get preview of reflection context"""
        pos = html.find(payload)
        if pos == -1:
            return ''
            
        start = max(0, pos - 50)
        end = min(len(html), pos + len(payload) + 50)
        
        preview = html[start:end]
        # Highlight the payload
        preview = preview.replace(payload, f"{Fore.RED}{payload}{Fore.WHITE}")
        
        return preview
        
    def scan_reflections(self):
        """Scan for XSS reflection points"""
        self.results = []
        parameters = self.extract_parameters()
        
        if not parameters:
            print(f"{Fore.YELLOW}[!] No parameters found to test{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}[*] Found {len(parameters)} potential injection points{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Testing {len(self.TEST_PAYLOADS)} XSS markers per parameter{Style.RESET_ALL}\n")
        
        total_tests = len(parameters) * len(self.TEST_PAYLOADS)
        completed = 0
        
        for param in parameters:
            param_name = param['name']
            location = param.get('location', 'url_query')
            
            print(f"{Fore.CYAN}[>] Testing parameter: {param_name} ({location}){Style.RESET_ALL}")
            
            for payload in self.TEST_PAYLOADS:
                result = self.test_parameter(param_name, payload, location)
                
                if result:
                    self.results.append(result)
                    
                # Update progress
                completed += 1
                if completed % 10 == 0:
                    progress = (completed / total_tests) * 100
                    print(f"\r{Fore.CYAN}  Progress: {completed}/{total_tests} ({progress:.1f}%) | Reflections: {len(self.results)}{Style.RESET_ALL}", end="")
                    
            print()  # New line after parameter
            
        print()  # New line after all tests
        
    def analyze_risk_level(self, contexts):
        """Analyze risk level based on reflection context"""
        if 'script' in contexts:
            return 'CRITICAL', 'Reflected in script context - likely executable'
        elif 'event' in contexts:
            return 'HIGH', 'Reflected in event handler - potentially executable'
        elif 'attribute' in contexts:
            return 'HIGH', 'Reflected in HTML attribute - may be executable'
        elif 'html' in contexts:
            return 'MEDIUM', 'Reflected in HTML body - may require breaking context'
        elif 'url' in contexts:
            return 'MEDIUM', 'Reflected in URL - potential open redirect'
        else:
            return 'LOW', 'Reflected but context unclear'
            
    def generate_report(self):
        """Generate comprehensive XSS reflection report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] XSS REFLECTION ANALYSIS REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ REFLECTION SUMMARY ============
        print(f"\n{Fore.CYAN}[ REFLECTION SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.results:
            # Group by parameter
            param_reflections = {}
            for result in self.results:
                param = result['parameter']
                if param not in param_reflections:
                    param_reflections[param] = []
                param_reflections[param].append(result)
                
            print(f"\n  {Fore.RED}[!] XSS REFLECTIONS DETECTED{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Total reflection points: {len(self.results)}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Affected parameters: {len(param_reflections)}{Style.RESET_ALL}\n")
            
            for param, reflections in param_reflections.items():
                print(f"  {Fore.YELLOW}→ Parameter: {param}{Style.RESET_ALL}")
                
                # Get unique contexts for this parameter
                all_contexts = []
                for r in reflections:
                    all_contexts.extend(r['reflection_context'])
                unique_contexts = list(set(all_contexts))
                
                risk_level, risk_desc = self.analyze_risk_level(unique_contexts)
                
                if risk_level == 'CRITICAL':
                    risk_color = Fore.RED + Style.BRIGHT
                elif risk_level == 'HIGH':
                    risk_color = Fore.RED
                elif risk_level == 'MEDIUM':
                    risk_color = Fore.YELLOW
                else:
                    risk_color = Fore.GREEN
                    
                print(f"     ├─ Reflections: {len(reflections)}")
                print(f"     ├─ Contexts: {', '.join(unique_contexts)}")
                print(f"     ├─ Risk Level: {risk_color}{risk_level}{Style.RESET_ALL}")
                print(f"     └─ Analysis: {Fore.WHITE}{risk_desc}{Style.RESET_ALL}")
                
                # Show example
                example = reflections[0]
                print(f"\n        Example:")
                print(f"        URL: {example['url'][:80]}...")
                print(f"        Payload: {Fore.CYAN}{example['payload']}{Style.RESET_ALL}")
                print(f"        Context Preview: {example['response_preview'][:100]}...")
                print()
        else:
            print(f"\n  {Fore.GREEN}[✓] No XSS reflections detected{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}The application appears to properly handle input{Style.RESET_ALL}")
            
        # ============ DETAILED FINDINGS ============
        if self.results:
            print(f"\n{Fore.CYAN}[ DETAILED FINDINGS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for i, result in enumerate(self.results[:10], 1):  # Show first 10
                print(f"\n  {Fore.WHITE}{i}. Reflection Point{Style.RESET_ALL}")
                print(f"     ├─ Parameter: {Fore.YELLOW}{result['parameter']}{Style.RESET_ALL}")
                print(f"     ├─ Payload: {Fore.CYAN}{result['payload']}{Style.RESET_ALL}")
                print(f"     ├─ Status Code: {result['status_code']}")
                print(f"     ├─ Context: {', '.join(result['reflection_context'])}")
                print(f"     └─ Count: {result['reflection_count']} occurrences")
                
            if len(self.results) > 10:
                print(f"\n  {Fore.YELLOW}... and {len(self.results) - 10} more reflections{Style.RESET_ALL}")
                
        # ============ SECURITY IMPLICATIONS ============
        if self.results:
            print(f"\n{Fore.CYAN}[ SECURITY IMPLICATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Check for critical reflections
            critical_params = []
            for param, reflections in param_reflections.items():
                all_contexts = []
                for r in reflections:
                    all_contexts.extend(r['reflection_context'])
                
                if 'script' in all_contexts or 'event' in all_contexts:
                    critical_params.append(param)
                    
            if critical_params:
                print(f"\n  {Fore.RED}[!] CRITICAL: Reflections in executable contexts{Style.RESET_ALL}")
                print(f"     Parameters: {', '.join(critical_params)}")
                print(f"     These reflections MAY be exploitable for XSS attacks")
                print(f"     Further manual testing is required to confirm exploitability")
                
            print(f"""
  {Fore.YELLOW}Note on XSS Testing:{Style.RESET_ALL}
  This tool performs SAFE, READ-ONLY testing using non-executable markers.
  Reflection does NOT equal vulnerability - it only indicates input is echoed back.
  
  To confirm XSS vulnerabilities, manual testing is required with:
  • Context-specific payloads
  • WAF/bypass techniques
  • Different browsers and versions
            """)
            
        # ============ REMEDIATION GUIDANCE ============
        if self.results:
            print(f"\n{Fore.CYAN}[ REMEDIATION GUIDANCE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"""
  {Fore.WHITE}1.{Style.RESET_ALL} Implement Context-Aware Output Encoding
     - HTML encode: & < > " ' /
     - JavaScript encode: \n \r ' " \
     - CSS encode: IE's expression() etc.
     - URL encode: %xx
  
  {Fore.WHITE}2.{Style.RESET_ALL} Use Content Security Policy (CSP)
     Content-Security-Policy: script-src 'self'
  
  {Fore.WHITE}3.{Style.RESET_ALL} Apply Input Validation
     - Whitelist allowed characters
     - Validate data type, length, format
  
  {Fore.WHITE}4.{Style.RESET_ALL} Set X-XSS-Protection header
     X-XSS-Protection: 1; mode=block
  
  {Fore.WHITE}5.{Style.RESET_ALL} Use modern frameworks with auto-escaping
     - React, Angular, Vue.js (with proper configuration)
            """)
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"xss_scan_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'reflections_detected': len(self.results) > 0,
            'total_reflections': len(self.results),
            'reflection_points': self.results,
            'parameters_tested': self.extract_parameters()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive XSS reflection scanning mode"""
        print(f"{Fore.GREEN}[*] XSS Reflection Detector initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] SAFE MODE - Using non-executable markers only{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter target URL (e.g., https://example.com/page.php?id=1): {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Starting XSS reflection scan on {self.url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Testing for input reflection patterns...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Perform scan
        self.scan_reflections()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.results:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] XSS reflection analysis completed{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Remember: Reflection ≠ Vulnerability - Manual testing required{Style.RESET_ALL}")


def xss_reflection_test(url=None):
    """Main entry point for CLI compatibility"""
    detector = XSSReflectionDetector()
    
    # Display banner
    detector.print_header()
    
    if url:
        # Direct scan mode
        detector.normalize_url(url)
        detector.start_time = datetime.now()
        detector.scan_reflections()
        detector.end_time = datetime.now()
        detector.generate_report()
    else:
        # Interactive mode
        detector.interactive_scan()


if __name__ == "__main__":
    xss_reflection_test()
