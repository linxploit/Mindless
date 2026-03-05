#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: MALICIOUS INDICATOR SCANNER
Advanced Threat Intelligence IOC Scanner
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import socket
from datetime import datetime
from colorama import Fore, Style, init
import urllib.parse

init(autoreset=True)

class MaliciousIndicatorScanner:
    """Advanced IOC (Indicators of Compromise) scanner"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███╗   ███╗ █████╗ ██╗     ██╗ ██████╗██╗ ██████╗ ██╗   ██╗███████╗     ║
    ║  ████╗ ████║██╔══██╗██║     ██║██╔════╝██║██╔═══██╗██║   ██║██╔════╝     ║
    ║  ██╔████╔██║███████║██║     ██║██║     ██║██║   ██║██║   ██║███████╗     ║
    ║  ██║╚██╔╝██║██╔══██║██║     ██║██║     ██║██║   ██║██║   ██║╚════██║     ║
    ║  ██║ ╚═╝ ██║██║  ██║███████╗██║╚██████╗██║╚██████╔╝╚██████╔╝███████║     ║
    ║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝╚═╝ ╚═════╝  ╚═════╝ ╚══════╝     ║
    ║                    {Fore.CYAN}INDICATOR OF COMPROMISE SCANNER v2.0{Fore.RED}         ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # IOC Patterns
    IOC_PATTERNS = {
        'IPv4': {
            'pattern': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            'type': 'IP Address',
            'severity': 'MEDIUM',
            'description': 'IPv4 address - may indicate C2 server or malicious host'
        },
        'IPv6': {
            'pattern': r'\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b',
            'type': 'IPv6 Address',
            'severity': 'MEDIUM',
            'description': 'IPv6 address - check threat intelligence feeds'
        },
        'Domain': {
            'pattern': r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b',
            'type': 'Domain Name',
            'severity': 'MEDIUM',
            'description': 'Domain name - potential malicious domain'
        },
        'URL': {
            'pattern': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[-\w$.+!*\'(),;:@&=?/~#%]*)?',
            'type': 'URL',
            'severity': 'HIGH',
            'description': 'URL - may host malicious content or phishing'
        },
        'MD5': {
            'pattern': r'\b[a-fA-F0-9]{32}\b',
            'type': 'MD5 Hash',
            'severity': 'HIGH',
            'description': 'MD5 file hash - malware sample indicator'
        },
        'SHA1': {
            'pattern': r'\b[a-fA-F0-9]{40}\b',
            'type': 'SHA-1 Hash',
            'severity': 'HIGH',
            'description': 'SHA-1 file hash - malware sample indicator'
        },
        'SHA256': {
            'pattern': r'\b[a-fA-F0-9]{64}\b',
            'type': 'SHA-256 Hash',
            'severity': 'HIGH',
            'description': 'SHA-256 file hash - malware sample indicator'
        },
        'Email': {
            'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'type': 'Email Address',
            'severity': 'MEDIUM',
            'description': 'Email address - potential phishing or spam source'
        },
        'CVE': {
            'pattern': r'\bCVE-\d{4}-\d{4,7}\b',
            'type': 'CVE Identifier',
            'severity': 'INFO',
            'description': 'Common Vulnerability and Exposure ID'
        },
        'Windows Path': {
            'pattern': r'\b(?:[A-Za-z]:\\[^*|"<>?]*|\\\\[^*|"<>?]+\\[^*|"<>?]+)\b',
            'type': 'Windows File Path',
            'severity': 'MEDIUM',
            'description': 'Windows file path - potential malware installation path'
        },
        'Linux Path': {
            'pattern': r'\b(?:/[^/ ]*)+/?\b',
            'type': 'Linux/Unix File Path',
            'severity': 'MEDIUM',
            'description': 'Linux file path - potential malware installation path'
        },
        'Registry Key': {
            'pattern': r'\b(?:HKLM|HKCU|HKCR|HKU|HKCC)\\[A-Za-z0-9_\\ -]+\b',
            'type': 'Windows Registry Key',
            'severity': 'HIGH',
            'description': 'Windows registry key - persistence mechanism'
        },
        'Mutex': {
            'pattern': r'\b(?:Global\\|Local\\)?[A-Za-z0-9_\-{}]+\b',
            'type': 'Mutex',
            'severity': 'MEDIUM',
            'description': 'Mutex name - malware synchronization object'
        },
        'SSDeep': {
            'pattern': r'\b\d+:[A-Za-z0-9/+]+:[A-Za-z0-9/+]+\b',
            'type': 'SSDeep Fuzzy Hash',
            'severity': 'MEDIUM',
            'description': 'SSDeep hash - similarity hash for malware'
        }
    }
    
    # Malware family keywords
    MALWARE_KEYWORDS = [
        'ransomware', 'trojan', 'worm', 'virus', 'backdoor', 'keylogger',
        'spyware', 'adware', 'rootkit', 'botnet', 'dropper', 'loader',
        'exploit', 'payload', 'shellcode', 'malware', 'ransom', 'locky',
        'wannacry', 'notpetya', 'emotet', 'trickbot', 'qakbot', 'dridex',
        'zeus', 'citadel', 'spyeye', 'carbanak', 'apt', 'cobaltstrike',
        'meterpreter', 'mimikatz', 'bloodhound', 'empire', 'psexec'
    ]
    
    def __init__(self):
        self.content = None
        self.content_type = None
        self.content_name = None
        self.iocs = []
        self.scan_summary = {
            'total_iocs': 0,
            'by_type': {},
            'by_severity': {}
        }
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def load_content(self, content, content_type='text', content_name=None):
        """Load content for scanning"""
        self.content = content
        self.content_type = content_type
        self.content_name = content_name or 'Unknown Source'
        
    def scan_for_iocs(self):
        """Scan content for IOCs"""
        self.iocs = []
        
        for ioc_name, ioc_info in self.IOC_PATTERNS.items():
            pattern = ioc_info['pattern']
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            
            # Deduplicate
            unique_matches = list(set(matches))
            
            for match in unique_matches[:100]:  # Limit per type
                ioc = {
                    'ioc': match.strip(),
                    'type': ioc_info['type'],
                    'ioc_type': ioc_name,
                    'severity': ioc_info['severity'],
                    'description': ioc_info['description'],
                    'context': self.get_context(match)
                }
                self.iocs.append(ioc)
                
        # Scan for malware keywords
        for keyword in self.MALWARE_KEYWORDS:
            if keyword.lower() in self.content.lower():
                self.iocs.append({
                    'ioc': keyword,
                    'type': 'Malware Keyword',
                    'ioc_type': 'MALWARE_KEYWORD',
                    'severity': 'MEDIUM',
                    'description': f'Malware family/keyword: {keyword}',
                    'context': self.get_context(keyword)
                })
                
        # Sort IOCs by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
        self.iocs.sort(key=lambda x: severity_order.get(x['severity'], 5))
        
        # Generate summary
        self.generate_summary()
        
        return self.iocs
        
    def get_context(self, ioc, context_chars=50):
        """Get surrounding context for IOC"""
        if not self.content:
            return ''
            
        pos = self.content.lower().find(ioc.lower())
        if pos == -1:
            return ''
            
        start = max(0, pos - context_chars)
        end = min(len(self.content), pos + len(ioc) + context_chars)
        
        context = self.content[start:end]
        # Highlight the IOC
        context = context.replace(ioc, f"{Fore.RED}{ioc}{Fore.WHITE}")
        
        return context
        
    def generate_summary(self):
        """Generate scan summary"""
        self.scan_summary = {
            'total_iocs': len(self.iocs),
            'by_type': {},
            'by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        }
        
        for ioc in self.iocs:
            ioc_type = ioc['type']
            severity = ioc['severity']
            
            self.scan_summary['by_type'][ioc_type] = self.scan_summary['by_type'].get(ioc_type, 0) + 1
            self.scan_summary['by_severity'][severity] = self.scan_summary['by_severity'].get(severity, 0) + 1
            
    def resolve_iocs(self):
        """Resolve domain IOCs to IPs"""
        resolved = []
        
        for ioc in self.iocs:
            if ioc['ioc_type'] == 'Domain':
                try:
                    ip = socket.gethostbyname(ioc['ioc'])
                    ioc['resolved_ip'] = ip
                    resolved.append({'domain': ioc['ioc'], 'ip': ip})
                except:
                    ioc['resolved_ip'] = 'Unable to resolve'
                    
        return resolved
        
    def generate_report(self):
        """Generate comprehensive IOC scan report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] IOC SCAN REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Source: {Fore.LIGHTGREEN_EX}{self.content_name}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Content Type: {Fore.LIGHTGREEN_EX}{self.content_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Content Size: {Fore.LIGHTGREEN_EX}{len(self.content)} characters{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SCAN SUMMARY ============
        print(f"\n{Fore.CYAN}[ SCAN SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}Total IOCs Found: {Fore.LIGHTGREEN_EX}{self.scan_summary['total_iocs']}{Style.RESET_ALL}")
        
        # Severity breakdown
        print(f"\n  {Fore.WHITE}Severity Breakdown:{Style.RESET_ALL}")
        for severity, count in self.scan_summary['by_severity'].items():
            if count > 0:
                if severity == 'CRITICAL':
                    color = Fore.RED + Style.BRIGHT
                elif severity == 'HIGH':
                    color = Fore.RED
                elif severity == 'MEDIUM':
                    color = Fore.YELLOW
                elif severity == 'LOW':
                    color = Fore.CYAN
                else:
                    color = Fore.GREEN
                    
                print(f"    {color}[{severity}]{Style.RESET_ALL}: {count}")
                
        # Type breakdown
        print(f"\n  {Fore.WHITE}IOC Type Breakdown:{Style.RESET_ALL}")
        for ioc_type, count in sorted(self.scan_summary['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"    {Fore.CYAN}→{Style.RESET_ALL} {ioc_type}: {count}")
            
        # ============ DETAILED IOC LIST ============
        if self.iocs:
            print(f"\n{Fore.CYAN}[ DETECTED INDICATORS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            
            # Group by severity
            severity_groups = {}
            for ioc in self.iocs:
                severity = ioc['severity']
                if severity not in severity_groups:
                    severity_groups[severity] = []
                severity_groups[severity].append(ioc)
                
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                if severity in severity_groups:
                    if severity == 'CRITICAL':
                        print(f"\n  {Fore.RED}{Style.BRIGHT}[{severity} INDICATORS]{Style.RESET_ALL}")
                    elif severity == 'HIGH':
                        print(f"\n  {Fore.RED}[{severity} INDICATORS]{Style.RESET_ALL}")
                    elif severity == 'MEDIUM':
                        print(f"\n  {Fore.YELLOW}[{severity} INDICATORS]{Style.RESET_ALL}")
                    elif severity == 'LOW':
                        print(f"\n  {Fore.CYAN}[{severity} INDICATORS]{Style.RESET_ALL}")
                    else:
                        print(f"\n  {Fore.GREEN}[{severity} INDICATORS]{Style.RESET_ALL}")
                        
                    for i, ioc in enumerate(severity_groups[severity][:20], 1):
                        print(f"\n    {i}. {Fore.WHITE}{ioc['ioc']}{Style.RESET_ALL}")
                        print(f"       ├─ Type: {ioc['type']}")
                        print(f"       ├─ Description: {Fore.WHITE}{ioc['description']}{Style.RESET_ALL}")
                        
                        if 'resolved_ip' in ioc:
                            print(f"       ├─ Resolved IP: {Fore.WHITE}{ioc['resolved_ip']}{Style.RESET_ALL}")
                            
                        if ioc.get('context'):
                            print(f"       └─ Context: {ioc['context'][:100]}...")
                            
                    if len(severity_groups[severity]) > 20:
                        print(f"\n       ... and {len(severity_groups[severity]) - 20} more indicators")
                        
        else:
            print(f"\n  {Fore.GREEN}[✓] No indicators of compromise detected{Style.RESET_ALL}")
            
        # ============ DOMAIN RESOLUTION ============
        domains = [i for i in self.iocs if i['ioc_type'] == 'Domain']
        if domains:
            print(f"\n{Fore.CYAN}[ DOMAIN RESOLUTION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.YELLOW}[*] Resolving domains to IP addresses...{Style.RESET_ALL}")
            resolved = self.resolve_iocs()
            
            for item in resolved[:10]:
                print(f"    {Fore.WHITE}{item['domain']:30} → {item['ip']}{Style.RESET_ALL}")
                
        # ============ THREAT ASSESSMENT ============
        print(f"\n{Fore.CYAN}[ THREAT ASSESSMENT ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        critical_count = self.scan_summary['by_severity'].get('CRITICAL', 0)
        high_count = self.scan_summary['by_severity'].get('HIGH', 0)
        medium_count = self.scan_summary['by_severity'].get('MEDIUM', 0)
        
        if critical_count > 0 or high_count > 0:
            print(f"""
  {Fore.RED}[!] CRITICAL THREAT INDICATORS DETECTED{Style.RESET_ALL}
  
  This content contains indicators strongly associated with:
  • Malware infections
  • Command & Control infrastructure
  • Phishing campaigns
  • Data breach artifacts
  
  Immediate investigation recommended.
            """)
        elif medium_count > 5:
            print(f"""
  {Fore.YELLOW}[!] MODERATE THREAT INDICATORS DETECTED{Style.RESET_ALL}
  
  Multiple suspicious indicators found.
  Further analysis recommended.
            """)
        elif self.iocs:
            print(f"""
  {Fore.CYAN}[i] LOW THREAT INDICATORS DETECTED{Style.RESET_ALL}
  
  Some indicators present but threat level appears low.
  Verify context before taking action.
            """)
        else:
            print(f"""
  {Fore.GREEN}[✓] NO THREAT INDICATORS DETECTED{Style.RESET_ALL}
  
  The scanned content appears clean.
  No known indicators of compromise found.
            """)
            
        # ============ RECOMMENDATIONS ============
        if self.iocs:
            print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"""
  1. Block identified IOCs at network perimeter
  2. Search SIEM/logs for these indicators
  3. Isolate affected systems if found
  4. Update threat intelligence feeds
  5. Escalate to security operations team
            """)
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"ioc_scan_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'source': self.content_name,
            'content_type': self.content_type,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'summary': self.scan_summary,
            'iocs': self.iocs
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive IOC scanning mode"""
        print(f"{Fore.GREEN}[*] Malicious Indicator Scanner initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced IOC pattern detection engine{Style.RESET_ALL}\n")
        
        # Get input method
        print(f"{Fore.CYAN}Input Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Direct text input")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Load from file")
        
        choice = input(f"\n{Fore.YELLOW}[?] Select input method: {Style.RESET_ALL}").strip()
        
        content = ""
        content_name = ""
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}[?] Enter/paste text to scan (Ctrl+D to finish):{Style.RESET_ALL}")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except (EOFError, KeyboardInterrupt):
                content = '\n'.join(lines)
                content_name = "Direct Text Input"
                
        elif choice == "2":
            filename = input(f"{Fore.YELLOW}[?] Enter file path: {Style.RESET_ALL}").strip()
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                content_name = filename
                print(f"{Fore.GREEN}[✓] Loaded {len(content)} characters from {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        if not content.strip():
            print(f"{Fore.RED}[✗] No content to scan{Style.RESET_ALL}")
            return
            
        self.load_content(content, content_type='text', content_name=content_name)
        
        print(f"\n{Fore.YELLOW}[*] Scanning for indicators of compromise...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Scan for IOCs
        self.scan_for_iocs()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.iocs:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] IOC scanning completed{Style.RESET_ALL}")


def malicious_indicator_scan(content=None, filename=None):
    """Main entry point for CLI compatibility"""
    scanner = MaliciousIndicatorScanner()
    
    # Display banner
    scanner.print_header()
    
    if filename:
        # Scan file
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            scanner.load_content(content, content_type='file', content_name=filename)
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
            return
    elif content:
        # Direct scan
        scanner.load_content(content, content_type='direct', content_name='Direct Input')
    else:
        # Interactive mode
        scanner.interactive_scan()
        return
        
    scanner.start_time = datetime.now()
    scanner.scan_for_iocs()
    scanner.end_time = datetime.now()
    scanner.generate_report()


if __name__ == "__main__":
    malicious_indicator_scan()
