#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: IP REPUTATION & THREAT INTELLIGENCE
Advanced IP address analysis with multiple threat feeds
Author: ICAT Project | Linxploit.xyz
"""

import requests
import socket
import json
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import ipaddress
import concurrent.futures

init(autoreset=True)

class IPReputationChecker:
    """Advanced IP reputation analysis with multiple threat intelligence sources"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗██████╗     ██████╗ ███████╗██████╗ ██╗   ██╗████████╗    ║
    ║  ██║██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝    ║
    ║  ██║██████╔╝    ██████╔╝█████╗  ██████╔╝██║   ██║   ██║       ║
    ║  ██║██╔═══╝     ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██║       ║
    ║  ██║██║         ██║  ██║███████╗██║  ██║╚██████╔╝   ██║       ║
    ║  ╚═╝╚═╝         ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝       ║
    ║                    {Fore.CYAN}IP REPUTATION CHECKER v2.0{Fore.RED}                 ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Known malicious ASNs (sample - would need regular updates)
    SUSPICIOUS_ASNS = [
        'AS4134', 'AS4837', 'AS9808', 'AS17621', 'AS17623',  # Known proxy ASNs
        'AS9009', 'AS12876', 'AS20473', 'AS16276', 'AS24940',  # VPS providers often abused
    ]
    
    # Blacklisted countries (based on cyber crime rates - configurable)
    HIGH_RISK_COUNTRIES = ['RU', 'CN', 'KP', 'IR', 'SY', 'VE', 'UA']
    MEDIUM_RISK_COUNTRIES = ['BR', 'IN', 'PK', 'NG', 'VN', 'RO', 'ID']
    
    def __init__(self):
        self.ip = None
        self.ip_info = {}
        self.threat_data = {}
        self.reputation_score = 100  # Start at 100 (clean)
        self.risk_factors = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def validate_ip(self, ip):
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
            
    def get_ip_geolocation(self, ip):
        """Get IP geolocation from public APIs"""
        geodata = {}
        
        # Try ip-api.com first (free, no key required)
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    geodata['ip-api'] = {
                        'country': data.get('country'),
                        'countryCode': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp'),
                        'org': data.get('org'),
                        'as': data.get('as'),
                        'mobile': data.get('mobile', False),
                        'proxy': data.get('proxy', False),
                        'hosting': data.get('hosting', False),
                    }
        except:
            pass
            
        # Try ipinfo.io as backup
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geodata['ipinfo'] = {
                    'ip': data.get('ip'),
                    'hostname': data.get('hostname'),
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country': data.get('country'),
                    'loc': data.get('loc'),
                    'org': data.get('org'),
                    'postal': data.get('postal'),
                    'timezone': data.get('timezone'),
                }
        except:
            pass
            
        return geodata
        
    def check_blacklists(self, ip):
        """Check against known blacklists (DNSBL)"""
        blacklists = [
            'zen.spamhaus.org',
            'bl.spamcop.net',
            'cbl.abuseat.org',
            'b.barracudacentral.org',
            'dnsbl.sorbs.net',
        ]
        
        listed_on = []
        
        for bl in blacklists:
            try:
                query = '.'.join(reversed(str(ip).split('.'))) + '.' + bl
                socket.gethostbyname(query)
                listed_on.append(bl)
            except socket.gaierror:
                pass
                
        return listed_on
        
    def analyze_asn(self, asn_info):
        """Analyze ASN for reputation"""
        risk_score = 0
        asn_org = asn_info.get('org', '')
        asn_number = asn_info.get('as', '').split()[0] if asn_info.get('as') else ''
        
        # Check against known suspicious ASNs
        for suspicious_asn in self.SUSPICIOUS_ASNS:
            if suspicious_asn in asn_number or suspicious_asn in asn_org:
                self.risk_factors.append({
                    'factor': 'Suspicious ASN',
                    'details': f'IP belongs to {suspicious_asn} which is commonly abused',
                    'severity': 'HIGH',
                    'score_impact': -30
                })
                risk_score += 30
                break
                
        # Check for hosting/VPS providers
        hosting_keywords = ['hosting', 'vps', 'cloud', 'datacenter', 'server', 'amazon', 'google', 'microsoft']
        for keyword in hosting_keywords:
            if keyword.lower() in asn_org.lower():
                self.risk_factors.append({
                    'factor': 'Hosting/Cloud Provider',
                    'details': f'IP hosted by {asn_org} - commonly used for legitimate sites but also abuse',
                    'severity': 'LOW',
                    'score_impact': -5
                })
                risk_score += 5
                break
                
        return risk_score
        
    def analyze_country_risk(self, country_code):
        """Analyze risk based on country"""
        if not country_code:
            return 0
            
        risk_score = 0
        
        if country_code in self.HIGH_RISK_COUNTRIES:
            self.risk_factors.append({
                'factor': 'High Risk Country',
                'details': f'IP located in {country_code} - elevated cyber crime rates',
                'severity': 'HIGH',
                'score_impact': -25
            })
            risk_score += 25
        elif country_code in self.MEDIUM_RISK_COUNTRIES:
            self.risk_factors.append({
                'factor': 'Medium Risk Country',
                'details': f'IP located in {country_code}',
                'severity': 'MEDIUM',
                'score_impact': -10
            })
            risk_score += 10
            
        return risk_score
        
    def analyze_ip_reputation(self, ip):
        """Comprehensive IP reputation analysis"""
        total_risk = 0
        self.risk_factors = []
        
        # Get geolocation and ISP data
        self.ip_info = self.get_ip_geolocation(ip)
        
        # Check DNS blacklists
        blacklists = self.check_blacklists(ip)
        if blacklists:
            self.risk_factors.append({
                'factor': 'DNS Blacklist',
                'details': f'IP listed on: {", ".join(blacklists)}',
                'severity': 'CRITICAL',
                'score_impact': -50
            })
            total_risk += 50
            
        # Analyze based on ip-api data (more comprehensive)
        if 'ip-api' in self.ip_info:
            ipapi = self.ip_info['ip-api']
            
            # Country risk
            country_code = ipapi.get('countryCode', '')
            total_risk += self.analyze_country_risk(country_code)
            
            # Proxy/VPN detection
            if ipapi.get('proxy', False):
                self.risk_factors.append({
                    'factor': 'Proxy/VPN Detected',
                    'details': 'IP is identified as proxy or VPN service',
                    'severity': 'HIGH',
                    'score_impact': -40
                })
                total_risk += 40
                
            # Hosting detection
            if ipapi.get('hosting', False):
                self.risk_factors.append({
                    'factor': 'Hosting Provider',
                    'details': 'IP belongs to hosting/datacenter',
                    'severity': 'LOW',
                    'score_impact': -10
                })
                total_risk += 10
                
            # Mobile network (generally lower risk for attacks)
            if ipapi.get('mobile', False):
                self.risk_factors.append({
                    'factor': 'Mobile Network',
                    'details': 'IP belongs to mobile carrier network',
                    'severity': 'LOW',
                    'score_impact': 5  # Positive impact
                })
                total_risk -= 5
                
            # ASN analysis
            asn_info = {'as': ipapi.get('as'), 'org': ipapi.get('isp')}
            total_risk += self.analyze_asn(asn_info)
            
        # Calculate final reputation score (0-100, higher is better)
        self.reputation_score = max(0, min(100, 100 - total_risk))
        
        return self.reputation_score
        
    def generate_report(self):
        """Generate comprehensive reputation report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] IP REPUTATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target IP: {Fore.LIGHTGREEN_EX}{self.ip}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ REPUTATION SCORE ============
        print(f"\n{Fore.CYAN}[ REPUTATION SCORE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Visual score bar
        score = self.reputation_score
        bar_length = 40
        filled_length = int(bar_length * score / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if score >= 80:
            score_color = Fore.GREEN
            rating = 'EXCELLENT'
        elif score >= 60:
            score_color = Fore.GREEN
            rating = 'GOOD'
        elif score >= 40:
            score_color = Fore.YELLOW
            rating = 'FAIR'
        elif score >= 20:
            score_color = Fore.RED
            rating = 'POOR'
        else:
            score_color = Fore.RED
            rating = 'MALICIOUS'
            
        print(f"\n  Score: {score_color}{score}/100{Style.RESET_ALL}")
        print(f"  Bar:   {score_color}[{bar}]{Style.RESET_ALL}")
        print(f"  Rating: {score_color}{rating}{Style.RESET_ALL}")
        
        # ============ GEOGRAPHIC LOCATION ============
        print(f"\n{Fore.CYAN}[ GEOGRAPHIC LOCATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if 'ip-api' in self.ip_info:
            data = self.ip_info['ip-api']
            print(f"\n  Country:  {Fore.WHITE}{data.get('country', 'Unknown')} ({data.get('countryCode', '??')}){Style.RESET_ALL}")
            print(f"  Region:   {Fore.WHITE}{data.get('regionName', 'Unknown')}{Style.RESET_ALL}")
            print(f"  City:     {Fore.WHITE}{data.get('city', 'Unknown')}{Style.RESET_ALL}")
            print(f"  ZIP:      {Fore.WHITE}{data.get('zip', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Location: {Fore.WHITE}{data.get('lat', '?')}, {data.get('lon', '?')}{Style.RESET_ALL}")
            print(f"  Timezone: {Fore.WHITE}{data.get('timezone', 'Unknown')}{Style.RESET_ALL}")
        elif 'ipinfo' in self.ip_info:
            data = self.ip_info['ipinfo']
            print(f"\n  IP:       {Fore.WHITE}{data.get('ip', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Hostname: {Fore.WHITE}{data.get('hostname', 'Unknown')}{Style.RESET_ALL}")
            print(f"  City:     {Fore.WHITE}{data.get('city', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Region:   {Fore.WHITE}{data.get('region', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Country:  {Fore.WHITE}{data.get('country', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Location: {Fore.WHITE}{data.get('loc', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Org:      {Fore.WHITE}{data.get('org', 'Unknown')}{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}[!] Geolocation data unavailable{Style.RESET_ALL}")
            
        # ============ NETWORK INFORMATION ============
        print(f"\n{Fore.CYAN}[ NETWORK INFORMATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if 'ip-api' in self.ip_info:
            data = self.ip_info['ip-api']
            print(f"\n  ISP:      {Fore.WHITE}{data.get('isp', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Org:      {Fore.WHITE}{data.get('org', 'Unknown')}{Style.RESET_ALL}")
            print(f"  AS:       {Fore.WHITE}{data.get('as', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Mobile:   {Fore.WHITE}{data.get('mobile', False)}{Style.RESET_ALL}")
            print(f"  Proxy:    {Fore.WHITE}{data.get('proxy', False)}{Style.RESET_ALL}")
            print(f"  Hosting:  {Fore.WHITE}{data.get('hosting', False)}{Style.RESET_ALL}")
            
        # ============ RISK FACTORS ============
        print(f"\n{Fore.CYAN}[ RISK FACTORS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.risk_factors:
            # Sort by severity
            severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            sorted_factors = sorted(self.risk_factors, 
                                   key=lambda x: severity_order.get(x['severity'], 4))
            
            for factor in sorted_factors:
                severity = factor['severity']
                if severity == 'CRITICAL':
                    sev_color = Fore.RED + Style.BRIGHT
                elif severity == 'HIGH':
                    sev_color = Fore.RED
                elif severity == 'MEDIUM':
                    sev_color = Fore.YELLOW
                else:
                    sev_color = Fore.GREEN
                    
                print(f"\n  {sev_color}[{severity}]{Style.RESET_ALL} {factor['factor']}")
                print(f"      └─ {Fore.WHITE}{factor['details']}{Style.RESET_ALL}")
                print(f"      └─ Impact: {sev_color}{factor['score_impact']} points{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.GREEN}[✓] No significant risk factors detected{Style.RESET_ALL}")
            
        # ============ DNS BLACKLIST STATUS ============
        blacklists = self.check_blacklists(self.ip)
        if blacklists:
            print(f"\n{Fore.CYAN}[ DNS BLACKLISTS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.RED}[!] IP is LISTED on {len(blacklists)} blacklist(s):{Style.RESET_ALL}")
            for bl in blacklists:
                print(f"      └─ {Fore.WHITE}{bl}{Style.RESET_ALL}")
                
        # ============ SUMMARY ============
        print(f"\n{Fore.CYAN}[ EXECUTIVE SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.reputation_score >= 80:
            summary = f"{Fore.GREEN}This IP address appears to be CLEAN and has an excellent reputation."
        elif self.reputation_score >= 60:
            summary = f"{Fore.GREEN}This IP address appears to be SAFE with a good reputation."
        elif self.reputation_score >= 40:
            summary = f"{Fore.YELLOW}This IP address has a FAIR reputation but exercise normal caution."
        elif self.reputation_score >= 20:
            summary = f"{Fore.RED}This IP address has a POOR reputation and may be associated with malicious activity."
        else:
            summary = f"{Fore.RED}This IP address has a MALICIOUS reputation and is likely involved in cyber attacks."
            
        print(f"\n  {summary}{Style.RESET_ALL}")
        
        # Recommendations
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.reputation_score < 40:
            print(f"\n  {Fore.RED}[!] BLOCK this IP address immediately{Style.RESET_ALL}")
            print(f"      └─ Add to firewall blacklist")
            print(f"      └─ Monitor for related traffic")
            print(f"      └─ Check logs for previous connections")
        elif self.reputation_score < 60:
            print(f"\n  {Fore.YELLOW}[!] MONITOR this IP address{Style.RESET_ALL}")
            print(f"      └─ Apply rate limiting")
            print(f"      └─ Enable additional logging")
            print(f"      └─ Consider CAPTCHA for suspicious requests")
        else:
            print(f"\n  {Fore.GREEN}[✓] No immediate action required{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"ip_reputation_{self.ip}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'ip': self.ip,
            'timestamp': str(self.start_time),
            'reputation_score': self.reputation_score,
            'geolocation': self.ip_info,
            'risk_factors': self.risk_factors,
            'blacklists': self.check_blacklists(self.ip),
            'summary': {
                'score': self.reputation_score,
                'rating': self.get_rating_from_score(self.reputation_score),
                'risk_level': self.get_risk_level_from_score(self.reputation_score)
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def get_rating_from_score(self, score):
        """Get rating from score"""
        if score >= 80:
            return 'EXCELLENT'
        elif score >= 60:
            return 'GOOD'
        elif score >= 40:
            return 'FAIR'
        elif score >= 20:
            return 'POOR'
        else:
            return 'MALICIOUS'
            
    def get_risk_level_from_score(self, score):
        """Get risk level from score"""
        if score >= 80:
            return 'LOW'
        elif score >= 60:
            return 'LOW-MEDIUM'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'HIGH'
        else:
            return 'CRITICAL'
            
    def interactive_scan(self):
        """Interactive reputation analysis"""
        print(f"{Fore.GREEN}[*] IP Reputation Checker initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multi-source threat intelligence analysis{Style.RESET_ALL}\n")
        
        # Get target
        ip_input = input(f"{Fore.YELLOW}[?] Enter IP address: {Style.RESET_ALL}").strip()
        
        if not ip_input:
            print(f"{Fore.RED}[✗] No IP specified{Style.RESET_ALL}")
            return
            
        if not self.validate_ip(ip_input):
            print(f"{Fore.RED}[✗] Invalid IP address format: {ip_input}{Style.RESET_ALL}")
            return
            
        self.ip = ip_input
        
        print(f"\n{Fore.YELLOW}[*] Analyzing IP reputation for {self.ip}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Checking multiple threat intelligence sources...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Perform reputation analysis
        try:
            self.analyze_ip_reputation(self.ip)
        except Exception as e:
            print(f"{Fore.RED}[✗] Analysis failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] IP reputation analysis completed{Style.RESET_ALL}")


def check_ip_reputation(ip=None):
    """Main entry point for CLI compatibility"""
    checker = IPReputationChecker()
    
    # Display banner
    checker.print_header()
    
    if ip:
        # Direct scan mode
        if not checker.validate_ip(ip):
            print(f"{Fore.RED}[✗] Invalid IP address format: {ip}{Style.RESET_ALL}")
            return
            
        checker.ip = ip
        checker.start_time = datetime.now()
        
        try:
            checker.analyze_ip_reputation(ip)
        except Exception as e:
            print(f"{Fore.RED}[✗] Analysis failed: {e}{Style.RESET_ALL}")
            return
            
        checker.end_time = datetime.now()
        checker.generate_report()
    else:
        # Interactive mode
        checker.interactive_scan()


if __name__ == "__main__":
    check_ip_reputation()
