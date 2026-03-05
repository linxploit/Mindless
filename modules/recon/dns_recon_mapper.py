#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: DNS RECON MAPPER
Advanced DNS Enumeration & Zone Analysis
Author: ICAT Project | Linxploit.xyz
"""

import dns.resolver
import dns.zone
import dns.query
import dns.reversename
import socket
import json
from datetime import datetime
from colorama import Fore, Style, init
import concurrent.futures
import re

init(autoreset=True)

class DNSReconMapper:
    """Advanced DNS reconnaissance and mapping tool"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ███╗   ██╗███████╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗    ║
    ║  ██╔══██╗████╗  ██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║    ║
    ║  ██║  ██║██╔██╗ ██║███████╗    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║    ║
    ║  ██║  ██║██║╚██╗██║╚════██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║    ║
    ║  ██████╔╝██║ ╚████║███████║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║    ║
    ║  ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝    ║
    ║                    {Fore.CYAN}DNS RECONNAISSANCE & ZONE MAPPING v2.0{Fore.RED}     ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # DNS record types to query
    RECORD_TYPES = [
        'A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR',
        'SRV', 'CAA', 'NAPTR', 'DS', 'DNSKEY', 'TLSA'
    ]
    
    # Common SRV services
    SRV_SERVICES = [
        '_http._tcp', '_https._tcp', '_ldap._tcp', '_kerberos._tcp',
        '_sip._tcp', '_xmpp._tcp', '_imap._tcp', '_pop3._tcp',
        '_smtp._tcp', '_ftp._tcp', '_ssh._tcp', '_telnet._tcp',
    ]
    
    def __init__(self):
        self.domain = None
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
        self.records = {}
        self.nameservers = []
        self.zone_transfer_possible = False
        self.zone_data = None
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
        domain = re.sub(r'^https?://', '', domain)
        domain = domain.split('/')[0]
        domain = re.sub(r'^www\.', '', domain)
        self.domain = domain
        return domain
        
    def query_record(self, record_type):
        """Query specific DNS record type"""
        results = []
        
        try:
            answers = self.resolver.resolve(self.domain, record_type)
            
            for rdata in answers:
                result = {
                    'type': record_type,
                    'ttl': answers.response.answer[0].ttl if answers.response.answer else None,
                }
                
                # Format based on record type
                if record_type in ['A', 'AAAA']:
                    result['value'] = str(rdata)
                elif record_type == 'MX':
                    result['preference'] = rdata.preference
                    result['exchange'] = str(rdata.exchange).rstrip('.')
                elif record_type == 'NS':
                    result['nameserver'] = str(rdata).rstrip('.')
                elif record_type == 'TXT':
                    result['text'] = str(rdata).strip('"')
                elif record_type == 'SOA':
                    result['mname'] = str(rdata.mname).rstrip('.')
                    result['rname'] = str(rdata.rname).rstrip('.')
                    result['serial'] = rdata.serial
                    result['refresh'] = rdata.refresh
                    result['retry'] = rdata.retry
                    result['expire'] = rdata.expire
                    result['minimum'] = rdata.minimum
                elif record_type == 'CNAME':
                    result['target'] = str(rdata.target).rstrip('.')
                elif record_type == 'PTR':
                    result['pointer'] = str(rdata).rstrip('.')
                elif record_type == 'SRV':
                    result['priority'] = rdata.priority
                    result['weight'] = rdata.weight
                    result['port'] = rdata.port
                    result['target'] = str(rdata.target).rstrip('.')
                elif record_type == 'CAA':
                    result['flags'] = rdata.flags
                    result['tag'] = rdata.tag.decode()
                    result['value'] = rdata.value.decode()
                elif record_type in ['DS', 'DNSKEY', 'TLSA']:
                    result['value'] = str(rdata)
                else:
                    result['value'] = str(rdata)
                    
                results.append(result)
                
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            raise Exception(f"Domain {self.domain} does not exist")
        except dns.exception.Timeout:
            pass
        except Exception as e:
            pass
            
        return results
        
    def query_srv_records(self):
        """Query common SRV records"""
        srv_records = []
        
        for service in self.SRV_SERVICES:
            try:
                srv_domain = f"{service}.{self.domain}"
                answers = self.resolver.resolve(srv_domain, 'SRV')
                
                for rdata in answers:
                    srv_records.append({
                        'service': service,
                        'priority': rdata.priority,
                        'weight': rdata.weight,
                        'port': rdata.port,
                        'target': str(rdata.target).rstrip('.')
                    })
            except:
                pass
                
        return srv_records
        
    def get_nameservers(self):
        """Get authoritative nameservers for domain"""
        try:
            answers = self.resolver.resolve(self.domain, 'NS')
            self.nameservers = [str(rdata).rstrip('.') for rdata in answers]
            return self.nameservers
        except:
            return []
            
    def attempt_zone_transfer(self, nameserver):
        """Attempt DNS zone transfer"""
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, self.domain, timeout=5))
            if zone:
                self.zone_transfer_possible = True
                return zone
        except:
            pass
        return None
        
    def check_all_nameservers_zone_transfer(self):
        """Check all nameservers for zone transfer vulnerability"""
        zones = {}
        
        for ns in self.nameservers:
            try:
                ns_ip = socket.gethostbyname(ns)
                zone = self.attempt_zone_transfer(ns_ip)
                if zone:
                    zones[ns] = zone
            except:
                pass
                
        if zones:
            self.zone_data = zones
            self.zone_transfer_possible = True
            
        return zones
        
    def reverse_lookup(self, ip_range=None):
        """Perform reverse DNS lookup on IP range"""
        results = []
        
        if ip_range:
            try:
                # Parse IP range
                import ipaddress
                network = ipaddress.ip_network(ip_range, strict=False)
                
                for ip in network.hosts():
                    try:
                        rev_name = dns.reversename.from_address(str(ip))
                        answers = self.resolver.resolve(rev_name, 'PTR')
                        for rdata in answers:
                            results.append({
                                'ip': str(ip),
                                'ptr': str(rdata).rstrip('.')
                            })
                    except:
                        pass
            except:
                pass
                
        return results
        
    def enumerate_all(self):
        """Enumerate all DNS record types"""
        self.records = {}
        
        print(f"{Fore.CYAN}[*] Querying {len(self.RECORD_TYPES)} DNS record types...{Style.RESET_ALL}")
        
        for record_type in self.RECORD_TYPES:
            results = self.query_record(record_type)
            if results:
                self.records[record_type] = results
                print(f"{Fore.GREEN}[✓] Found {len(results)} {record_type} record(s){Style.RESET_ALL}")
                
        # Query SRV records
        srv_results = self.query_srv_records()
        if srv_results:
            self.records['SRV (Common)'] = srv_results
            print(f"{Fore.GREEN}[✓] Found {len(srv_results)} common SRV record(s){Style.RESET_ALL}")
            
        # Get nameservers
        self.get_nameservers()
        
        return self.records
        
    def generate_report(self):
        """Generate comprehensive DNS recon report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] DNS RECONNAISSANCE REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ RECORD SUMMARY ============
        print(f"\n{Fore.CYAN}[ RECORD SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.records:
            print(f"\n  {Fore.WHITE}Record Types Found: {len(self.records)}{Style.RESET_ALL}")
            
            for record_type, records in self.records.items():
                print(f"\n  {Fore.YELLOW}• {record_type}:{Style.RESET_ALL} {len(records)} record(s)")
        else:
            print(f"\n  {Fore.RED}[!] No DNS records found{Style.RESET_ALL}")
            
        # ============ DETAILED RECORDS ============
        for record_type, records in self.records.items():
            print(f"\n{Fore.CYAN}[ {record_type} RECORDS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for i, record in enumerate(records, 1):
                if record_type == 'A' or record_type == 'AAAA':
                    print(f"\n  {i}. {Fore.WHITE}{record['value']}{Style.RESET_ALL}")
                    if 'ttl' in record:
                        print(f"      └─ TTL: {record['ttl']}s")
                        
                elif record_type == 'MX':
                    print(f"\n  {i}. {Fore.WHITE}Priority {record['preference']}: {record['exchange']}{Style.RESET_ALL}")
                    
                elif record_type == 'NS':
                    print(f"\n  {i}. {Fore.WHITE}{record['nameserver']}{Style.RESET_ALL}")
                    
                elif record_type == 'TXT':
                    text = record['text']
                    if len(text) > 80:
                        text = text[:80] + '...'
                    print(f"\n  {i}. {Fore.WHITE}{text}{Style.RESET_ALL}")
                    
                elif record_type == 'SOA':
                    print(f"\n  {i}. {Fore.WHITE}Primary NS: {record['mname']}{Style.RESET_ALL}")
                    print(f"      ├─ Hostmaster: {record['rname']}")
                    print(f"      ├─ Serial: {record['serial']}")
                    print(f"      ├─ Refresh: {record['refresh']}s")
                    print(f"      ├─ Retry: {record['retry']}s")
                    print(f"      ├─ Expire: {record['expire']}s")
                    print(f"      └─ Minimum TTL: {record['minimum']}s")
                    
                elif record_type == 'CNAME':
                    print(f"\n  {i}. {Fore.WHITE}{record['target']}{Style.RESET_ALL}")
                    
                elif record_type == 'SRV' or record_type == 'SRV (Common)':
                    print(f"\n  {i}. {Fore.WHITE}{record.get('service', 'SRV')}{Style.RESET_ALL}")
                    print(f"      ├─ Target: {record['target']}")
                    print(f"      ├─ Port: {record['port']}")
                    print(f"      ├─ Priority: {record['priority']}")
                    print(f"      └─ Weight: {record['weight']}")
                    
                elif record_type == 'CAA':
                    print(f"\n  {i}. {Fore.WHITE}{record['tag']}={record['value']}{Style.RESET_ALL}")
                    print(f"      └─ Flags: {record['flags']}")
                    
                else:
                    print(f"\n  {i}. {Fore.WHITE}{record.get('value', str(record))}{Style.RESET_ALL}")
                    
        # ============ NAMESERVERS ============
        if self.nameservers:
            print(f"\n{Fore.CYAN}[ AUTHORITATIVE NAMESERVERS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            for i, ns in enumerate(self.nameservers, 1):
                print(f"\n  {i}. {Fore.WHITE}{ns}{Style.RESET_ALL}")
                
                # Resolve NS IP
                try:
                    ns_ip = socket.gethostbyname(ns)
                    print(f"      └─ IP: {ns_ip}")
                except:
                    pass
                    
        # ============ ZONE TRANSFER ============
        print(f"\n{Fore.CYAN}[ ZONE TRANSFER CHECK ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.zone_transfer_possible and self.zone_data:
            print(f"\n  {Fore.RED}{Style.BRIGHT}[!] ZONE TRANSFER VULNERABLE!{Style.RESET_ALL}")
            print(f"      └─ Successful on {len(self.zone_data)} nameserver(s)")
            
            for ns, zone in self.zone_data.items():
                print(f"\n      {Fore.YELLOW}→ {ns}:{Style.RESET_ALL}")
                count = 0
                for name, node in zone.nodes.items():
                    if count < 20:  # Limit output
                        rdataset = node.rdatasets[0] if node.rdatasets else None
                        if rdataset:
                            print(f"          {name} → {rdataset}")
                            count += 1
                if count >= 20:
                    print(f"          ... and more records")
        else:
            print(f"\n  {Fore.GREEN}[✓] Zone transfer not permitted{Style.RESET_ALL}")
            print(f"      └─ Nameservers properly configured")
            
        # ============ RECOMMENDATIONS ============
        print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if self.zone_transfer_possible:
            print(f"\n  {Fore.RED}• Disable zone transfers for all nameservers{Style.RESET_ALL}")
            
        if 'TXT' not in self.records:
            print(f"\n  {Fore.YELLOW}• Consider adding SPF/DKIM/DMARC TXT records for email security{Style.RESET_ALL}")
            
        if 'CAA' not in self.records:
            print(f"\n  {Fore.YELLOW}• Consider adding CAA records to restrict SSL certificate issuance{Style.RESET_ALL}")
            
        if 'DS' not in self.records:
            print(f"\n  {Fore.YELLOW}• Consider enabling DNSSEC and adding DS records{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"dns_recon_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'records': self.records,
            'nameservers': self.nameservers,
            'zone_transfer_possible': self.zone_transfer_possible
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive DNS reconnaissance mode"""
        print(f"{Fore.GREEN}[*] DNS Recon Mapper initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced DNS enumeration & zone analysis{Style.RESET_ALL}\n")
        
        # Get domain
        domain_input = input(f"{Fore.YELLOW}[?] Enter domain to scan: {Style.RESET_ALL}").strip()
        
        if not domain_input:
            print(f"{Fore.RED}[✗] No domain specified{Style.RESET_ALL}")
            return
            
        self.normalize_domain(domain_input)
        
        print(f"\n{Fore.YELLOW}[*] Starting DNS reconnaissance on {self.domain}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Querying {len(self.RECORD_TYPES)} record types...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        try:
            # Enumerate all records
            self.enumerate_all()
            
            # Check zone transfer
            if self.nameservers:
                print(f"\n{Fore.CYAN}[*] Checking zone transfer vulnerability...{Style.RESET_ALL}")
                self.check_all_nameservers_zone_transfer()
                
        except Exception as e:
            print(f"{Fore.RED}[✗] DNS recon failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] DNS reconnaissance completed{Style.RESET_ALL}")


def dns_recon(domain=None):
    """Main entry point for CLI compatibility"""
    mapper = DNSReconMapper()
    
    # Display banner
    mapper.print_header()
    
    if domain:
        # Direct scan mode
        mapper.normalize_domain(domain)
        mapper.start_time = datetime.now()
        
        print(f"\n  {Fore.YELLOW}[*] Starting DNS reconnaissance on {domain}...{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] Querying 14+ DNS record types{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] This may take 10-20 seconds{Style.RESET_ALL}\n")
        
        try:
            mapper.enumerate_all()
            if mapper.nameservers:
                mapper.check_all_nameservers_zone_transfer()
            mapper.end_time = datetime.now()
            mapper.generate_report()
        except Exception as e:
            print(f"{Fore.RED}[✗] DNS recon failed: {e}{Style.RESET_ALL}")
    else:
        # Interactive mode
        mapper.interactive_scan()


if __name__ == "__main__":
    dns_recon()