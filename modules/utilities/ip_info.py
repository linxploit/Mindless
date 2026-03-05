#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: IP INFORMATION FINDER
Advanced IP Geolocation & Network Intelligence
Author: ICAT Project | Linxploit.xyz
"""

import requests
import socket
import json
import ipaddress
from datetime import datetime
from colorama import Fore, Style, init
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class IPInfoFinder:
    """Advanced IP address intelligence and geolocation"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗██████╗     ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗  ║
    ║  ██║██╔══██╗    ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║  ║
    ║  ██║██████╔╝    ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║  ║
    ║  ██║██╔═══╝     ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║  ║
    ║  ██║██║         ██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║  ║
    ║  ╚═╝╚═╝         ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝  ║
    ║                    {Fore.GREEN}IP INFORMATION FINDER v2.0{Fore.CYAN}                    ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # IP Geolocation API endpoints
    GEOIP_SERVICES = {
        'ip-api': {
            'url': 'http://ip-api.com/json/{}',
            'fields': ['status', 'country', 'countryCode', 'region', 'regionName', 
                      'city', 'zip', 'lat', 'lon', 'timezone', 'isp', 'org', 'as',
                      'mobile', 'proxy', 'hosting', 'query']
        },
        'ipinfo': {
            'url': 'https://ipinfo.io/{}/json',
            'fields': ['ip', 'hostname', 'city', 'region', 'country', 'loc', 'org', 'postal', 'timezone']
        }
    }
    
    # ASN to provider mapping (partial)
    ASN_PROVIDERS = {
        '15169': 'Google',
        '16509': 'Amazon AWS',
        '8075': 'Microsoft',
        '32934': 'Facebook',
        '13335': 'Cloudflare',
        '20940': 'Akamai',
        '16625': 'Akamai',
        '14618': 'Amazon AWS',
        '3': 'MIT',
        '714': 'Apple',
        '8068': 'Microsoft',
        '5413': 'Microsoft',
        '36692': 'Microsoft',
        '40065': 'Microsoft',
        '36351': 'Microsoft',
        '19994': 'Microsoft',
    }
    
    def __init__(self):
        self.ip = None
        self.ip_version = None
        self.is_private = False
        self.geo_data = {}
        self.threat_data = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def validate_ip(self, ip):
        """Validate and classify IP address"""
        try:
            # Try IPv4
            ip_obj = ipaddress.ip_address(ip)
            self.ip = str(ip_obj)
            self.ip_version = ip_obj.version
            self.is_private = ip_obj.is_private
            self.is_loopback = ip_obj.is_loopback
            self.is_multicast = ip_obj.is_multicast
            self.is_global = ip_obj.is_global
            return True
        except ValueError:
            # Try hostname resolution
            try:
                self.ip = socket.gethostbyname(ip)
                self.ip_version = 4
                self.is_private = False
                return True
            except:
                return False
                
    def get_geolocation_ipapi(self, ip):
        """Get geolocation from ip-api.com"""
        try:
            url = self.GEOIP_SERVICES['ip-api']['url'].format(ip)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data
        except:
            pass
        return None
        
    def get_geolocation_ipinfo(self, ip):
        """Get geolocation from ipinfo.io"""
        try:
            url = self.GEOIP_SERVICES['ipinfo']['url'].format(ip)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
        
    def get_geolocation(self, ip):
        """Get geolocation from multiple services"""
        self.geo_data = {}
        
        # Try ip-api first (more detailed, no API key)
        ipapi_data = self.get_geolocation_ipapi(ip)
        if ipapi_data:
            self.geo_data['ip-api'] = ipapi_data
            
        # Try ipinfo as backup
        ipinfo_data = self.get_geolocation_ipinfo(ip)
        if ipinfo_data:
            self.geo_data['ipinfo'] = ipinfo_data
            
        return self.geo_data
        
    def parse_asn(self, as_string):
        """Parse ASN information"""
        if not as_string:
            return None
            
        # Format: "AS15169 Google LLC"
        parts = as_string.split(' ', 1)
        asn = parts[0].replace('AS', '') if parts[0].startswith('AS') else parts[0]
        provider = parts[1] if len(parts) > 1 else self.ASN_PROVIDERS.get(asn, 'Unknown')
        
        return {
            'asn': asn,
            'provider': provider,
            'full': as_string
        }
        
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return '127.0.0.1'
            
    def get_public_ip(self):
        """Get public IP address"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            return response.json().get('ip')
        except:
            try:
                response = requests.get('https://icanhazip.com', timeout=10)
                return response.text.strip()
            except:
                return None
                
    def reverse_dns(self, ip):
        """Perform reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
            
    def whois_lookup(self, ip):
        """Simplified WHOIS lookup (requires python-whois)"""
        try:
            import whois
            w = whois.whois(ip)
            return {
                'registrar': w.registrar,
                'org': w.org,
                'country': w.country
            }
        except:
            return None
            
    def generate_report(self):
        """Generate comprehensive IP information report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] IP INFORMATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target IP: {Fore.LIGHTGREEN_EX}{self.ip}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ IP CLASSIFICATION ============
        print(f"\n{Fore.CYAN}[ IP CLASSIFICATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}IP Version:{Style.RESET_ALL} IPv{self.ip_version}")
        print(f"  {Fore.WHITE}Type:{Style.RESET_ALL} {'Private' if self.is_private else 'Public'}{' (Loopback)' if self.is_loopback else ''}{' (Multicast)' if self.is_multicast else ''}")
        print(f"  {Fore.WHITE}Global:{Style.RESET_ALL} {'Yes' if self.is_global else 'No'}")
        
        # Reverse DNS
        hostname = self.reverse_dns(self.ip)
        if hostname:
            print(f"  {Fore.WHITE}Reverse DNS:{Style.RESET_ALL} {hostname}")
            
        # ============ GEOLOCATION ============
        if 'ip-api' in self.geo_data:
            data = self.geo_data['ip-api']
            
            print(f"\n{Fore.CYAN}[ GEOLOCATION (ip-api.com) ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n  {Fore.WHITE}Country:{Style.RESET_ALL} {data.get('country', 'Unknown')} ({data.get('countryCode', '??')})")
            print(f"  {Fore.WHITE}Region:{Style.RESET_ALL} {data.get('regionName', 'Unknown')}")
            print(f"  {Fore.WHITE}City:{Style.RESET_ALL} {data.get('city', 'Unknown')}")
            print(f"  {Fore.WHITE}ZIP/Postal:{Style.RESET_ALL} {data.get('zip', 'Unknown')}")
            print(f"  {Fore.WHITE}Coordinates:{Style.RESET_ALL} {data.get('lat', '?')}, {data.get('lon', '?')}")
            print(f"  {Fore.WHITE}Timezone:{Style.RESET_ALL} {data.get('timezone', 'Unknown')}")
            
            # Google Maps link
            if data.get('lat') and data.get('lon'):
                maps_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
                print(f"  {Fore.WHITE}Google Maps:{Style.RESET_ALL} {Fore.CYAN}{maps_url}{Style.RESET_ALL}")
                
        elif 'ipinfo' in self.geo_data:
            data = self.geo_data['ipinfo']
            
            print(f"\n{Fore.CYAN}[ GEOLOCATION (ipinfo.io) ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n  {Fore.WHITE}IP:{Style.RESET_ALL} {data.get('ip', 'Unknown')}")
            if data.get('hostname'):
                print(f"  {Fore.WHITE}Hostname:{Style.RESET_ALL} {data['hostname']}")
            print(f"  {Fore.WHITE}City:{Style.RESET_ALL} {data.get('city', 'Unknown')}")
            print(f"  {Fore.WHITE}Region:{Style.RESET_ALL} {data.get('region', 'Unknown')}")
            print(f"  {Fore.WHITE}Country:{Style.RESET_ALL} {data.get('country', 'Unknown')}")
            print(f"  {Fore.WHITE}Location:{Style.RESET_ALL} {data.get('loc', 'Unknown')}")
            print(f"  {Fore.WHITE}Postal:{Style.RESET_ALL} {data.get('postal', 'Unknown')}")
            print(f"  {Fore.WHITE}Timezone:{Style.RESET_ALL} {data.get('timezone', 'Unknown')}")
            
        else:
            print(f"\n  {Fore.YELLOW}[!] Geolocation data unavailable{Style.RESET_ALL}")
            
        # ============ NETWORK INFORMATION ============
        if 'ip-api' in self.geo_data:
            data = self.geo_data['ip-api']
            
            print(f"\n{Fore.CYAN}[ NETWORK INFORMATION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n  {Fore.WHITE}ISP:{Style.RESET_ALL} {data.get('isp', 'Unknown')}")
            print(f"  {Fore.WHITE}Organization:{Style.RESET_ALL} {data.get('org', 'Unknown')}")
            
            # Parse ASN
            as_data = self.parse_asn(data.get('as', ''))
            if as_data:
                print(f"  {Fore.WHITE}ASN:{Style.RESET_ALL} AS{as_data['asn']}")
                print(f"  {Fore.WHITE}Provider:{Style.RESET_ALL} {as_data['provider']}")
                
            print(f"\n  {Fore.WHITE}Connection Type:{Style.RESET_ALL}")
            print(f"    ├─ Mobile: {Fore.CYAN}{data.get('mobile', False)}{Style.RESET_ALL}")
            print(f"    ├─ Proxy: {Fore.YELLOW if data.get('proxy') else Fore.GREEN}{data.get('proxy', False)}{Style.RESET_ALL}")
            print(f"    └─ Hosting: {Fore.YELLOW if data.get('hosting') else Fore.GREEN}{data.get('hosting', False)}{Style.RESET_ALL}")
            
        # ============ LOCAL NETWORK ============
        if self.is_private:
            print(f"\n{Fore.CYAN}[ LOCAL NETWORK ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            print(f"\n  {Fore.WHITE}This is a private/local IP address{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Cannot determine geolocation for private IPs{Style.RESET_ALL}")
            
            # Try to get local network info
            try:
                local_ip = self.get_local_ip()
                print(f"\n  {Fore.WHITE}Your local IP:{Style.RESET_ALL} {local_ip}")
            except:
                pass
                
        # ============ YOUR PUBLIC IP ============
        if self.ip == 'me' or self.ip == 'myip' or self.ip == 'public':
            public_ip = self.get_public_ip()
            if public_ip:
                print(f"\n{Fore.CYAN}[ YOUR PUBLIC IP ]{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
                print(f"\n  {Fore.WHITE}Public IP Address:{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}{public_ip}{Style.RESET_ALL}")
                
        # ============ THREAT INTELLIGENCE ============
        if not self.is_private and not self.is_loopback:
            print(f"\n{Fore.CYAN}[ THREAT INTELLIGENCE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Check for known bad ASNs
            if 'ip-api' in self.geo_data:
                as_data = self.parse_asn(self.geo_data['ip-api'].get('as', ''))
                if as_data and as_data['asn'] in ['4134', '4837', '9808', '17621', '17623']:
                    print(f"\n  {Fore.YELLOW}[!] IP belongs to AS{as_data['asn']} - known for abuse{Style.RESET_ALL}")
                    
            # Proxy/VPN check
            if 'ip-api' in self.geo_data and self.geo_data['ip-api'].get('proxy', False):
                print(f"\n  {Fore.YELLOW}[!] IP is identified as proxy/VPN{Style.RESET_ALL}")
                
            # Hosting check
            if 'ip-api' in self.geo_data and self.geo_data['ip-api'].get('hosting', False):
                print(f"\n  {Fore.CYAN}[i] IP belongs to hosting provider{Style.RESET_ALL}")
                
        # ============ MAP VISUALIZATION ============
        if 'ip-api' in self.geo_data and self.geo_data['ip-api'].get('lat') and self.geo_data['ip-api'].get('lon'):
            print(f"\n{Fore.CYAN}[ MAP VISUALIZATION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            lat = self.geo_data['ip-api']['lat']
            lon = self.geo_data['ip-api']['lon']
            
            # Simple ASCII map
            print(f"\n  {Fore.WHITE}Location: {lat}, {lon}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}View on map: {Fore.CYAN}https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"ip_info_{self.ip}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'ip': self.ip,
            'ip_version': self.ip_version,
            'is_private': self.is_private,
            'is_loopback': self.is_loopback,
            'is_multicast': self.is_multicast,
            'is_global': self.is_global,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'geolocation': self.geo_data,
            'reverse_dns': self.reverse_dns(self.ip)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_lookup(self):
        """Interactive IP information lookup mode"""
        print(f"{Fore.GREEN}[*] IP Information Finder initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced geolocation and network intelligence{Style.RESET_ALL}\n")
        
        # Get target
        print(f"{Fore.CYAN}IP Lookup Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Lookup specific IP address")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Lookup domain/hostname")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Get my public IP")
        print(f"  {Fore.WHITE}[4]{Style.RESET_ALL} Get my local IP")
        
        choice = input(f"\n{Fore.YELLOW}[?] Select option: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            ip_input = input(f"{Fore.YELLOW}[?] Enter IP address: {Style.RESET_ALL}").strip()
        elif choice == "2":
            domain = input(f"{Fore.YELLOW}[?] Enter domain/hostname: {Style.RESET_ALL}").strip()
            ip_input = domain
        elif choice == "3":
            ip_input = "me"
        elif choice == "4":
            local_ip = self.get_local_ip()
            print(f"\n{Fore.GREEN}[✓] Your local IP: {local_ip}{Style.RESET_ALL}")
            return
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        if not ip_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        if not self.validate_ip(ip_input):
            print(f"{Fore.RED}[✗] Invalid IP address or hostname{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.YELLOW}[*] Gathering intelligence for {self.ip}...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Querying geolocation databases...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Get geolocation
        self.get_geolocation(self.ip)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] IP information lookup completed{Style.RESET_ALL}")


def ip_info(ip=None):
    """Main entry point for CLI compatibility"""
    finder = IPInfoFinder()
    
    # Display banner
    finder.print_header()
    
    if ip:
        # Direct lookup mode
        if ip.lower() in ['me', 'myip', 'public']:
            public_ip = finder.get_public_ip()
            if public_ip:
                ip = public_ip
                print(f"{Fore.GREEN}[*] Your public IP: {public_ip}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}[✗] Could not determine public IP{Style.RESET_ALL}")
                return
                
        if not finder.validate_ip(ip):
            print(f"{Fore.RED}[✗] Invalid IP address or hostname{Style.RESET_ALL}")
            return
            
        finder.start_time = datetime.now()
        finder.get_geolocation(finder.ip)
        finder.end_time = datetime.now()
        finder.generate_report()
    else:
        # Interactive mode
        finder.interactive_lookup()


if __name__ == "__main__":
    ip_info()
