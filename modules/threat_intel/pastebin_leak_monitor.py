#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: PASTEBIN / LEAK MONITOR
Advanced OSINT Threat Intelligence & Data Leak Detection
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import requests
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from urllib.parse import quote_plus
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class PastebinLeakMonitor:
    """Advanced Pastebin monitoring and OSINT leak detection"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗  █████╗ ███████╗████████╗███████╗██████╗ ██╗███╗   ██╗     ║
    ║  ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║████╗  ██║     ║
    ║  ██████╔╝███████║███████╗   ██║   █████╗  ██████╔╝██║██╔██╗ ██║     ║
    ║  ██╔═══╝ ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║██║╚██╗██║     ║
    ║  ██║     ██║  ██║███████║   ██║   ███████╗██████╔╝██║██║ ╚████║     ║
    ║  ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝     ║
    ║                    {Fore.CYAN}PASTEBIN / LEAK MONITOR v2.0{Fore.RED}                 ║
    ║                    {Fore.YELLOW}[ OSINT - PASSIVE MONITORING ]{Fore.RED}              ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Pastebin search URL
    PASTEBIN_SEARCH = "https://pastebin.com/search?q={}"
    
    # Alternative leak sites
    LEAK_SITES = [
        "https://snipt.net/search/?q={}",
        "https://controlc.com/?s={}",
        "https://paste.ee/search?q={}",
        "https://justpaste.it/search?q={}",
        "https://ghostbin.com/search?q={}",
        "https://hastebin.com/search?q={}",
        "https://rentry.org/?query={}",
        "https://privnote.com/search?q={}",
    ]
    
    # Sensitive data patterns
    SENSITIVE_PATTERNS = {
        'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'API Key': r'\b([a-zA-Z0-9]{32,}|sk-[a-zA-Z0-9]{48,}|[a-zA-Z0-9_-]{40,})\b',
        'AWS Key': r'\b(AKIA|ASIA)[A-Z0-9]{16}\b',
        'Password': r'\b(password|passwd|pwd)[=:]\s*[^\s]{8,}\b',
        'Credit Card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
        'IP Address': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        'Private Key': r'-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
        'JWT Token': r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
    }
    
    def __init__(self):
        self.query = None
        self.query_type = None
        self.query_description = None
        self.results = []
        self.leak_summary = {
            'total_finds': 0,
            'by_source': {},
            'by_sensitive_data': {}
        }
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def set_query(self, query, query_type='keyword', description=None):
        """Set search query"""
        self.query = query
        self.query_type = query_type
        self.query_description = description or query
        
    def search_pastebin(self, query):
        """Search Pastebin for query"""
        results = []
        
        try:
            search_url = self.PASTEBIN_SEARCH.format(quote_plus(query))
            response = self.session.get(search_url, timeout=15, verify=False)
            
            if response.status_code == 200:
                # Extract paste links
                paste_pattern = r'/archive/([a-zA-Z0-9]+)'
                paste_matches = re.findall(paste_pattern, response.text)
                
                # Extract paste titles
                title_pattern = r'<a href="/archive/[^>]+>([^<]+)</a>'
                title_matches = re.findall(title_pattern, response.text)
                
                unique_pastes = {}
                for i, paste_id in enumerate(paste_matches):
                    if paste_id not in unique_pastes:
                        title = title_matches[i] if i < len(title_matches) else "Untitled"
                        unique_pastes[paste_id] = {
                            'id': paste_id,
                            'title': title.strip(),
                            'url': f'https://pastebin.com/raw/{paste_id}',
                            'view_url': f'https://pastebin.com/{paste_id}'
                        }
                        
                # Get first 5 results
                for paste_id, paste_info in list(unique_pastes.items())[:5]:
                    results.append({
                        'source': 'Pastebin',
                        'id': paste_id,
                        'title': paste_info['title'],
                        'url': paste_info['url'],
                        'view_url': paste_info['view_url'],
                        'relevance': 'HIGH' if query.lower() in paste_info['title'].lower() else 'MEDIUM'
                    })
                    
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Pastebin search error: {e}{Style.RESET_ALL}")
            
        return results
        
    def search_alternative_sites(self, query):
        """Search alternative leak/paste sites"""
        results = []
        
        for site_url in self.LEAK_SITES[:3]:  # Limit to first 3 to avoid timeouts
            try:
                search_url = site_url.format(quote_plus(query))
                response = self.session.get(search_url, timeout=10, verify=False)
                
                if response.status_code == 200:
                    site_name = site_url.split('//')[1].split('/')[0]
                    results.append({
                        'source': site_name,
                        'url': search_url,
                        'status': 'Available',
                        'relevance': 'UNKNOWN'
                    })
                    
            except Exception as e:
                pass
                
        return results
        
    def fetch_paste_content(self, url):
        """Fetch raw content of a paste"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return None
        
    def analyze_paste_content(self, content):
        """Analyze paste content for sensitive data"""
        findings = []
        
        for data_type, pattern in self.SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                findings.append({
                    'type': data_type,
                    'count': len(matches),
                    'sample': matches[0][:30] + '...' if len(matches[0]) > 30 else matches[0]
                })
                
        return findings
        
    def monitor(self):
        """Execute monitoring scan"""
        self.results = []
        
        print(f"{Fore.CYAN}[*] Searching Pastebin for '{self.query}'...{Style.RESET_ALL}")
        pastebin_results = self.search_pastebin(self.query)
        self.results.extend(pastebin_results)
        
        print(f"{Fore.CYAN}[*] Checking alternative sources...{Style.RESET_ALL}")
        alt_results = self.search_alternative_sites(self.query)
        self.results.extend(alt_results)
        
        # Fetch and analyze Pastebin results
        for result in self.results:
            if result['source'] == 'Pastebin' and 'url' in result:
                print(f"{Fore.CYAN}[*] Analyzing {result['id']}...{Style.RESET_ALL}")
                content = self.fetch_paste_content(result['url'])
                if content:
                    result['content_length'] = len(content)
                    result['sensitive_findings'] = self.analyze_paste_content(content)
                    
        # Generate summary
        self.generate_summary()
        
        return self.results
        
    def generate_summary(self):
        """Generate scan summary"""
        self.leak_summary = {
            'total_finds': len([r for r in self.results if r['source'] == 'Pastebin']),
            'by_source': {},
            'by_sensitive_data': {}
        }
        
        for result in self.results:
            source = result['source']
            self.leak_summary['by_source'][source] = self.leak_summary['by_source'].get(source, 0) + 1
            
            if 'sensitive_findings' in result:
                for finding in result['sensitive_findings']:
                    data_type = finding['type']
                    self.leak_summary['by_sensitive_data'][data_type] = \
                        self.leak_summary['by_sensitive_data'].get(data_type, 0) + finding['count']
                        
    def generate_report(self):
        """Generate comprehensive leak monitoring report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] PASTEBIN / LEAK MONITOR REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Search Query: {Fore.LIGHTGREEN_EX}{self.query}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Query Type: {Fore.LIGHTGREEN_EX}{self.query_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Description: {Fore.LIGHTGREEN_EX}{self.query_description}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SCAN SUMMARY ============
        print(f"\n{Fore.CYAN}[ SCAN SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        pastebin_finds = self.leak_summary['total_finds']
        
        if pastebin_finds > 0:
            print(f"\n  {Fore.RED}[!] POTENTIAL LEAK DETECTED{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Found {pastebin_finds} paste(s) containing your query{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.GREEN}[✓] No direct Pastebin results found{Style.RESET_ALL}")
            
        # Sensitive data summary
        if self.leak_summary['by_sensitive_data']:
            print(f"\n  {Fore.RED}[!] SENSITIVE DATA DETECTED{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Found in paste contents:{Style.RESET_ALL}")
            
            for data_type, count in self.leak_summary['by_sensitive_data'].items():
                if 'Password' in data_type or 'Key' in data_type:
                    color = Fore.RED
                elif 'Email' in data_type or 'IP' in data_type:
                    color = Fore.YELLOW
                else:
                    color = Fore.CYAN
                    
                print(f"    {color}→{Style.RESET_ALL} {data_type}: {count} occurrence(s)")
                
        # ============ PASTEBIN RESULTS ============
        pastebin_results = [r for r in self.results if r['source'] == 'Pastebin']
        
        if pastebin_results:
            print(f"\n{Fore.CYAN}[ PASTEBIN RESULTS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            
            for i, result in enumerate(pastebin_results, 1):
                print(f"\n  {i}. {Fore.WHITE}{result['title']}{Style.RESET_ALL}")
                print(f"     ├─ ID: {result['id']}")
                print(f"     ├─ URL: {Fore.CYAN}{result['view_url']}{Style.RESET_ALL}")
                print(f"     ├─ Relevance: {result['relevance']}")
                
                if 'content_length' in result:
                    print(f"     ├─ Size: {result['content_length']} bytes")
                    
                if 'sensitive_findings' in result and result['sensitive_findings']:
                    print(f"     └─ {Fore.RED}Sensitive Data Found:{Style.RESET_ALL}")
                    for finding in result['sensitive_findings']:
                        print(f"         • {finding['type']}: {finding['count']}x")
                        print(f"           Sample: {finding['sample']}")
                        
        # ============ ALTERNATIVE SOURCES ============
        alt_results = [r for r in self.results if r['source'] != 'Pastebin']
        
        if alt_results:
            print(f"\n{Fore.CYAN}[ ALTERNATIVE SOURCES ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for result in alt_results:
                print(f"\n  {Fore.WHITE}{result['source']}{Style.RESET_ALL}")
                print(f"     ├─ URL: {result['url']}")
                print(f"     └─ Status: {Fore.GREEN}{result['status']}{Style.RESET_ALL}")
                
        # ============ THREAT ASSESSMENT ============
        print(f"\n{Fore.CYAN}[ THREAT ASSESSMENT ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if pastebin_finds > 0:
            if self.leak_summary['by_sensitive_data']:
                print(f"""
  {Fore.RED}{Style.BRIGHT}[!] CRITICAL DATA LEAK DETECTED{Style.RESET_ALL}
  
  Your query was found in public pastes containing:
  • Sensitive information (passwords, keys, credentials)
  • Immediate action required
  
  Recommended Actions:
  1. Rotate ALL credentials immediately
  2. Enable 2FA/MFA on all accounts
  3. Monitor for unauthorized access
  4. Consider identity theft protection
  5. Contact relevant service providers
                """)
            else:
                print(f"""
  {Fore.YELLOW}[!] POTENTIAL INFORMATION DISCLOSURE{Style.RESET_ALL}
  
  Your query appears in public pastes.
  While no sensitive data was detected in samples:
  • Full pastes may contain more information
  • Pastes can be edited after creation
  • Multiple pastes indicate pattern
  
  Recommended Actions:
  1. Review all identified pastes
  2. Monitor for new appearances
  3. Consider proactive credential rotation
                """)
        else:
            print(f"""
  {Fore.GREEN}[✓] NO IMMEDIATE THREAT DETECTED{Style.RESET_ALL}
  
  Your query was not found in recent Pastebin content.
  Continue regular monitoring for:
  • New credential dumps
  • Corporate data leaks
  • Personal information exposure
            """)
            
        # ============ MONITORING RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ MONITORING RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"""
  1. {Fore.WHITE}Set up automated daily scans{Style.RESET_ALL}
  2. {Fore.WHITE}Monitor multiple paste sites{Style.RESET_ALL}
  3. {Fore.WHITE}Use variations of your query{Style.RESET_ALL}
  4. {Fore.WHITE}Check for encoded/obfuscated versions{Style.RESET_ALL}
  5. {Fore.WHITE}Subscribe to breach notification services{Style.RESET_ALL}
  6. {Fore.WHITE}Monitor dark web forums (advanced){Style.RESET_ALL}
  7. {Fore.WHITE}Implement credential rotation policy{Style.RESET_ALL}
        """)
        
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] OSINT - Passive monitoring only{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Results may not be comprehensive{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    False positives are possible{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"leak_monitor_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'query': self.query,
            'query_type': self.query_type,
            'query_description': self.query_description,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'summary': self.leak_summary,
            'results': self.results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_monitor(self):
        """Interactive leak monitoring mode"""
        print(f"{Fore.GREEN}[*] Pastebin/Leak Monitor initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] OSINT - Passive data leak detection{Style.RESET_ALL}\n")
        
        # Get search query
        print(f"{Fore.CYAN}Query Type:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Email address")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Domain name")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Username")
        print(f"  {Fore.WHITE}[4]{Style.RESET_ALL} API key / Token")
        print(f"  {Fore.WHITE}[5]{Style.RESET_ALL} Custom keyword")
        
        type_choice = input(f"\n{Fore.YELLOW}[?] Select query type: {Style.RESET_ALL}").strip()
        
        type_map = {
            '1': 'email',
            '2': 'domain',
            '3': 'username',
            '4': 'api_key',
            '5': 'keyword'
        }
        
        self.query_type = type_map.get(type_choice, 'keyword')
        
        # Get query
        if self.query_type == 'email':
            self.query = input(f"{Fore.YELLOW}[?] Enter email address: {Style.RESET_ALL}").strip().lower()
            self.query_description = f"Email: {self.query}"
        elif self.query_type == 'domain':
            self.query = input(f"{Fore.YELLOW}[?] Enter domain name: {Style.RESET_ALL}").strip().lower()
            self.query_description = f"Domain: {self.query}"
        elif self.query_type == 'username':
            self.query = input(f"{Fore.YELLOW}[?] Enter username: {Style.RESET_ALL}").strip()
            self.query_description = f"Username: {self.query}"
        elif self.query_type == 'api_key':
            self.query = input(f"{Fore.YELLOW}[?] Enter API key/token: {Style.RESET_ALL}").strip()
            self.query_description = f"API Key: {self.query[:10]}...{self.query[-5:]}"
        else:
            self.query = input(f"{Fore.YELLOW}[?] Enter search keyword: {Style.RESET_ALL}").strip()
            self.query_description = f"Keyword: {self.query}"
            
        if not self.query:
            print(f"{Fore.RED}[✗] No query specified{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.YELLOW}[*] Monitoring Pastebin and leak sites for: {self.query_description}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take 10-20 seconds...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Execute monitoring
        self.monitor()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Leak monitoring completed{Style.RESET_ALL}")


def pastebin_leak_monitor(query=None):
    """Main entry point for CLI compatibility"""
    monitor = PastebinLeakMonitor()
    
    # Display banner
    monitor.print_header()
    
    if query:
        # Direct scan mode
        monitor.set_query(query, 'direct', f'Query: {query}')
        monitor.start_time = datetime.now()
        monitor.monitor()
        monitor.end_time = datetime.now()
        monitor.generate_report()
    else:
        # Interactive mode
        monitor.interactive_monitor()


if __name__ == "__main__":
    pastebin_leak_monitor()
