#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: SUBDOMAIN ENUMERATOR
Advanced Subdomain Discovery & DNS Brute-Forcing
Author: ICAT Project | Linxploit.xyz
"""

import dns.resolver
import socket
import requests
import json
import concurrent.futures
import threading
from datetime import datetime
from colorama import Fore, Style, init
import re

init(autoreset=True)

class SubdomainEnumerator:
    """Advanced subdomain discovery using multiple techniques"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗██╗   ██╗██████╗ ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗    ║
    ║  ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║    ║
    ║  ███████╗██║   ██║██████╔╝██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║    ║
    ║  ╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ║
    ║  ███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ║
    ║  ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ║
    ║                    {Fore.CYAN}SUBDOMAIN ENUMERATOR v2.0{Fore.RED}                    ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Common subdomain wordlist (expanded)
    COMMON_SUBDOMAINS = [
        # Web services
        'www', 'ww2', 'web', 'webmail', 'mail', 'email', 'webdisk', 'webmail2',
        'cpanel', 'whm', 'webmin', 'plesk', 'cpcalendars', 'cpcontacts',
        'blog', 'shop', 'store', 'forum', 'community', 'support', 'help',
        'docs', 'documentation', 'wiki', 'kb', 'knowledgebase',
        'status', 'health', 'monitor', 'stats', 'statistics', 'analytics',
        'api', 'api-dev', 'dev-api', 'rest', 'graphql', 'swagger', 'swagger-ui',
        'jenkins', 'gitlab', 'github', 'bitbucket', 'git', 'svn', 'cvs',
        'travis', 'circleci', 'teamcity', 'bamboo', 'crucible',
        
        # Development and testing
        'dev', 'development', 'test', 'testing', 'staging', 'stage', 'qa',
        'uat', 'demo', 'sandbox', 'playground', 'beta', 'alpha', 'preview',
        'uat', 'preprod', 'pre-production', 'stage', 'staging',
        
        # Administrative interfaces
        'admin', 'administrator', 'admincp', 'adminpanel', 'dashboard',
        'manager', 'management', 'control', 'controlpanel', 'cpanel',
        'phpmyadmin', 'pma', 'myadmin', 'mysql', 'pgadmin', 'adminer',
        'redis', 'rabbitmq', 'kafka', 'zookeeper', 'elastic', 'kibana',
        'logstash', 'grafana', 'prometheus', 'alertmanager',
        
        # Security and authentication
        'login', 'signin', 'sign-in', 'auth', 'authentication', 'oauth',
        'sso', 'cas', 'saml', 'openid', 'keycloak', 'auth0',
        '2fa', 'twofactor', 'mfa', 'secure', 'security',
        
        # Monitoring and logging
        'logs', 'log', 'logging', 'splunk', 'sumologic', 'datadog',
        'newrelic', 'appdynamics', 'dynatrace', 'instana',
        
        # File storage and transfer
        'ftp', 'sftp', 'ftps', 'files', 'transfer', 'send', 'receive',
        'upload', 'download', 'dl', 'up', 'cdn', 'static', 'assets',
        'media', 'images', 'img', 'css', 'js', 'javascript',
        
        # Email services
        'smtp', 'pop', 'pop3', 'imap', 'exchange', 'owa', 'webmail',
        'roundcube', 'squirrelmail', 'horde', 'zimbra', 'rainloop',
        
        # Databases
        'db', 'database', 'mysql', 'postgres', 'mongodb', 'cassandra',
        'redis', 'memcached', 'couchdb', 'neo4j', 'influxdb',
        'oracle', 'mssql', 'sqlserver', 'db2', 'mariadb',
        
        # Infrastructure
        'ns1', 'ns2', 'ns3', 'ns4', 'dns', 'dns1', 'dns2',
        'vpn', 'vpn1', 'vpn2', 'openvpn', 'wireguard', 'ipsec',
        'proxy', 'proxy1', 'proxy2', 'squid', 'nginx', 'apache',
        'haproxy', 'traefik', 'envoy', 'istio', 'consul',
        
        # Cloud services
        'aws', 'azure', 'gcp', 'google', 'amazon', 'microsoft',
        's3', 'bucket', 'storage', 'cloud', 'compute', 'lambda',
        'ec2', 'rds', 'elb', 'alb', 'nlb', 'route53',
        
        # IoT and devices
        'printer', 'print', 'scan', 'scanner', 'cam', 'camera',
        'webcam', 'nvr', 'dvr', 'router', 'switch', 'ap', 'wifi',
        'nas', 'storage', 'backup', 'tape', 'drive',
        
        # Miscellaneous
        'remote', 'rdp', 'vnc', 'teamviewer', 'anydesk',
        'chat', 'discord', 'slack', 'teams', 'zoom', 'meet',
        'calendar', 'cal', 'drive', 'docs', 'sheets', 'slides',
        'forms', 'survey', 'poll', 'vote', 'feedback',
    ]
    
    # Certificate transparency log sources
    CRT_SH_URL = "https://crt.sh/?q=%25.{}&output=json"
    
    def __init__(self):
        self.domain = None
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 3
        self.resolver.lifetime = 3
        self.subdomains = []
        self.resolved_subdomains = []
        self.lock = threading.Lock()
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.threads = 50
        self.use_crt_sh = True
        self.use_bruteforce = True
        self.resolve_ips = True
        
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
        
    def get_crt_sh_subdomains(self):
        """Get subdomains from crt.sh certificate transparency logs"""
        subdomains = set()
        
        try:
            url = self.CRT_SH_URL.format(self.domain)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for entry in data:
                    name_value = entry.get('name_value', '')
                    # Split multi-domain entries
                    for name in name_value.split('\n'):
                        name = name.strip().lower()
                        if name.endswith(self.domain) and name != self.domain:
                            subdomains.add(name)
                            
                print(f"{Fore.GREEN}[✓] crt.sh: Found {len(subdomains)} subdomains{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.YELLOW}[!] crt.sh query failed: {e}{Style.RESET_ALL}")
            
        return list(subdomains)
        
    def check_subdomain(self, subdomain):
        """Check if subdomain resolves"""
        full_domain = f"{subdomain}.{self.domain}"
        
        try:
            answers = self.resolver.resolve(full_domain, 'A')
            ip = str(answers[0])
            
            with self.lock:
                self.resolved_subdomains.append({
                    'subdomain': full_domain,
                    'ip': ip,
                    'type': 'A'
                })
                
            # Try to get additional records
            try:
                answers_aaaa = self.resolver.resolve(full_domain, 'AAAA')
                ipv6 = str(answers_aaaa[0])
                with self.lock:
                    self.resolved_subdomains.append({
                        'subdomain': full_domain,
                        'ip': ipv6,
                        'type': 'AAAA'
                    })
            except:
                pass
                
            # Try to get CNAME
            try:
                answers_cname = self.resolver.resolve(full_domain, 'CNAME')
                cname = str(answers_cname[0])
                with self.lock:
                    # Update existing entry with CNAME
                    for entry in self.resolved_subdomains:
                        if entry['subdomain'] == full_domain and entry['type'] == 'A':
                            entry['cname'] = cname
                            break
            except:
                pass
                
            return True
            
        except:
            return False
            
    def brute_force_subdomains(self, wordlist=None):
        """Brute force subdomains using wordlist"""
        if not wordlist:
            wordlist = self.COMMON_SUBDOMAINS
            
        total = len(wordlist)
        found = 0
        self.resolved_subdomains = []
        
        print(f"\n{Fore.CYAN}[*] Brute-forcing {total} common subdomains...{Style.RESET_ALL}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_sub = {executor.submit(self.check_subdomain, sub): sub for sub in wordlist}
            
            for i, future in enumerate(concurrent.futures.as_completed(future_to_sub), 1):
                sub = future_to_sub[future]
                if future.result():
                    found += 1
                    
                # Progress indicator
                if i % 50 == 0 or i == total:
                    print(f"\r  Progress: {i}/{total} ({i/total*100:.1f}%) | Found: {found}", end="")
                    
        print(f"\n  {Fore.GREEN}[✓] Found {found} resolvable subdomains{Style.RESET_ALL}")
        
        return self.resolved_subdomains
        
    def enumerate_with_techniques(self):
        """Enumerate subdomains using multiple techniques"""
        all_subdomains = set()
        
        # Technique 1: Certificate transparency logs
        if self.use_crt_sh:
            print(f"{Fore.CYAN}[*] Querying crt.sh certificate logs...{Style.RESET_ALL}")
            crt_subdomains = self.get_crt_sh_subdomains()
            all_subdomains.update(crt_subdomains)
            
        # Technique 2: Common subdomain bruteforce
        if self.use_bruteforce:
            print(f"{Fore.CYAN}[*] Starting brute-force enumeration...{Style.RESET_ALL}")
            self.brute_force_subdomains()
            
            # Add resolved subdomains to set
            for sub in self.resolved_subdomains:
                all_subdomains.add(sub['subdomain'])
                
        # Sort and deduplicate
        self.subdomains = sorted(list(all_subdomains))
        
        return self.subdomains
        
    def resolve_subdomains(self, subdomains):
        """Resolve IP addresses for subdomains"""
        resolved = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_sub = {executor.submit(self.check_subdomain, sub.replace(f".{self.domain}", "")): sub 
                           for sub in subdomains if sub != self.domain}
                           
            for future in concurrent.futures.as_completed(future_to_sub):
                future.result()
                
        return self.resolved_subdomains
        
    def generate_report(self):
        """Generate comprehensive subdomain enumeration report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] SUBDOMAIN ENUMERATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SUMMARY ============
        print(f"\n{Fore.CYAN}[ ENUMERATION SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        unique_subdomains = len(set([s['subdomain'] for s in self.resolved_subdomains]))
        print(f"\n  {Fore.WHITE}Total Unique Subdomains:{Style.RESET_ALL} {Fore.GREEN}{unique_subdomains}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Total DNS Records:{Style.RESET_ALL} {len(self.resolved_subdomains)}")
        
        # Count by record type
        a_count = len([s for s in self.resolved_subdomains if s['type'] == 'A'])
        aaaa_count = len([s for s in self.resolved_subdomains if s['type'] == 'AAAA'])
        
        print(f"\n  {Fore.WHITE}IPv4 Addresses (A):{Style.RESET_ALL} {a_count}")
        print(f"  {Fore.WHITE}IPv6 Addresses (AAAA):{Style.RESET_ALL} {aaaa_count}")
        
        # ============ SUBDOMAINS TABLE ============
        if self.resolved_subdomains:
            print(f"\n{Fore.CYAN}[ RESOLVED SUBDOMAINS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}{'SUBDOMAIN':<45} {'IP ADDRESS':<20} {'TYPE':<6}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}{'-' * 45} {'-' * 20} {'-' * 6}{Style.RESET_ALL}")
            
            # Sort by subdomain
            sorted_subs = sorted(self.resolved_subdomains, key=lambda x: x['subdomain'])
            
            for entry in sorted_subs[:50]:  # Limit to 50 for display
                sub = entry['subdomain']
                ip = entry['ip']
                type_ = entry['type']
                
                if type_ == 'A':
                    ip_color = Fore.GREEN
                elif type_ == 'AAAA':
                    ip_color = Fore.CYAN
                else:
                    ip_color = Fore.WHITE
                    
                print(f"  {Fore.WHITE}{sub:<45}{Style.RESET_ALL} {ip_color}{ip:<20}{Style.RESET_ALL} {type_:<6}")
                
                if 'cname' in entry:
                    print(f"  {' ' * 47}└─ CNAME: {entry['cname']}")
                    
            if len(sorted_subs) > 50:
                print(f"\n  {Fore.YELLOW}... and {len(sorted_subs) - 50} more subdomains{Style.RESET_ALL}")
                
        # ============ IP STATISTICS ============
        if self.resolved_subdomains:
            ip_addresses = [s['ip'] for s in self.resolved_subdomains if s['type'] == 'A']
            unique_ips = set(ip_addresses)
            
            print(f"\n{Fore.CYAN}[ IP ADDRESS STATISTICS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}Unique IP Addresses:{Style.RESET_ALL} {len(unique_ips)}")
            print(f"  {Fore.WHITE}Subdomains per IP:{Style.RESET_ALL} {len(ip_addresses)/len(unique_ips):.1f} average")
            
            # Find IPs with most subdomains
            from collections import Counter
            ip_counter = Counter(ip_addresses)
            top_ips = ip_counter.most_common(5)
            
            if top_ips:
                print(f"\n  {Fore.WHITE}Top IPs:{Style.RESET_ALL}")
                for ip, count in top_ips:
                    print(f"    {Fore.CYAN}• {ip}:{Style.RESET_ALL} {count} subdomain(s)")
                    
        # ============ SECURITY INSIGHTS ============
        print(f"\n{Fore.CYAN}[ SECURITY INSIGHTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Check for admin panels
        admin_keywords = ['admin', 'cpanel', 'whm', 'phpmyadmin', 'pma', 'dashboard']
        admin_subs = [s for s in self.resolved_subdomains 
                     if any(k in s['subdomain'].lower() for k in admin_keywords)]
        
        if admin_subs:
            print(f"\n  {Fore.YELLOW}[!] Admin panels exposed:{Style.RESET_ALL}")
            for s in admin_subs[:5]:
                print(f"      • {s['subdomain']} → {s['ip']}")
                
        # Check for development subdomains
        dev_keywords = ['dev', 'test', 'staging', 'qa', 'uat', 'demo', 'beta']
        dev_subs = [s for s in self.resolved_subdomains 
                   if any(k in s['subdomain'].lower() for k in dev_keywords)]
        
        if dev_subs:
            print(f"\n  {Fore.YELLOW}[!] Development subdomains exposed:{Style.RESET_ALL}")
            for s in dev_subs[:5]:
                print(f"      • {s['subdomain']} → {s['ip']}")
                
        # Check for API endpoints
        api_subs = [s for s in self.resolved_subdomains if 'api' in s['subdomain'].lower()]
        
        if api_subs:
            print(f"\n  {Fore.CYAN}[i] API endpoints discovered:{Style.RESET_ALL}")
            for s in api_subs[:5]:
                print(f"      • {s['subdomain']}")
                
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if admin_subs:
            print(f"\n  {Fore.YELLOW}• Restrict access to admin panels (IP whitelisting, VPN){Style.RESET_ALL}")
        if dev_subs:
            print(f"\n  {Fore.YELLOW}• Remove or password-protect development subdomains{Style.RESET_ALL}")
        if len(unique_ips) < len(set([s['subdomain'] for s in self.resolved_subdomains])):
            print(f"\n  {Fore.CYAN}• Multiple subdomains share IPs - potential virtual hosting{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"subdomains_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'total_subdomains': len(set([s['subdomain'] for s in self.resolved_subdomains])),
            'subdomains': self.resolved_subdomains,
            'unique_ips': list(set([s['ip'] for s in self.resolved_subdomains if s['type'] == 'A']))
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def export_txt(self, filename=None):
        """Export subdomains to text file"""
        if not filename:
            filename = f"subdomains_{self.domain}_{self.scan_id}.txt"
            
        try:
            with open(filename, 'w') as f:
                unique_subs = set([s['subdomain'] for s in self.resolved_subdomains])
                for sub in sorted(unique_subs):
                    f.write(f"{sub}\n")
                    
            print(f"{Fore.GREEN}[✓] Subdomains exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_enum(self):
        """Interactive subdomain enumeration mode"""
        print(f"{Fore.GREEN}[*] Subdomain Enumerator initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multiple discovery techniques: DNS bruteforce, CT logs{Style.RESET_ALL}\n")
        
        # Get domain
        domain_input = input(f"{Fore.YELLOW}[?] Enter domain to enumerate: {Style.RESET_ALL}").strip()
        
        if not domain_input:
            print(f"{Fore.RED}[✗] No domain specified{Style.RESET_ALL}")
            return
            
        self.normalize_domain(domain_input)
        
        # Configure scan
        print(f"\n{Fore.CYAN}Scan Configuration:{Style.RESET_ALL}")
        
        use_crt = input(f"{Fore.YELLOW}[?] Use certificate transparency logs? (y/n, default y): {Style.RESET_ALL}").strip().lower()
        self.use_crt_sh = use_crt != 'n'
        
        use_brute = input(f"{Fore.YELLOW}[?] Use DNS bruteforce? (y/n, default y): {Style.RESET_ALL}").strip().lower()
        self.use_bruteforce = use_brute != 'n'
        
        try:
            threads = input(f"{Fore.YELLOW}[?] Threads (default 50): {Style.RESET_ALL}").strip()
            self.threads = int(threads) if threads else 50
        except:
            self.threads = 50
            
        print(f"\n{Fore.YELLOW}[*] Starting subdomain enumeration for {self.domain}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take several minutes...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Enumerate subdomains
        self.enumerate_with_techniques()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export options
        if self.resolved_subdomains:
            print(f"\n{Fore.CYAN}Export Options:{Style.RESET_ALL}")
            export_json = input(f"{Fore.YELLOW}[?] Export to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export_json == 'y':
                self.export_report()
                
            export_txt = input(f"{Fore.YELLOW}[?] Export subdomains to text file? (y/n): {Style.RESET_ALL}").strip().lower()
            if export_txt == 'y':
                self.export_txt()
                
        print(f"\n{Fore.GREEN}[✓] Subdomain enumeration completed{Style.RESET_ALL}")


def subdomain_enum(domain=None):
    """Main entry point for CLI compatibility"""
    enumerator = SubdomainEnumerator()
    
    # Display banner
    enumerator.print_header()
    
    if domain:
        # Direct scan mode
        enumerator.normalize_domain(domain)
        enumerator.start_time = datetime.now()
        
        print(f"\n  {Fore.YELLOW}[*] Starting subdomain enumeration for {domain}...{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] Using DNS bruteforce + CT logs{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] This may take 20-60 seconds{Style.RESET_ALL}\n")
        
        try:
            enumerator.enumerate_with_techniques()
            enumerator.end_time = datetime.now()
            enumerator.generate_report()
        except Exception as e:
            print(f"{Fore.RED}[✗] Subdomain enumeration failed: {e}{Style.RESET_ALL}")
    else:
        # Interactive mode
        enumerator.interactive_enum()


if __name__ == "__main__":
    subdomain_enum()