#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: LIVE HOST DISCOVERY
Advanced Network Sweeper & Host Detection
Author: ICAT Project | Linxploit.xyz
"""

import socket
import subprocess
import platform
import threading
import ipaddress
import time
from queue import Queue
from datetime import datetime
from colorama import Fore, Style, init
import concurrent.futures
import sys
import os

init(autoreset=True)

class LiveHostDiscovery:
    """Advanced live host discovery with multiple detection methods"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗     ██╗██╗   ██╗███████╗    ██╗  ██╗ ██████╗ ███████╗████████╗  ║
    ║  ██║     ██║██║   ██║██╔════╝    ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝  ║
    ║  ██║     ██║██║   ██║█████╗      ███████║██║   ██║███████╗   ██║     ║
    ║  ██║     ██║╚██╗ ██╔╝██╔══╝      ██╔══██║██║   ██║╚════██║   ██║     ║
    ║  ███████╗██║ ╚████╔╝ ███████╗    ██║  ██║╚██████╔╝███████║   ██║     ║
    ║  ╚══════╝╚═╝  ╚═══╝  ╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝     ║
    ║                    {Fore.CYAN}LIVE HOST DISCOVERY v2.0{Fore.RED}                    ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    def __init__(self):
        self.live_hosts = []
        self.lock = threading.Lock()
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.os_type = platform.system().lower()
        self.total_hosts = 0
        self.completed = 0
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def resolve_hostname(self, ip):
        """Reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
            
    def ping_host_windows(self, ip, timeout=1000):
        """Windows ping command"""
        try:
            cmd = ["ping", "-n", "1", "-w", str(timeout), ip]
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except:
            return False
            
    def ping_host_posix(self, ip, timeout=1):
        """Linux/Unix ping command"""
        try:
            cmd = ["ping", "-c", "1", "-W", str(timeout), ip]
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except:
            return False
            
    def ping_host(self, ip, timeout):
        """Cross-platform ping"""
        if self.os_type == "windows":
            return self.ping_host_windows(ip, timeout * 1000)
        else:
            return self.ping_host_posix(ip, timeout)
            
    def tcp_connect_scan(self, ip, ports=[80, 443, 22, 445, 3389]):
        """TCP connect scan for hosts blocking ICMP"""
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    return True
            except:
                pass
        return False
        
    def arp_scan_windows(self, subnet):
        """ARP scan on Windows using arp -a"""
        try:
            cmd = ["arp", "-a"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            hosts = []
            for line in result.stdout.split('\n'):
                if '.' in line and 'dynamic' in line.lower():
                    parts = line.split()
                    if parts and self.ip_in_subnet(parts[0], subnet):
                        hosts.append(parts[0])
            return hosts
        except:
            return []
            
    def ip_in_subnet(self, ip, subnet):
        """Check if IP is in subnet"""
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(subnet, strict=False)
        except:
            return False
            
    def check_host(self, ip, use_tcp=False):
        """Comprehensive host check"""
        is_alive = False
        method = ""
        
        # ICMP ping
        if self.ping_host(ip, 1):
            is_alive = True
            method = "ICMP"
        # TCP fallback
        elif use_tcp and self.tcp_connect_scan(ip):
            is_alive = True
            method = "TCP"
            
        if is_alive:
            hostname = self.resolve_hostname(ip)
            with self.lock:
                self.live_hosts.append({
                    'ip': ip,
                    'hostname': hostname,
                    'method': method,
                    'timestamp': datetime.now().isoformat()
                })
                
        # Update progress
        with self.lock:
            self.completed += 1
            if self.completed % 10 == 0 or self.completed == self.total_hosts:
                progress = (self.completed / self.total_hosts) * 100
                # Simple ASCII progress bar
                bar_length = 30
                filled = int(bar_length * self.completed / self.total_hosts)
                bar = '#' * filled + '-' * (bar_length - filled)
                print(f"\r{Fore.CYAN}[{bar}] {self.completed}/{self.total_hosts} ({progress:.1f}%) | Found: {len(self.live_hosts)}{Style.RESET_ALL}", end="")
                
    def scan_subnet_ping_sweep(self, subnet, threads=50, use_tcp_fallback=True):
        """Ping sweep with threading"""
        self.live_hosts = []
        
        try:
            network = ipaddress.ip_network(subnet, strict=False)
        except ValueError as e:
            print(f"{Fore.RED}[✗] Invalid subnet format: {e}{Style.RESET_ALL}")
            return
            
        self.total_hosts = network.num_addresses - (1 if network.num_addresses > 1 else 0)
        
        print(f"\n{Fore.GREEN}[*] Scanning {subnet} - {self.total_hosts} hosts{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Threads: {threads} | TCP Fallback: {'Yes' if use_tcp_fallback else 'No'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] This may take several minutes depending on network size{Style.RESET_ALL}\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for ip in network.hosts():
                futures.append(executor.submit(self.check_host, str(ip), use_tcp_fallback))
                
            # Wait for all to complete
            concurrent.futures.wait(futures)
            
        print()  # New line after progress
        
    def scan_topology(self):
        """Discover network topology"""
        if self.os_type == "windows":
            return self.arp_scan_windows("0.0.0.0/0")
        else:
            return []
            
    def generate_report(self):
        """Generate detailed scan report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] LIVE HOST REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Hosts Scanned: {Fore.LIGHTGREEN_EX}{self.total_hosts}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Live Hosts Found: {Fore.LIGHTGREEN_EX}{len(self.live_hosts)}{Style.RESET_ALL}")
        
        if self.live_hosts:
            print(f"\n{Fore.CYAN}LIVE HOSTS:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  IP ADDRESS       HOSTNAME                    METHOD{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  ----------       --------                    ------\n{Style.RESET_ALL}")
            
            for host in sorted(self.live_hosts, key=lambda x: ipaddress.ip_address(x['ip'])):
                ip_display = f"{host['ip']:<16}"
                hostname_display = (host['hostname'][:25] + '...') if host['hostname'] and len(host['hostname']) > 25 else (host['hostname'] or 'Unknown')
                hostname_display = f"{hostname_display:<25}"
                
                if host['method'] == 'ICMP':
                    method_color = Fore.GREEN
                else:
                    method_color = Fore.YELLOW
                    
                print(f"  {Fore.WHITE}{ip_display}{Style.RESET_ALL} {hostname_display} {method_color}{host['method']}{Style.RESET_ALL}")
                
            # Statistics
            print(f"\n{Fore.CYAN}STATISTICS:{Style.RESET_ALL}")
            methods = {}
            for host in self.live_hosts:
                methods[host['method']] = methods.get(host['method'], 0) + 1
                
            for method, count in methods.items():
                print(f"  {Fore.GREEN}[+]{Style.RESET_ALL} {method}: {count} hosts")
                
        else:
            print(f"\n{Fore.RED}  [!] No live hosts discovered{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_csv(self, filename=None):
        """Export results to CSV"""
        import csv
        if not filename:
            filename = f"hosts_{self.scan_id}.csv"
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['IP Address', 'Hostname', 'Detection Method', 'Timestamp'])
                for host in self.live_hosts:
                    writer.writerow([host['ip'], host['hostname'] or 'Unknown', host['method'], host['timestamp']])
                    
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive discovery mode"""
        print(f"{Fore.GREEN}[*] Live Host Discovery initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Multiple detection methods: ICMP, TCP, ARP{Style.RESET_ALL}\n")
        
        # Scan options
        print(f"{Fore.CYAN}Scan Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Ping Sweep (ICMP + TCP fallback)")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} ARP Scan (local network)")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Single IP scan")
        print(f"  {Fore.WHITE}[4]{Style.RESET_ALL} IP Range (CIDR or dash notation)")
        
        scan_choice = input(f"\n{Fore.YELLOW}[?] Select scan type: {Style.RESET_ALL}").strip()
        
        if scan_choice == "1":
            subnet = input(f"{Fore.YELLOW}[?] Enter subnet (e.g., 192.168.1.0/24): {Style.RESET_ALL}").strip()
            try:
                threads = int(input(f"{Fore.YELLOW}[?] Threads (default 50): {Style.RESET_ALL}").strip() or "50")
            except:
                threads = 50
                
            tcp_fallback = input(f"{Fore.YELLOW}[?] Use TCP fallback for ICMP-blocked hosts? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
            
            self.start_time = datetime.now()
            self.scan_subnet_ping_sweep(subnet, threads, tcp_fallback)
            self.end_time = datetime.now()
            
        elif scan_choice == "2":
            print(f"\n{Fore.YELLOW}[*] Performing ARP cache scan...{Style.RESET_ALL}")
            self.start_time = datetime.now()
            
            if self.os_type == "windows":
                arp_hosts = self.arp_scan_windows("0.0.0.0/0")
                for ip in arp_hosts:
                    hostname = self.resolve_hostname(ip)
                    self.live_hosts.append({
                        'ip': ip,
                        'hostname': hostname,
                        'method': 'ARP',
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                print(f"{Fore.YELLOW}[!] ARP scan optimized for Windows{Style.RESET_ALL}")
                
            self.end_time = datetime.now()
            self.total_hosts = len(self.live_hosts)
            
        elif scan_choice == "3":
            ip = input(f"{Fore.YELLOW}[?] Enter IP address: {Style.RESET_ALL}").strip()
            self.start_time = datetime.now()
            self.total_hosts = 1
            
            print(f"\n{Fore.YELLOW}[*] Checking host {ip}...{Style.RESET_ALL}")
            self.check_host(ip, use_tcp_fallback=True)
            
            self.end_time = datetime.now()
            
        elif scan_choice == "4":
            range_input = input(f"{Fore.YELLOW}[?] Enter IP range (e.g., 192.168.1.1-254): {Style.RESET_ALL}").strip()
            
            try:
                if '/' in range_input:
                    network = ipaddress.ip_network(range_input, strict=False)
                    hosts = [str(ip) for ip in network.hosts()]
                elif '-' in range_input:
                    # Parse dash notation
                    start_ip, end = range_input.split('-')
                    if '.' not in end:
                        # e.g., 192.168.1.1-254
                        base = '.'.join(start_ip.split('.')[:-1])
                        start_num = int(start_ip.split('.')[-1])
                        end_num = int(end)
                        hosts = [f"{base}.{i}" for i in range(start_num, end_num + 1)]
                    else:
                        # Full IP range
                        start = ipaddress.ip_address(start_ip)
                        end = ipaddress.ip_address(end)
                        hosts = [str(ipaddress.ip_address(i)) for i in range(int(start), int(end) + 1)]
                else:
                    print(f"{Fore.RED}[✗] Invalid range format{Style.RESET_ALL}")
                    return
                    
                self.total_hosts = len(hosts)
                self.start_time = datetime.now()
                
                for ip in hosts:
                    self.check_host(ip, use_tcp_fallback=True)
                    
                self.end_time = datetime.now()
                
            except Exception as e:
                print(f"{Fore.RED}[✗] Invalid range: {e}{Style.RESET_ALL}")
                return
                
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        # Generate report
        self.generate_report()
        
        # Export option
        if self.live_hosts:
            export = input(f"\n{Fore.YELLOW}[?] Export results to CSV? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_csv()
                
        print(f"\n{Fore.GREEN}[✓] Host discovery completed{Style.RESET_ALL}")


def live_host_discovery(subnet=None):
    """Main entry point for CLI compatibility"""
    discoverer = LiveHostDiscovery()
    
    # Display banner
    discoverer.print_header()
    
    if subnet:
        # Direct scan mode
        discoverer.start_time = datetime.now()
        discoverer.scan_subnet_ping_sweep(subnet)
        discoverer.end_time = datetime.now()
        discoverer.generate_report()
    else:
        # Interactive mode
        discoverer.interactive_scan()


if __name__ == "__main__":
    live_host_discovery()
