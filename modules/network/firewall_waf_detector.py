#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: FIREWALL/WAF DETECTOR
Advanced Web Application Firewall & Network Protection Fingerprinting
Author: ICAT Project | Linxploit.xyz
"""

import requests
import socket
import re
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class FirewallWAFDetector:
    """Advanced WAF/Firewall detection and fingerprinting"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗██╗██████╗ ███████╗██╗    ██╗ █████╗ ██╗     ██╗     ║
    ║  ██╔════╝██║██╔══██╗██╔════╝██║    ██║██╔══██╗██║     ██║     ║
    ║  █████╗  ██║██████╔╝█████╗  ██║ █╗ ██║███████║██║     ██║     ║
    ║  ██╔══╝  ██║██╔══██╗██╔══╝  ██║███╗██║██╔══██║██║     ██║     ║
    ║  ██║     ██║██║  ██║███████╗╚███╔███╔╝██║  ██║███████╗███████╗║
    ║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝║
    ║                    {Fore.CYAN}WAF/FIREWALL DETECTOR v2.0{Fore.RED}                 ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # WAF Signatures Database
    WAF_SIGNATURES = {
        'Cloudflare': {
            'headers': ['cf-ray', 'cf-cache-status', 'cf-request-id', 'cloudflare'],
            'cookies': ['__cfduid', '__cfruid'],
            'response': ['cloudflare', 'cf-ray', 'attention required'],
            'server': ['cloudflare'],
            'block_codes': [403, 503, 520, 521, 522, 523, 524],
        },
        'AWS WAF': {
            'headers': ['x-amzn-requestid', 'x-amzn-errortype', 'x-amz-cf-id', 'x-amz-cf-pop'],
            'cookies': ['AWSALB', 'AWSALBCORS'],
            'response': ['amazon', 'aws', 'waf'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'CloudFront': {
            'headers': ['x-amz-cf-id', 'x-amz-cf-pop', 'x-cloudfront-request-id'],
            'cookies': ['CloudFront-Policy', 'CloudFront-Signature'],
            'server': ['CloudFront', 'Amazon'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Akamai': {
            'headers': ['x-akamai-request-id', 'x-akamai-session-info', 'x-akamai-transformed'],
            'cookies': ['akaalb', 'ak_bmsc', 'bm_sz'],
            'server': ['Akamai', 'AkamaiGHost'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Imperva/Incapsula': {
            'headers': ['x-cdn', 'x-iinfo', 'incap_s', 'visid_incap'],
            'cookies': ['incap_ses_', 'visid_incap_', 'incap_visid_'],
            'server': ['Imperva', 'Incapsula'],
            'response': ['incapsula', 'imperva'],
            'block_codes': [403, 404, 500, 502, 503, 508],
        },
        'Sucuri': {
            'headers': ['x-sucuri-id', 'x-sucuri-cache', 'x-sucuri-block'],
            'cookies': ['sucuri_cloudproxy'],
            'server': ['Sucuri'],
            'response': ['sucuri', 'cloudproxy'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'F5 BIG-IP ASM': {
            'headers': ['x-wa-info', 'x-asm-request-id', 'x-f5-new-authenticated'],
            'cookies': ['TS', 'BIGipServer', 'ASM'],
            'server': ['BIG-IP', 'F5'],
            'response': ['the requested url was rejected', 'please consult with your administrator'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'ModSecurity': {
            'headers': ['x-mod-security', 'x-mod-sec-req-id'],
            'cookies': [],
            'server': ['modsecurity', 'mod_security'],
            'response': ['mod_security', 'modsecurity', 'web application firewall', 'request blocked'],
            'block_codes': [403, 406, 500],
        },
        'Citrix NetScaler': {
            'headers': ['x-netscaler-request-id', 'via'],
            'cookies': ['NSC_', 'citrix'],
            'server': ['NetScaler', 'Citrix'],
            'response': ['netscaler', 'citrix'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Barracuda': {
            'headers': ['x-barracuda-request-id', 'x-barracuda-block'],
            'cookies': ['barra'],
            'server': ['Barracuda'],
            'response': ['barracuda', 'blocked by'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Palo Alto': {
            'headers': ['x-paloalto-request-id'],
            'cookies': ['PAN'],
            'server': ['PaloAlto', 'PAN'],
            'response': ['palo alto', 'blocked'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Fortinet': {
            'headers': ['x-fortinet-request-id'],
            'cookies': ['Forti'],
            'server': ['Fortinet', 'FortiWeb'],
            'response': ['fortinet', 'fortiweb'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Wordfence': {
            'headers': ['x-wordfence'],
            'cookies': ['wfvt_', 'wordfence_'],
            'server': [],
            'response': ['wordfence', 'blocked by wordfence'],
            'block_codes': [403, 404, 500],
        },
        'StackPath': {
            'headers': ['x-stackpath-request-id'],
            'cookies': ['stackpath'],
            'server': ['StackPath'],
            'response': ['stackpath'],
            'block_codes': [403, 404, 500, 502, 503],
        },
        'Varnish': {
            'headers': ['x-varnish', 'via'],
            'cookies': [],
            'server': ['Varnish'],
            'response': ['varnish'],
            'block_codes': [403, 404, 500, 502, 503],
        },
    }
    
    # Known firewall ports
    FIREWALL_PORTS = {
        22: 'SSH Filtering',
        443: 'SSL Inspection',
        8080: 'Proxy Firewall',
        8443: 'SSL Inspection',
        31337: 'Norton Personal Firewall',
        32764: 'Linksys Firewall',
        41121: 'Panda Security',
        5000: 'UPnP Firewall',
        5900: 'VNC Filtering',
    }
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.responses = {}
        self.detected_wafs = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
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
        
        return url
        
    def send_probe_requests(self, url):
        """Send various probes to trigger WAF responses"""
        responses = {}
        
        headers_list = [
            {'User-Agent': 'Mozilla/5.0'},
            {'User-Agent': '() { :; }; /bin/bash -c "echo vulnerable"'},
            {'User-Agent': 'Mozilla/5.0', 'X-Forwarded-For': '127.0.0.1'},
            {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://evil.com'},
            {'User-Agent': 'Mozilla/5.0', 'X-Originating-IP': '127.0.0.1'},
            {'User-Agent': 'Mozilla/5.0', 'X-Remote-IP': '127.0.0.1'},
            {'User-Agent': 'Mozilla/5.0', 'X-Remote-Addr': '127.0.0.1'},
            {'User-Agent': 'Mozilla/5.0', 'X-Forwarded-Host': '127.0.0.1'},
        ]
        
        payloads = [
            '',
            "' OR '1'='1",
            "<script>alert(1)</script>",
            "../../../etc/passwd",
            "?id=1 UNION SELECT * FROM users",
            "?page=../../../../etc/passwd",
            "?id=1 AND 1=1",
            "?id=1 AND 1=2",
            "?q='><script>alert('XSS')</script>",
            "?q={{7*7}}",
        ]
        
        session = requests.Session()
        
        # Normal request
        try:
            resp = session.get(url, timeout=10, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
            responses['normal'] = resp
        except:
            pass
            
        # Probe with malicious payloads
        for i, payload in enumerate(payloads[:5]):
            try:
                probe_url = url + payload
                resp = session.get(probe_url, timeout=10, verify=False, 
                                  headers={'User-Agent': 'Mozilla/5.0'})
                responses[f'probe_{i}'] = resp
            except:
                pass
                
        # Probe with suspicious headers
        for i, headers in enumerate(headers_list[:5]):
            try:
                resp = session.get(url, timeout=10, verify=False, headers=headers)
                responses[f'header_probe_{i}'] = resp
            except:
                pass
                
        return responses
        
    def analyze_headers(self, headers):
        """Analyze response headers for WAF signatures"""
        findings = []
        
        for waf_name, signatures in self.WAF_SIGNATURES.items():
            # Check header signatures
            for sig in signatures.get('headers', []):
                for header in headers:
                    if sig.lower() in header.lower():
                        findings.append({
                            'waf': waf_name,
                            'evidence': f'Header: {header}: {headers[header]}',
                            'confidence': 'HIGH',
                            'source': 'header'
                        })
                        break
                        
            # Check cookie signatures
            cookie_header = headers.get('Set-Cookie', '')
            for sig in signatures.get('cookies', []):
                if sig.lower() in cookie_header.lower():
                    findings.append({
                        'waf': waf_name,
                        'evidence': f'Cookie: {sig}',
                        'confidence': 'HIGH',
                        'source': 'cookie'
                    })
                    break
                    
            # Check server header
            server = headers.get('Server', '')
            for sig in signatures.get('server', []):
                if sig.lower() in server.lower():
                    findings.append({
                        'waf': waf_name,
                        'evidence': f'Server: {server}',
                        'confidence': 'MEDIUM',
                        'source': 'server'
                    })
                    break
                    
        return findings
        
    def analyze_response_body(self, body, status_code):
        """Analyze response body for WAF signatures"""
        findings = []
        body_lower = body.lower() if body else ''
        
        for waf_name, signatures in self.WAF_SIGNATURES.items():
            # Check response signatures
            for sig in signatures.get('response', []):
                if sig.lower() in body_lower:
                    findings.append({
                        'waf': waf_name,
                        'evidence': f'Response contains: {sig}',
                        'confidence': 'HIGH',
                        'source': 'response_body'
                    })
                    break
                    
            # Check block codes
            if status_code in signatures.get('block_codes', []):
                # Only add if not already detected
                if not any(f['waf'] == waf_name for f in findings):
                    findings.append({
                        'waf': waf_name,
                        'evidence': f'Block code: {status_code}',
                        'confidence': 'MEDIUM',
                        'source': 'status_code'
                    })
                    
        return findings
        
    def detect_waf(self, url):
        """Main WAF detection logic"""
        all_findings = []
        
        # Send probes
        self.responses = self.send_probe_requests(url)
        
        for probe_name, response in self.responses.items():
            if not response:
                continue
                
            # Analyze headers
            header_findings = self.analyze_headers(response.headers)
            all_findings.extend(header_findings)
            
            # Analyze response body
            body_findings = self.analyze_response_body(response.text, response.status_code)
            all_findings.extend(body_findings)
            
        # Deduplicate and consolidate findings
        consolidated = {}
        for finding in all_findings:
            waf = finding['waf']
            if waf not in consolidated:
                consolidated[waf] = {
                    'waf': waf,
                    'evidence': [],
                    'confidence': finding['confidence'],
                    'sources': []
                }
                
            if finding['evidence'] not in consolidated[waf]['evidence']:
                consolidated[waf]['evidence'].append(finding['evidence'])
            if finding['source'] not in consolidated[waf]['sources']:
                consolidated[waf]['sources'].append(finding['source'])
            
            # Upgrade confidence if multiple evidence
            if len(consolidated[waf]['evidence']) > 2:
                consolidated[waf]['confidence'] = 'VERY HIGH'
            elif len(consolidated[waf]['evidence']) > 1:
                consolidated[waf]['confidence'] = 'HIGH'
                
        self.detected_wafs = list(consolidated.values())
        
        return self.detected_wafs
        
    def check_firewall_ports(self, domain):
        """Check for known firewall ports"""
        findings = []
        
        for port, description in self.FIREWALL_PORTS.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((domain, port))
                sock.close()
                
                if result == 0:
                    findings.append({
                        'port': port,
                        'description': description,
                        'state': 'open'
                    })
            except:
                pass
                
        return findings
        
    def generate_report(self):
        """Generate comprehensive detection report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] WAF/FIREWALL DETECTION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ WAF DETECTION ============
        print(f"\n{Fore.CYAN}[ WAF DETECTION RESULTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.detected_wafs:
            for waf in self.detected_wafs:
                confidence = waf['confidence']
                
                if confidence in ['VERY HIGH', 'HIGH']:
                    conf_color = Fore.RED
                elif confidence == 'MEDIUM':
                    conf_color = Fore.YELLOW
                else:
                    conf_color = Fore.GREEN
                    
                print(f"\n{conf_color}[+] {waf['waf']}{Style.RESET_ALL}")
                print(f"    Confidence: {conf_color}{confidence}{Style.RESET_ALL}")
                print(f"    Evidence:")
                
                for evidence in waf['evidence'][:5]:
                    print(f"      └─ {Fore.WHITE}{evidence}{Style.RESET_ALL}")
                    
                print(f"    Sources: {', '.join(set(waf['sources']))}")
        else:
            print(f"\n{Fore.GREEN}[✓] No WAF detected{Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}[!] Target may be unprotected or using non-standard WAF{Style.RESET_ALL}")
            
        # ============ RESPONSE ANALYSIS ============
        if 'normal' in self.responses and self.responses['normal']:
            normal_resp = self.responses['normal']
            
            print(f"\n{Fore.CYAN}[ RESPONSE ANALYSIS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}Status Code:{Style.RESET_ALL} {normal_resp.status_code}")
            print(f"{Fore.YELLOW}Server:{Style.RESET_ALL} {normal_resp.headers.get('Server', 'Unknown')}")
            print(f"{Fore.YELLOW}Content-Type:{Style.RESET_ALL} {normal_resp.headers.get('Content-Type', 'Unknown')}")
            print(f"{Fore.YELLOW}Response Size:{Style.RESET_ALL} {len(normal_resp.text)} bytes")
            
            # Response time differences
            probe_found = False
            for key in self.responses:
                if 'probe' in key and self.responses[key]:
                    probe_resp = self.responses[key]
                    if probe_resp.elapsed.total_seconds() > normal_resp.elapsed.total_seconds() * 2:
                        if not probe_found:
                            print(f"\n{Fore.YELLOW}[!] Suspicious delay on malicious request:{Style.RESET_ALL}")
                            probe_found = True
                        print(f"    {key}: {probe_resp.elapsed.total_seconds():.3f}s (Normal: {normal_resp.elapsed.total_seconds():.3f}s)")
                    
        # ============ FIREWALL PORT DETECTION ============
        firewall_ports = self.check_firewall_ports(self.domain)
        
        if firewall_ports:
            print(f"\n{Fore.CYAN}[ FIREWALL PORT DETECTION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for port in firewall_ports:
                print(f"\n{Fore.YELLOW}[!] Port {port['port']}: {port['description']}{Style.RESET_ALL}")
                print(f"    State: {Fore.GREEN}OPEN{Style.RESET_ALL}")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if not self.detected_wafs:
            print(f"\n{Fore.RED}[!] No WAF detected - consider implementing:{Style.RESET_ALL}")
            print(f"    {Fore.WHITE}├─ Cloudflare (free tier available){Style.RESET_ALL}")
            print(f"    {Fore.WHITE}├─ ModSecurity with OWASP CRS{Style.RESET_ALL}")
            print(f"    {Fore.WHITE}└─ AWS WAF or similar cloud WAF{Style.RESET_ALL}")
        else:
            for waf in self.detected_wafs:
                if waf['waf'] == 'Cloudflare':
                    print(f"\n{Fore.GREEN}[✓] Cloudflare detected - good protection{Style.RESET_ALL}")
                    print(f"    {Fore.WHITE}Ensure WAF rules are enabled and set to appropriate level{Style.RESET_ALL}")
                elif waf['waf'] in ['AWS WAF', 'CloudFront']:
                    print(f"\n{Fore.GREEN}[✓] AWS WAF detected{Style.RESET_ALL}")
                    print(f"    {Fore.WHITE}Verify rate limiting and SQL injection rules are active{Style.RESET_ALL}")
                elif waf['waf'] in ['ModSecurity']:
                    print(f"\n{Fore.YELLOW}[!] ModSecurity detected{Style.RESET_ALL}")
                    print(f"    {Fore.WHITE}Check if OWASP CRS is enabled and updated{Style.RESET_ALL}")
                    
        # ============ PENETRATION TESTER NOTES ============
        if self.detected_wafs:
            print(f"\n{Fore.CYAN}[ PENETRATION TESTER NOTES ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}WAF Bypass Techniques to Consider:{Style.RESET_ALL}")
            
            if any(w['waf'] in ['Cloudflare', 'AWS WAF', 'Akamai'] for w in self.detected_wafs):
                print(f"  {Fore.WHITE}├─ IP Rotation / Proxy Chains{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}├─ Payload Obfuscation{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}├─ Rate Limiting Avoidance{Style.RESET_ALL}")
                
            if any(w['waf'] == 'ModSecurity' for w in self.detected_wafs):
                print(f"  {Fore.WHITE}├─ HTTP Parameter Pollution{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}├─ Comment Injection{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}├─ Case Manipulation{Style.RESET_ALL}")
                
            if any(w['waf'] == 'Imperva/Incapsula' for w in self.detected_wafs):
                print(f"  {Fore.WHITE}├─ HTTP Verb Tampering{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}├─ Encoded Payloads{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}└─ Boundary Confusion{Style.RESET_ALL}")
                
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"waf_scan_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'detected_wafs': self.detected_wafs,
            'responses': {
                k: {
                    'status_code': v.status_code,
                    'headers': dict(v.headers),
                    'elapsed': v.elapsed.total_seconds()
                } if v else None
                for k, v in self.responses.items()
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive detection mode"""
        print(f"{Fore.GREEN}[*] WAF/Firewall Detector initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Signature-based detection for 15+ WAFs{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter URL (e.g., https://example.com): {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.url = self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Starting WAF/Firewall detection on {self.url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Sending probe requests...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Perform detection
        try:
            self.detect_waf(self.url)
        except Exception as e:
            print(f"{Fore.RED}[✗] Detection failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.detected_wafs:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] WAF/Firewall detection completed{Style.RESET_ALL}")


def detect_firewall_waf(url=None):
    """Main entry point for CLI compatibility"""
    detector = FirewallWAFDetector()
    
    # Display banner
    detector.print_header()
    
    if url:
        # Direct scan mode
        detector.url = detector.normalize_url(url)
        detector.start_time = datetime.now()
        
        try:
            detector.detect_waf(detector.url)
        except Exception as e:
            print(f"{Fore.RED}[✗] Detection failed: {e}{Style.RESET_ALL}")
            return
            
        detector.end_time = datetime.now()
        detector.generate_report()
    else:
        # Interactive mode
        detector.interactive_scan()


if __name__ == "__main__":
    detect_firewall_waf()
