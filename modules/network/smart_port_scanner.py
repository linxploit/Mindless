#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: SMART PORT SCANNER
Professional Network Reconnaissance Tool
Author: ICAT Project | Linxploit.xyz
"""

import socket
import threading
import sys
import time
from queue import Queue
from datetime import datetime
from colorama import Fore, Style, init
import ipaddress
import argparse

init(autoreset=True)

class SmartPortScanner:
    """Advanced multi-threaded port scanner with service detection"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███╗   ███╗██╗███╗   ██╗██████╗ ██╗     ███████╗███████╗███████╗  ║
    ║  ████╗ ████║██║████╗  ██║██╔══██╗██║     ██╔════╝██╔════╝██╔════╝  ║
    ║  ██╔████╔██║██║██╔██╗ ██║██║  ██║██║     █████╗  ███████╗███████╗  ║
    ║  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║██║     ██╔══╝  ╚════██║╚════██║  ║
    ║  ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝███████╗███████╗███████║███████║  ║
    ║  ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝  ║
    ║                    {Fore.CYAN}SMART PORT SCANNER v2.0{Fore.RED}                      ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Extended port database with service signatures
    PORT_SERVICES = {
        20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
        53: "DNS", 69: "TFTP", 80: "HTTP", 81: "HTTP-ALT", 88: "KERBEROS",
        110: "POP3", 111: "RPCBIND", 135: "MSRPC", 139: "NETBIOS-SSN",
        143: "IMAP", 161: "SNMP", 162: "SNMP-TRAP", 389: "LDAP",
        443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "SYSLOG",
        587: "SMTP-SUB", 593: "HTTP-RPC", 636: "LDAPS", 873: "RSYNC",
        993: "IMAPS", 995: "POP3S", 1080: "SOCKS", 1194: "OPENVPN",
        1337: "WASTE", 1433: "MSSQL", 1434: "MSSQL-UDP", 1521: "ORACLE",
        1723: "PPTP", 2049: "NFS", 2082: "CPANEL", 2083: "CPANEL-SSL",
        2086: "WHM", 2087: "WHM-SSL", 2095: "CPANEL-WEB", 2096: "CPANEL-WEB-SSL",
        2222: "SSH-ALT", 2375: "DOCKER", 2376: "DOCKER-SSL", 3128: "SQUID",
        3306: "MYSQL", 3389: "RDP", 3690: "SVN", 4444: "METASPLOIT",
        4848: "GLASSFISH", 5000: "UPNP", 5432: "POSTGRESQL", 5555: "ADB",
        5632: "PCANYWHERE", 5800: "VNC-HTTP", 5900: "VNC", 5984: "COUCHDB",
        5985: "WINRM", 5986: "WINRM-SSL", 6379: "REDIS", 6660: "IRC",
        6661: "IRC", 6662: "IRC", 6663: "IRC", 6664: "IRC", 6665: "IRC",
        6666: "IRC", 6667: "IRC", 6668: "IRC", 6669: "IRC", 6679: "IRC-SSL",
        6697: "IRC-SSL", 7001: "WEBLOGIC", 7002: "WEBLOGIC-SSL",
        7070: "REAL-SERVER", 8000: "HTTP-ALT", 8008: "HTTP-ALT", 8009: "AJP",
        8080: "HTTP-PROXY", 8081: "HTTP-ALT", 8086: "INFLUXDB", 8088: "HTTP-ALT",
        8089: "SPLUNKD", 8090: "HTTP-ALT", 8181: "GLASSFISH-ADMIN", 8443: "HTTPS-ALT",
        8888: "HTTP-ALT", 9000: "SONARQUBE", 9001: "TOR", 9042: "CASSANDRA",
        9092: "KAFKA", 9100: "JETDIRECT", 9200: "ELASTICSEARCH", 9300: "ELASTICSEARCH",
        9418: "GIT", 9999: "HTTP-ALT", 10000: "WEBMIN", 11211: "MEMCACHED",
        27017: "MONGODB", 27018: "MONGODB", 28017: "MONGODB-STATS", 50000: "SAP",
        50030: "HADOOP", 50060: "HADOOP", 50070: "HDFS", 50075: "HDFS",
    }
    
    # Service signature patterns for banner grabbing
    SERVICE_SIGNATURES = {
        b"SSH": "SSH",
        b"220": "FTP",
        b"HTTP/": "HTTP",
        b"SMTP": "SMTP",
        b"POP3": "POP3",
        b"IMAP": "IMAP",
        b"MySQL": "MySQL",
        b"PostgreSQL": "PostgreSQL",
        b"MongoDB": "MongoDB",
        b"Redis": "Redis",
        b"Apache": "Apache",
        b"nginx": "NGINX",
        b"IIS": "IIS",
        b"Microsoft-IIS": "IIS",
        b"220-": "FTP",
    }

    def __init__(self):
        self.open_ports = []
        self.lock = threading.Lock()
        self.queue = Queue()
        self.results = []
        self.start_time = None
        self.end_time = None
        self.target_ip = None
        self.target_host = None
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def resolve_target(self, target):
        """Resolve hostname to IP with timeout"""
        try:
            self.target_host = target
            self.target_ip = socket.gethostbyname(target)
            return True
        except socket.gaierror:
            return False
            
    def grab_banner(self, sock, port):
        """Advanced banner grabbing with multiple probes"""
        try:
            # Send common probes based on port
            probes = [
                b"\r\n",
                b"HEAD / HTTP/1.0\r\n\r\n",
                b"GET / HTTP/1.0\r\n\r\n",
                b"HELP\r\n",
                b"STATUS\r\n",
                b"QUIT\r\n",
                b"\x00",
            ]
            
            for probe in probes:
                try:
                    sock.send(probe)
                    banner = sock.recv(1024).decode(errors='ignore').strip()
                    if banner:
                        # Identify service from banner
                        for sig, service in self.SERVICE_SIGNATURES.items():
                            if sig.lower() in banner.lower() or sig in banner.encode():
                                return banner[:100], service
                        return banner[:100], self.PORT_SERVICES.get(port, "Unknown")
                except:
                    continue
                    
            return "", self.PORT_SERVICES.get(port, "Unknown")
            
        except Exception:
            return "", self.PORT_SERVICES.get(port, "Unknown")
            
    def scan_port(self, port, timeout=0.8):
        """Scan single port with service detection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:
                banner, service = self.grab_banner(sock, port)
                
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'service': service,
                        'banner': banner,
                        'state': 'open'
                    })
                    
                    # Colored output with formatting
                    port_str = f"{port:5d}"
                    service_str = f"{service:15s}"
                    
                    if port in [21, 22, 23, 25, 110, 143, 443, 993, 995, 3389, 5900, 5901]:
                        status_color = Fore.RED
                    elif port in [80, 8080, 8443, 8000, 8888]:
                        status_color = Fore.YELLOW
                    else:
                        status_color = Fore.GREEN
                        
                    print(f"{status_color}  [>] PORT {port_str} | {service_str} | OPEN{Style.RESET_ALL}")
                    
                    if banner:
                        print(f"{Fore.CYAN}      └─ Banner: {banner[:80]}{'...' if len(banner) > 80 else ''}{Style.RESET_ALL}")
                        
            sock.close()
            
        except Exception:
            pass
            
    def worker(self, timeout):
        """Thread worker function"""
        while not self.queue.empty():
            port = self.queue.get()
            self.scan_port(port, timeout)
            self.queue.task_done()
            
    def scan_range(self, start_port=1, end_port=1024, threads=100, timeout=0.8):
        """Scan port range with threading"""
        self.open_ports = []
        self.queue = Queue()
        
        # Add ports to queue
        for port in range(start_port, end_port + 1):
            self.queue.put(port)
            
        # Create thread pool
        thread_list = []
        for _ in range(min(threads, end_port - start_port + 1)):
            t = threading.Thread(target=self.worker, args=(timeout,))
            t.daemon = True
            t.start()
            thread_list.append(t)
            
        # Wait for all threads
        for t in thread_list:
            try:
                t.join(timeout + 1)
            except:
                pass
                
        self.queue.join()
        
    def scan_common_ports(self, threads=50, timeout=0.6):
        """Scan only common ports for speed"""
        common_ports = list(self.PORT_SERVICES.keys())[:100]
        
        for port in common_ports:
            self.queue.put(port)
            
        thread_list = []
        for _ in range(min(threads, len(common_ports))):
            t = threading.Thread(target=self.worker, args=(timeout,))
            t.daemon = True
            t.start()
            thread_list.append(t)
            
        for t in thread_list:
            try:
                t.join(timeout + 1)
            except:
                pass
                
        self.queue.join()
        
    def scan_top_ports(self, threads=100, timeout=0.8):
        """Scan top 1000 most common ports"""
        top_ports = [
            21,22,23,25,53,80,81,110,111,135,139,143,443,445,993,995,
            1723,3306,3389,5900,8080,8443,8888,10000,32768,49152,49154,
            49155,49156,49157,49158,49159,49160,49161,49162,49163,49165,
            49171,49172,49175,49176,49177,49181,49182,49183,49184,49185,
            49186,49187,49188,49189,49190,49191,49192,49193,49194,49195,
            49196,49197,49198,49199,49200,49201,49202,49203,49204,49205,
            49206,49207,49208,49209,49210,49211,49212,49213,49214,49215,
            49216,49217,49218,49219,49220,49221,49222,49223,49224,49225,
            49226,49227,49228,49229,49230,49231,49232,49233,49234,49235,
            49236,49237,49238,49239,49240,49241,49242,49243,49244,49245,
            49246,49247,49248,49249,49250,49251,49252,49253,49254,49255,
            49256,49257,49258,49259,49260,49261,49262,49263,49264,49265,
            49266,49267,49268,49269,49270,49271,49272,49273,49274,49275,
            49276,49277,49278,49279,49280,49281,49282,49283,49284,49285,
            49286,49287,49288,49289,49290,49291,49292,49293,49294,49295,
            49296,49297,49298,49299,49300,49301,49302,49303,49304,49305,
            49306,49307,49308,49309,49310,49311,49312,49313,49314,49315,
            49316,49317,49318,49319,49320,49321,49322,49323,49324,49325,
            49326,49327,49328,49329,49330,49331,49332,49333,49334,49335,
            49336,49337,49338,49339,49340,49341,49342,49343,49344,49345,
            49346,49347,49348,49349,49350,49351,49352,49353,49354,49355,
            49356,49357,49358,49359,49360,49361,49362,49363,49364,49365,
            49366,49367,49368,49369,49370,49371,49372,49373,49374,49375,
            49376,49377,49378,49379,49380,49381,49382,49383,49384,49385,
            49386,49387,49388,49389,49390,49391,49392,49393,49394,49395,
            49396,49397,49398,49399,49400
        ]
        
        for port in top_ports[:1000]:
            self.queue.put(port)
            
        thread_list = []
        for _ in range(min(threads, len(top_ports))):
            t = threading.Thread(target=self.worker, args=(timeout,))
            t.daemon = True
            t.start()
            thread_list.append(t)
            
        for t in thread_list:
            try:
                t.join(timeout + 1)
            except:
                pass
                
        self.queue.join()
        
    def generate_report(self):
        """Generate detailed scan report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] SCAN REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target: {Fore.LIGHTGREEN_EX}{self.target_host} ({self.target_ip}){Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Open Ports Found: {Fore.LIGHTGREEN_EX}{len(self.open_ports)}{Style.RESET_ALL}")
        
        if self.open_ports:
            print(f"\n{Fore.CYAN}OPEN PORTS:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  PORT     SERVICE         BANNER{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  ----     -------         ------\n{Style.RESET_ALL}")
            
            for p in sorted(self.open_ports, key=lambda x: x['port']):
                banner_preview = p['banner'][:50].replace('\n', ' ').replace('\r', '') if p['banner'] else 'No banner'
                print(f"  {p['port']:<8} {p['service']:<15} {Fore.WHITE}{banner_preview}{'...' if len(p['banner']) > 50 else ''}{Style.RESET_ALL}")
                
            # Service summary
            print(f"\n{Fore.CYAN}SERVICE SUMMARY:{Style.RESET_ALL}")
            service_counts = {}
            for p in self.open_ports:
                service_counts[p['service']] = service_counts.get(p['service'], 0) + 1
                
            for service, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True):
                if service != "Unknown":
                    print(f"  {Fore.GREEN}[+]{Style.RESET_ALL} {service}: {count} port(s)")
                    
            # Security recommendations
            print(f"\n{Fore.YELLOW}SECURITY NOTES:{Style.RESET_ALL}")
            vulnerable_ports = {
                21: "FTP - Cleartext credentials, consider SFTP/FTPS",
                23: "Telnet - Unencrypted, use SSH instead",
                25: "SMTP - Check for open relay",
                110: "POP3 - Cleartext, use POP3S",
                143: "IMAP - Cleartext, use IMAPS",
                445: "SMB - Potential EternalBlue vector",
                3389: "RDP - Ensure NLA is enabled",
                5900: "VNC - Check authentication",
            }
            
            for p in self.open_ports:
                if p['port'] in vulnerable_ports:
                    print(f"  {Fore.RED}[!]{Style.RESET_ALL} Port {p['port']}: {vulnerable_ports[p['port']]}")
                    
        else:
            print(f"\n{Fore.RED}  [!] No open ports detected{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_json(self, filename=None):
        """Export results to JSON"""
        import json
        if not filename:
            filename = f"scan_{self.target_ip}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.target_host,
            'target_ip': self.target_ip,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'open_ports': self.open_ports,
            'total_open': len(self.open_ports)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive scanning mode"""
        print(f"{Fore.GREEN}[*] Smart Port Scanner initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multi-threaded TCP connect scan with service detection{Style.RESET_ALL}\n")
        
        # Get target
        target = input(f"{Fore.YELLOW}[?] Enter target (IP/hostname): {Style.RESET_ALL}").strip()
        
        if not target:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        if not self.resolve_target(target):
            print(f"{Fore.RED}[✗] Could not resolve target: {target}{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}[✓] Target resolved: {self.target_ip}{Style.RESET_ALL}\n")
        
        # Scan options
        print(f"{Fore.CYAN}Scan Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Common ports (fast)")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Full range (1-1024)")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Custom range")
        print(f"  {Fore.WHITE}[4]{Style.RESET_ALL} Top 1000 ports")
        
        scan_choice = input(f"\n{Fore.YELLOW}[?] Select scan type: {Style.RESET_ALL}").strip()
        
        # Thread configuration
        try:
            threads = int(input(f"{Fore.YELLOW}[?] Threads (default 100): {Style.RESET_ALL}").strip() or "100")
            timeout = float(input(f"{Fore.YELLOW}[?] Timeout (default 0.8s): {Style.RESET_ALL}").strip() or "0.8")
        except ValueError:
            print(f"{Fore.RED}[✗] Invalid input, using defaults{Style.RESET_ALL}")
            threads = 100
            timeout = 0.8
            
        self.start_time = datetime.now()
        print(f"\n{Fore.YELLOW}[*] Starting scan at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Target: {self.target_host} ({self.target_ip}){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Threads: {threads} | Timeout: {timeout}s{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}\n")
        
        try:
            if scan_choice == "1":
                self.scan_common_ports(threads, timeout)
            elif scan_choice == "2":
                self.scan_range(1, 1024, threads, timeout)
            elif scan_choice == "3":
                start = int(input(f"{Fore.YELLOW}[?] Start port: {Style.RESET_ALL}").strip())
                end = int(input(f"{Fore.YELLOW}[?] End port: {Style.RESET_ALL}").strip())
                self.scan_range(start, end, threads, timeout)
            elif scan_choice == "4":
                self.scan_top_ports(threads, timeout)
            else:
                print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
                return
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
            return
        except Exception as e:
            print(f"{Fore.RED}[✗] Scan failed: {e}{Style.RESET_ALL}")
            return
            
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_json()
            
        print(f"\n{Fore.GREEN}[✓] Scan completed successfully{Style.RESET_ALL}")


def smart_port_scan(target=None):
    """Main entry point for CLI compatibility"""
    scanner = SmartPortScanner()
    
    # Display banner
    scanner.print_header()
    
    if target:
        # Direct scan mode
        if not scanner.resolve_target(target):
            print(f"{Fore.RED}[✗] Could not resolve target: {target}{Style.RESET_ALL}")
            return
            
        scanner.start_time = datetime.now()
        print(f"\n{Fore.YELLOW}[*] Starting scan on {scanner.target_ip}{Style.RESET_ALL}")
        
        scanner.scan_common_ports(threads=100, timeout=0.8)
        
        scanner.end_time = datetime.now()
        scanner.generate_report()
    else:
        # Interactive mode
        scanner.interactive_scan()


if __name__ == "__main__":
    smart_port_scan()
