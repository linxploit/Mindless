#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: WHOIS INTELLIGENCE
Advanced Domain Registration & Ownership Analysis
Author: ICAT Project | Linxploit.xyz
"""

import whois
import socket
import json
import re
from datetime import datetime
from colorama import Fore, Style, init
import ipaddress

init(autoreset=True)

class WHOISIntelligence:
    """Advanced WHOIS lookup and domain intelligence"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗    ██╗██╗  ██╗ ██████╗ ██╗███████╗    ██╗███╗   ██╗████████╗███████╗██╗     ██╗     ██╗ ██████╗ ███████╗███╗   ██╗ ██████╗███████╗ ║
    ║  ██║    ██║██║  ██║██╔═══██╗██║██╔════╝    ██║████╗  ██║╚══██╔══╝██╔════╝██║     ██║     ██║██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝ ║
    ║  ██║ █╗ ██║███████║██║   ██║██║███████╗    ██║██╔██╗ ██║   ██║   █████╗  ██║     ██║     ██║██║  ███╗█████╗  ██╔██╗ ██║██║     █████╗   ║
    ║  ██║███╗██║██╔══██║██║   ██║██║╚════██║    ██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██║     ██║██║   ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝   ║
    ║  ╚███╔███╔╝██║  ██║╚██████╔╝██║███████║    ██║██║ ╚████║   ██║   ███████╗███████╗███████╗██║╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗ ║
    ║   ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝ ║
    ║                    {Fore.CYAN}WHOIS INTELLIGENCE & DOMAIN FORENSICS v2.0{Fore.RED}         ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Privacy/proxy registrar patterns
    PRIVACY_REGISTRARS = [
        'whoisguard', 'domainsbyproxy', 'perfect privacy', 'privacyprotect',
        'privacy service', 'whois privacy', 'gdpr masked', 'redacted for privacy',
        'registrant email:', 'contact via', 'whoisagent', 'anonymize',
        'knock knock whois not there', 'whoisprotection', 'idprotect',
        'privacyprotect.org', 'whoisprivacyprotect', 'protected',
    ]
    
    # Common domain hacks/takeover indicators
    EXPIRY_RISK_DAYS = 30
    GRACE_PERIOD_DAYS = 45
    
    def __init__(self):
        self.domain = None
        self.whois_data = None
        self.raw_whois = None
        self.parsed_data = {}
        self.risk_factors = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_domain(self, domain):
        """Normalize domain input"""
        domain = domain.strip().lower()
        # Remove protocol if present
        domain = re.sub(r'^https?://', '', domain)
        # Remove path
        domain = domain.split('/')[0]
        # Remove www
        domain = re.sub(r'^www\.', '', domain)
        self.domain = domain
        return domain
        
    def lookup_whois(self, domain):
        """Perform WHOIS lookup"""
        try:
            w = whois.whois(domain)
            self.whois_data = w
            self.raw_whois = w.text if hasattr(w, 'text') else str(w)
            return w
        except Exception as e:
            raise Exception(f"WHOIS lookup failed: {e}")
            
    def parse_whois_data(self):
        """Parse and structure WHOIS data"""
        if not self.whois_data:
            return {}
            
        data = {}
        
        # Domain name
        data['domain_name'] = self._parse_field(self.whois_data.domain_name)
        
        # Registrar
        data['registrar'] = self._parse_field(self.whois_data.registrar)
        data['registrar_url'] = self._parse_field(self.whois_data.registrar_url)
        data['registrar_iana_id'] = self._parse_field(self.whois_data.registrar_iana_id)
        data['registrar_abuse_contact'] = self._parse_field(self.whois_data.registrar_abuse_contact_email)
        
        # Registrant
        data['registrant_name'] = self._parse_field(self.whois_data.name)
        data['registrant_organization'] = self._parse_field(self.whois_data.org)
        data['registrant_email'] = self._parse_field(self.whois_data.email)
        data['registrant_phone'] = self._parse_field(self.whois_data.phone)
        data['registrant_country'] = self._parse_field(self.whois_data.country)
        data['registrant_city'] = self._parse_field(self.whois_data.city)
        data['registrant_state'] = self._parse_field(self.whois_data.state)
        data['registrant_postal'] = self._parse_field(self.whois_data.zipcode)
        data['registrant_address'] = self._parse_field(self.whois_data.address)
        
        # Dates
        data['creation_date'] = self._parse_date(self.whois_data.creation_date)
        data['expiration_date'] = self._parse_date(self.whois_data.expiration_date)
        data['updated_date'] = self._parse_date(self.whois_data.updated_date)
        
        # Name Servers
        data['name_servers'] = self._parse_list(self.whois_data.name_servers)
        
        # Status
        data['status'] = self._parse_list(self.whois_data.status)
        data['dnssec'] = self._parse_field(self.whois_data.dnssec)
        
        # WHOIS Server
        data['whois_server'] = self._parse_field(self.whois_data.whois_server)
        
        self.parsed_data = data
        return data
        
    def _parse_field(self, field):
        """Parse WHOIS field (handle lists and None)"""
        if not field:
            return None
        if isinstance(field, list):
            return field[0] if field else None
        return field
        
    def _parse_list(self, field):
        """Parse WHOIS list field"""
        if not field:
            return []
        if isinstance(field, str):
            return [field]
        return field if isinstance(field, list) else []
        
    def _parse_date(self, date_field):
        """Parse WHOIS date field"""
        if not date_field:
            return None
        if isinstance(date_field, list):
            date_field = date_field[0]
        if isinstance(date_field, datetime):
            return date_field
        try:
            return datetime.strptime(str(date_field), "%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.strptime(str(date_field), "%Y-%m-%d")
            except:
                return str(date_field)
                
    def analyze_risk(self):
        """Analyze domain for risk factors"""
        self.risk_factors = []
        
        # Check domain age
        if self.parsed_data.get('creation_date'):
            age_days = (datetime.now() - self.parsed_data['creation_date']).days
            age_years = age_days / 365
            
            if age_days < 30:
                self.risk_factors.append({
                    'factor': 'Newly Registered Domain',
                    'severity': 'HIGH',
                    'details': f'Domain registered {age_days} days ago',
                    'recommendation': 'High risk for malicious activity'
                })
            elif age_days < 90:
                self.risk_factors.append({
                    'factor': 'Recently Registered Domain',
                    'severity': 'MEDIUM',
                    'details': f'Domain registered {age_days} days ago',
                    'recommendation': 'Verify domain legitimacy'
                })
                
        # Check expiry
        if self.parsed_data.get('expiration_date'):
            days_until_expiry = (self.parsed_data['expiration_date'] - datetime.now()).days
            
            if days_until_expiry < 0:
                self.risk_factors.append({
                    'factor': 'EXPIRED DOMAIN',
                    'severity': 'CRITICAL',
                    'details': f'Domain expired {abs(days_until_expiry)} days ago',
                    'recommendation': 'Immediate renewal required or domain takeover risk'
                })
            elif days_until_expiry < 7:
                self.risk_factors.append({
                    'factor': 'Expiring Imminently',
                    'severity': 'CRITICAL',
                    'details': f'Domain expires in {days_until_expiry} days',
                    'recommendation': 'Renew immediately'
                })
            elif days_until_expiry < 30:
                self.risk_factors.append({
                    'factor': 'Expiring Soon',
                    'severity': 'HIGH',
                    'details': f'Domain expires in {days_until_expiry} days',
                    'recommendation': 'Renew within 30 days'
                })
                
        # Check privacy protection
        if self.parsed_data.get('registrar'):
            registrar_lower = self.parsed_data['registrar'].lower()
            for pattern in self.PRIVACY_REGISTRARS:
                if pattern.lower() in registrar_lower:
                    self.risk_factors.append({
                        'factor': 'Privacy Protection',
                        'severity': 'INFO',
                        'details': f'Registrar uses privacy protection: {self.parsed_data["registrar"]}',
                        'recommendation': 'Owner identity is masked'
                    })
                    break
                    
        # Check for missing registrant info
        if not self.parsed_data.get('registrant_name') and not self.parsed_data.get('registrant_organization'):
            self.risk_factors.append({
                'factor': 'Redacted Registrant',
                'severity': 'INFO',
                'details': 'Registrant information is redacted (GDPR/privacy)',
                'recommendation': 'Common for privacy protection'
            })
            
        # Check DNSSEC
        if not self.parsed_data.get('dnssec') or self.parsed_data['dnssec'] == 'unsigned':
            self.risk_factors.append({
                'factor': 'DNSSEC Not Enabled',
                'severity': 'LOW',
                'details': 'Domain does not have DNSSEC enabled',
                'recommendation': 'Enable DNSSEC for additional security'
            })
            
        # Check name servers
        if not self.parsed_data.get('name_servers'):
            self.risk_factors.append({
                'factor': 'No Name Servers',
                'severity': 'CRITICAL',
                'details': 'No name servers configured',
                'recommendation': 'Domain may be inactive or misconfigured'
            })
            
        return self.risk_factors
        
    def get_registrar_history(self):
        """Extract registrar history from raw WHOIS (simplified)"""
        # This would require historical WHOIS database
        # For now, return current registrar
        if self.parsed_data.get('registrar'):
            return [{
                'registrar': self.parsed_data['registrar'],
                'date': self.parsed_data.get('updated_date', 'Unknown')
            }]
        return []
        
    def generate_report(self):
        """Generate comprehensive WHOIS intelligence report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] WHOIS INTELLIGENCE REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ REGISTRATION DETAILS ============
        print(f"\n{Fore.CYAN}[ REGISTRATION DETAILS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.parsed_data.get('domain_name'):
            print(f"\n  {Fore.WHITE}Domain:{Style.RESET_ALL} {self.parsed_data['domain_name']}")
        if self.parsed_data.get('registrar'):
            print(f"  {Fore.WHITE}Registrar:{Style.RESET_ALL} {self.parsed_data['registrar']}")
        if self.parsed_data.get('registrar_iana_id'):
            print(f"  {Fore.WHITE}IANA ID:{Style.RESET_ALL} {self.parsed_data['registrar_iana_id']}")
        if self.parsed_data.get('whois_server'):
            print(f"  {Fore.WHITE}WHOIS Server:{Style.RESET_ALL} {self.parsed_data['whois_server']}")
            
        # ============ DATES & TIMELINE ============
        print(f"\n{Fore.CYAN}[ DOMAIN TIMELINE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.parsed_data.get('creation_date'):
            created = self.parsed_data['creation_date']
            age_days = (datetime.now() - created).days
            age_years = age_days / 365
            print(f"\n  {Fore.WHITE}Created:{Style.RESET_ALL} {created.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  {Fore.WHITE}Domain Age:{Style.RESET_ALL} {age_days} days ({age_years:.1f} years)")
            
        if self.parsed_data.get('updated_date'):
            updated = self.parsed_data['updated_date']
            if isinstance(updated, datetime):
                print(f"  {Fore.WHITE}Last Updated:{Style.RESET_ALL} {updated.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"  {Fore.WHITE}Last Updated:{Style.RESET_ALL} {updated}")
                
        if self.parsed_data.get('expiration_date'):
            expires = self.parsed_data['expiration_date']
            days_left = (expires - datetime.now()).days
            
            if days_left < 0:
                expiry_color = Fore.RED + Style.BRIGHT
                status = f"EXPIRED ({abs(days_left)} days ago)"
            elif days_left < 7:
                expiry_color = Fore.RED + Style.BRIGHT
                status = f"EXPIRES TODAY" if days_left == 0 else f"EXPIRES IN {days_left} DAYS"
            elif days_left < 30:
                expiry_color = Fore.RED
                status = f"Expiring soon ({days_left} days)"
            elif days_left < 90:
                expiry_color = Fore.YELLOW
                status = f"Expires in {days_left} days"
            else:
                expiry_color = Fore.GREEN
                status = f"Valid ({days_left} days remaining)"
                
            print(f"  {Fore.WHITE}Expires:{Style.RESET_ALL} {expires.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  {Fore.WHITE}Status:{Style.RESET_ALL} {expiry_color}{status}{Style.RESET_ALL}")
            
        # ============ REGISTRANT INFORMATION ============
        print(f"\n{Fore.CYAN}[ REGISTRANT INFORMATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        has_registrant = False
        
        if self.parsed_data.get('registrant_name'):
            print(f"\n  {Fore.WHITE}Name:{Style.RESET_ALL} {self.parsed_data['registrant_name']}")
            has_registrant = True
        if self.parsed_data.get('registrant_organization'):
            print(f"  {Fore.WHITE}Organization:{Style.RESET_ALL} {self.parsed_data['registrant_organization']}")
            has_registrant = True
        if self.parsed_data.get('registrant_email'):
            print(f"  {Fore.WHITE}Email:{Style.RESET_ALL} {self.parsed_data['registrant_email']}")
            has_registrant = True
        if self.parsed_data.get('registrant_phone'):
            print(f"  {Fore.WHITE}Phone:{Style.RESET_ALL} {self.parsed_data['registrant_phone']}")
            has_registrant = True
        if self.parsed_data.get('registrant_country'):
            print(f"  {Fore.WHITE}Country:{Style.RESET_ALL} {self.parsed_data['registrant_country']}")
            has_registrant = True
        if self.parsed_data.get('registrant_city'):
            print(f"  {Fore.WHITE}City:{Style.RESET_ALL} {self.parsed_data['registrant_city']}")
            has_registrant = True
        if self.parsed_data.get('registrant_state'):
            print(f"  {Fore.WHITE}State/Province:{Style.RESET_ALL} {self.parsed_data['registrant_state']}")
            has_registrant = True
        if self.parsed_data.get('registrant_postal'):
            print(f"  {Fore.WHITE}Postal Code:{Style.RESET_ALL} {self.parsed_data['registrant_postal']}")
            has_registrant = True
        if self.parsed_data.get('registrant_address'):
            print(f"  {Fore.WHITE}Address:{Style.RESET_ALL} {self.parsed_data['registrant_address']}")
            has_registrant = True
            
        if not has_registrant:
            print(f"\n  {Fore.YELLOW}[!] Registrant information is redacted or unavailable{Style.RESET_ALL}")
            print(f"      └─ Common due to GDPR and privacy protection")
            
        # ============ NAME SERVERS ============
        if self.parsed_data.get('name_servers'):
            print(f"\n{Fore.CYAN}[ NAME SERVERS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for i, ns in enumerate(self.parsed_data['name_servers'], 1):
                print(f"\n  {i}. {Fore.WHITE}{ns}{Style.RESET_ALL}")
                
        # ============ DOMAIN STATUS ============
        if self.parsed_data.get('status'):
            print(f"\n{Fore.CYAN}[ DOMAIN STATUS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for status in self.parsed_data['status']:
                if 'ok' in status.lower():
                    color = Fore.GREEN
                elif 'pending' in status.lower():
                    color = Fore.YELLOW
                elif 'reserved' in status.lower() or 'hold' in status.lower():
                    color = Fore.RED
                else:
                    color = Fore.WHITE
                    
                print(f"\n  {color}• {status}{Style.RESET_ALL}")
                
        # ============ RISK ANALYSIS ============
        if self.risk_factors:
            print(f"\n{Fore.CYAN}[ RISK ANALYSIS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Sort by severity
            severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
            sorted_risks = sorted(self.risk_factors, key=lambda x: severity_order.get(x['severity'], 5))
            
            for risk in sorted_risks:
                severity = risk['severity']
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
                    
                print(f"\n  {color}[{severity}]{Style.RESET_ALL} {risk['factor']}")
                print(f"      ├─ {Fore.WHITE}{risk['details']}{Style.RESET_ALL}")
                print(f"      └─ {Fore.YELLOW}→ {risk['recommendation']}{Style.RESET_ALL}")
                
        # ============ REGISTRAR CONTACT ============
        if self.parsed_data.get('registrar_abuse_contact'):
            print(f"\n{Fore.CYAN}[ REGISTRAR CONTACT ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.WHITE}Abuse Contact:{Style.RESET_ALL} {self.parsed_data['registrar_abuse_contact']}")
            
        # ============ EXECUTIVE SUMMARY ============
        print(f"\n{Fore.CYAN}[ EXECUTIVE SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        critical_count = len([r for r in self.risk_factors if r['severity'] == 'CRITICAL'])
        high_count = len([r for r in self.risk_factors if r['severity'] == 'HIGH'])
        
        if critical_count > 0:
            print(f"\n  {Fore.RED}{Style.BRIGHT}[!] CRITICAL ISSUES DETECTED{Style.RESET_ALL}")
            print(f"      └─ Immediate action required for {critical_count} issue(s)")
        elif high_count > 0:
            print(f"\n  {Fore.RED}[!] HIGH RISK FACTORS DETECTED{Style.RESET_ALL}")
            print(f"      └─ Investigate {high_count} issue(s) promptly")
        else:
            print(f"\n  {Fore.GREEN}[✓] No critical or high-risk issues detected{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"whois_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'whois_data': self.parsed_data,
            'risk_factors': self.risk_factors,
            'raw_whois': self.raw_whois[:5000] if self.raw_whois else None  # Truncate raw data
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_lookup(self):
        """Interactive WHOIS lookup mode"""
        print(f"{Fore.GREEN}[*] WHOIS Intelligence initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced domain registration forensics{Style.RESET_ALL}\n")
        
        # Get domain
        domain_input = input(f"{Fore.YELLOW}[?] Enter domain to lookup: {Style.RESET_ALL}").strip()
        
        if not domain_input:
            print(f"{Fore.RED}[✗] No domain specified{Style.RESET_ALL}")
            return
            
        self.normalize_domain(domain_input)
        
        print(f"\n{Fore.YELLOW}[*] Querying WHOIS databases for {self.domain}...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take a few seconds...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        try:
            # Perform WHOIS lookup
            self.lookup_whois(self.domain)
            
            # Parse data
            self.parse_whois_data()
            
            # Analyze risks
            self.analyze_risk()
            
        except Exception as e:
            print(f"{Fore.RED}[✗] WHOIS lookup failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] WHOIS intelligence completed{Style.RESET_ALL}")


def whois_lookup(domain=None):
    """Main entry point for CLI compatibility"""
    analyzer = WHOISIntelligence()
    
    # Display banner
    analyzer.print_header()
    
    if domain:
        # Direct lookup mode
        analyzer.normalize_domain(domain)
        analyzer.start_time = datetime.now()
        
        try:
            analyzer.lookup_whois(analyzer.domain)
            analyzer.parse_whois_data()
            analyzer.analyze_risk()
            analyzer.end_time = datetime.now()
            analyzer.generate_report()
        except Exception as e:
            print(f"{Fore.RED}[✗] WHOIS lookup failed: {e}{Style.RESET_ALL}")
    else:
        # Interactive mode
        analyzer.interactive_lookup()


if __name__ == "__main__":
    whois_lookup()
