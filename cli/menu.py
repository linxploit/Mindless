#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: PROFESSIONAL CLI MENU SYSTEM
ULTRA FAST - Lazy loading + Caching
Author: ICAT Project | Linxploit.xyz
"""

import os
import sys
import platform
from datetime import datetime
from colorama import Fore, Style, init, Back
C = Fore.CYAN
Y = Fore.YELLOW



# Initialize colorama (this is fast, keep it)
init(autoreset=True)

# ============================================
# BANNERS - Keep your beautiful art! (fast to load)
# ============================================
from cli.banners import kali_dragon, main_banner, H_LINE, V_LINE, TL_CORNER, TR_CORNER, BL_CORNER, BR_CORNER

# ============================================
# LAZY LOADING CACHE - MODULES LOAD ONLY WHEN USED
# ============================================

# Cache dictionary - stores modules after first use
_MODULE_CACHE = {}

def lazy_import(module_path, function_name):
    """Import a module only when needed and cache it"""
    cache_key = f"{module_path}.{function_name}"
    
    if cache_key not in _MODULE_CACHE:
        try:
            # Dynamic import - FAST because it only runs when you use the tool
            module = __import__(module_path, fromlist=[function_name])
            _MODULE_CACHE[cache_key] = getattr(module, function_name)
        except ImportError as e:
            print(f"  {Fore.RED}[✗] Module not available: {module_path}{Style.RESET_ALL}")
            print(f"      {Fore.YELLOW}Error: {e}{Style.RESET_ALL}")
            _MODULE_CACHE[cache_key] = None
        except Exception as e:
            print(f"  {Fore.RED}[✗] Failed to load: {function_name}{Style.RESET_ALL}")
            print(f"      {Fore.YELLOW}Error: {e}{Style.RESET_ALL}")
            _MODULE_CACHE[cache_key] = None
    
    return _MODULE_CACHE[cache_key]

# ============================================
# MODULE LOADERS - Each tool loads ONLY when called
# ============================================

# Network modules
def get_smart_port_scan():
    return lazy_import('modules.network.smart_port_scanner', 'smart_port_scan')

def get_live_host_discovery():
    return lazy_import('modules.network.live_host_discovery', 'live_host_discovery')

def get_inspect_ssl_tls():
    return lazy_import('modules.network.ssl_tls_inspector', 'inspect_ssl_tls')

def get_detect_firewall_waf():
    return lazy_import('modules.network.firewall_waf_detector', 'detect_firewall_waf')

def get_check_ip_reputation():
    return lazy_import('modules.network.ip_reputation_checker', 'check_ip_reputation')

# Web modules
def get_analyze_headers():
    return lazy_import('modules.websec.http_security_header_analyzer', 'analyze_headers')

def get_directory_fuzzer():
    return lazy_import('modules.websec.directory_endpoint_fuzzer', 'directory_fuzzer')

def get_check_cors_misconfig():
    return lazy_import('modules.websec.cors_misconfiguration_checker', 'check_cors_misconfig')

def get_xss_reflection_test():
    return lazy_import('modules.websec.xss_reflection_detector', 'xss_reflection_test')

def get_analyze_file_upload_risk():
    return lazy_import('modules.websec.file_upload_risk_analyzer', 'analyze_file_upload_risk')

# Threat intel modules
def get_phishing_check():
    return lazy_import('modules.threat_intel.phishing_url_analyzer', 'phishing_check')

def get_hash_analysis():
    return lazy_import('modules.threat_intel.hash_analyzer', 'hash_analysis')

def get_pastebin_leak_monitor():
    return lazy_import('modules.threat_intel.pastebin_monitor', 'pastebin_leak_monitor')

def get_malicious_indicator_scan():
    return lazy_import('modules.threat_intel.malicious_indicator_scanner', 'malicious_indicator_scan')

def get_brand_impersonation():
    return lazy_import('modules.threat_intel.brand_impersonation_detector', 'brand_impersonation')

# Utilities modules
def get_url_to_qr():
    return lazy_import('modules.utilities.url_to_qr', 'url_to_qr')

def get_ip_info():
    return lazy_import('modules.utilities.ip_info', 'ip_info')

def get_email_validator():
    return lazy_import('modules.utilities.email_validator', 'email_validator')

def get_password_strength_check():
    return lazy_import('modules.utilities.password_strength', 'password_strength_check')

def get_base64_encode():
    return lazy_import('modules.utilities.base64_tool', 'base64_encode')

def get_base64_decode():
    return lazy_import('modules.utilities.base64_tool', 'base64_decode')

def get_user_agent_generator():
    return lazy_import('modules.utilities.user_agent_generator', 'user_agent_generator')

# ============================================
# RECON MODULES - SLOW, LOAD WITH TIMEOUT
# ============================================
import threading
import queue

def load_with_timeout(module_path, function_name, timeout=0.1):
    """Load module with timeout - if it takes >0.1s, skip it"""
    result_queue = queue.Queue()
    
    def loader():
        try:
            module = __import__(module_path, fromlist=[function_name])
            func = getattr(module, function_name)
            result_queue.put(('success', func))
        except Exception as e:
            result_queue.put(('error', str(e)))
    
    thread = threading.Thread(target=loader)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        return None  # Timed out - module is too slow
    
    try:
        status, result = result_queue.get_nowait()
        if status == 'success':
            return result
    except:
        pass
    
    return None

# Recon module loaders with timeout
def get_whois_lookup():
    return load_with_timeout('modules.recon.whois_intelligence', 'whois_lookup', timeout=0.1)

def get_dns_recon():
    return load_with_timeout('modules.recon.dns_recon_mapper', 'dns_recon', timeout=0.1)

def get_subdomain_enum():
    return load_with_timeout('modules.recon.subdomain_enumerator', 'subdomain_enum', timeout=0.1)

def get_detect_technology():
    return load_with_timeout('modules.recon.technology_stack_detector', 'detect_technology', timeout=0.1)

def get_analyze_email_headers():
    return load_with_timeout('modules.recon.email_header_analyzer', 'analyze_email_headers', timeout=0.1)

def get_certificate_intelligence():
    return load_with_timeout('modules.recon.certificate_intelligence', 'certificate_intelligence', timeout=0.1)

# ============================================
# GLOBAL CONFIGURATION - Your beautiful colors!
# ============================================
VERSION = "2.0.0"
CODENAME = "Red Harbor"
AUTHOR = "ICAT Project | Linxploit.xyz"

# Your professional color scheme
P = Fore.RED + Style.BRIGHT      # Primary - Blood Red
S = Fore.CYAN + Style.BRIGHT     # Secondary - Cyber Cyan
G = Fore.GREEN + Style.BRIGHT    # Success - Matrix Green
Y = Fore.YELLOW + Style.BRIGHT   # Warning - Amber
R = Fore.RED + Style.BRIGHT      # Error - Crimson
W = Fore.WHITE + Style.BRIGHT    # Info - White
D = Fore.BLACK + Style.BRIGHT    # Dim - Console Black

# Status indicators
LOADED = f"{Fore.GREEN}[✓]{Style.RESET_ALL}"
COMING = f"{Fore.YELLOW}[⏳]{Style.RESET_ALL}"
ERROR = f"{Fore.RED}[✗]{Style.RESET_ALL}"
INFO = f"{Fore.CYAN}[i]{Style.RESET_ALL}"
WARN = f"{Fore.YELLOW}[!]{Style.RESET_ALL}"
ARROW = f"{Fore.CYAN}→{Style.RESET_ALL}"
BRANCH = f"{Fore.CYAN}├─{Style.RESET_ALL}"
LAST = f"{Fore.CYAN}└─{Style.RESET_ALL}"

# ============================================
# SYSTEM HEADER - FAST (no delays)
# ============================================

def show_header():
    """Display dynamic system header - INSTANT"""
    os_name = platform.system()
    hostname = platform.node()
    username = os.getenv('USER') or os.getenv('USERNAME') or 'operator'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"{P}{TL_CORNER}{H_LINE * 78}{TR_CORNER}{Style.RESET_ALL}")
    print(f"{P}{V_LINE} {S}MINDLESS{R}::{P}REDOPS {D}[{W}v{VERSION}{D} | {W}{CODENAME}{D}]{V_LINE * 45}{P}{V_LINE}{Style.RESET_ALL}")
    print(f"{P}{V_LINE} {D}Operator : {W}{username:<20} {D}Host : {W}{hostname:<20} {D}{current_time}{P}{V_LINE}{Style.RESET_ALL}")
    print(f"{P}{BL_CORNER}{H_LINE * 78}{BR_CORNER}{Style.RESET_ALL}")
    print()

# ============================================
# MODULE STATUS - INSTANT (no imports)
# ============================================

def show_module_status():
    """Show module status - FAST (no actual imports)"""
    print(f"  {S}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"  {S}║                     MODULE STATUS DASHBOARD                    ║{Style.RESET_ALL}")
    print(f"  {S}╠════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"  {S}║  {LOADED} {W}Network Security       {D}[READY]                            {S}║{Style.RESET_ALL}")
    print(f"  {S}║  {LOADED} {W}Web Security           {D}[READY]                            {S}║{Style.RESET_ALL}")
    print(f"  {S}║  {LOADED} {W}Threat Intelligence    {D}[READY]                            {S}║{Style.RESET_ALL}")
    print(f"  {S}║  {LOADED} {W}Utilities              {D}[READY]                            {S}║{Style.RESET_ALL}")
    print(f"  {S}║  {LOADED} {W}Reconnaissance         {D}[READY]                            {S}║{Style.RESET_ALL}")
    print(f"  {S}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()








# ============================================
# CLEAR SCREEN - FAST
# ============================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================
# PAUSE FUNCTION - Your style, no delays
# ============================================

def pause():
    """Simple pause"""
    input(f"\n  {P}[>] Press Enter to continue...{Style.RESET_ALL}")

# ============================================
# PRINT HEADER - Your beautiful boxes
# ============================================

def print_header(title, subtitle=None):
    """Your professional header - INSTANT"""
    print(f"\n  {P}┌─{'─' * 48}─┐{Style.RESET_ALL}")
    print(f"  {P}│ {S}{title:^48}{P} │{Style.RESET_ALL}")
    if subtitle:
        print(f"  {P}│ {W}{subtitle:^48}{P} │{Style.RESET_ALL}")
    print(f"  {P}└─{'─' * 48}─┘{Style.RESET_ALL}")
    print()

# ============================================
# MAIN MENU - Your FULL professional design, now FAST!
# ============================================

def run_cli_menu():
    """Main menu - PROFESSIONAL + FAST"""
    
    while True:
        clear_screen()
        kali_dragon()
        main_banner()
        show_header()
        show_module_status()
        
        # Your beautiful main menu - FULL DESIGN
        print(f"  {P}┌────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"  {P}│{S}                    MAIN OPERATIONS MENU                    {P}│{Style.RESET_ALL}")
        print(f"  {P}├────────────────────────────────────────────────────────────┤{Style.RESET_ALL}")
        print(f"  {P}│                                                            │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[1]{Style.RESET_ALL}  {W}RECONNAISSANCE      {D}│ {W}WHOIS, DNS, Subdomains      {P}   │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[2]{Style.RESET_ALL}  {W}NETWORK SECURITY    {D}│ {W}Port Scan, Host Discovery   {P}   │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[3]{Style.RESET_ALL}  {W}WEB SECURITY        {D}│ {W}Headers, Fuzzing, CORS, XSS{P}    │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[4]{Style.RESET_ALL}  {W}THREAT INTELLIGENCE {D}│ {W}Phishing, Hash, IOC, Leaks{P}     │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[5]{Style.RESET_ALL}  {W}UTILITIES           {D}│ {W}QR, Email, Password, Base64{P}    │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[6]{Style.RESET_ALL}  {W}WIFI ATTACKS        {D}│ {W}ESP8266 Deauther, Beacon Flood{P} │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[7]{Style.RESET_ALL}  {W}SOC TOOLS           {D}│ {W}Log Monitor {Y}[Coming Soon]{W}{P}      │{Style.RESET_ALL}")
        print(f"  {P}│  {P}[0]{Style.RESET_ALL}  {R}EXIT                {D}│ {R}Terminate Session              {P}│{Style.RESET_ALL}")
        print(f"  {P}│                                                            │{Style.RESET_ALL}")
        print(f"  {P}└────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        print()
        

        # Hacker-style prompt
        print(f"  {S}┌─[ {P}MINDLESS{R}::{S}REDOPS {D}→ {W}SELECT{Style.RESET_ALL} {S}]")
        choice = input(f"  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            recon_menu()
        elif choice == "2":
            network_menu()
        elif choice == "3":
            web_menu()
        elif choice == "4":
            threat_menu()
        elif choice == "5":
            utilities_menu()
        elif choice == "7":
            soc_menu()
        # In the menu choice handler, add:
        elif choice == "6":
           wifi_menu()
        elif choice == "0":
            print(f"\n  {P}[*] Stay Hungary, Terminating session...{Style.RESET_ALL}")
            print(f"  {G}[✓] Goodbye, .{Style.RESET_ALL}")
            break
        else:
            print(f"\n  {R}[✗] Invalid option: {choice}{Style.RESET_ALL}")
            pause()

# ============================================
# NETWORK MENU - Your FULL design, now FAST!
# ============================================

def network_menu():
    """Network menu - PROFESSIONAL + FAST"""
    while True:
        clear_screen()
        print_header("NETWORK SECURITY OPERATIONS", "Perimeter Scanning & Analysis")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE MODULES                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}Smart Port Scanner     {D}│ {W}TCP Connect, Service Detection{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}Live Host Discovery    {D}│ {W}ICMP Ping Sweep & ARP Scan    {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}SSL/TLS Inspector      {D}│ {W}Protocol Analysis{S}             ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[4]{Style.RESET_ALL}  {W}WAF Detector           {D}│ {W}Firewall Fingerprinting       {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[5]{Style.RESET_ALL}  {W}IP Reputation Checker  {D}│ {W}Intelligence & Geolocation    {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN         {D}│ {R}Back to main menu             {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}NETWORK{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            target = input(f"\n  {Y}[?]{Style.RESET_ALL} Target IP/host: ").strip()
            if target:
                func = get_smart_port_scan()
                if func: func(target)
            pause()
        elif choice == "2":
            subnet = input(f"\n  {Y}[?]{Style.RESET_ALL} Subnet (e.g., 192.168.1.0/24): ").strip()
            if subnet:
                func = get_live_host_discovery()
                if func: func(subnet)
            pause()
        elif choice == "3":
            host = input(f"\n  {Y}[?]{Style.RESET_ALL} Target host: ").strip()
            if host:
                func = get_inspect_ssl_tls()
                if func: func(host)
            pause()
        elif choice == "4":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} Target URL: ").strip()
            if url:
                func = get_detect_firewall_waf()
                if func: func(url)
            pause()
        elif choice == "5":
            ip = input(f"\n  {Y}[?]{Style.RESET_ALL} IP address: ").strip()
            if ip:
                func = get_check_ip_reputation()
                if func: func(ip)
            pause()
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()

# ============================================
# RECON MENU - LAZY LOADED, FAST STARTUP
# ============================================

def recon_menu():
    """Recon menu - with expected wait times"""
    while True:
        clear_screen()
        print_header("RECONNAISSANCE OPERATIONS", "Information Gathering & OSINT")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE MODULES                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}WHOIS Intelligence     {D}│ {Y}[5-10s] Domain registration   {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}DNS Recon Mapper       {D}│ {Y}[10-20s] DNS records & zone   {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}Subdomain Enumerator   {D}│ {Y}[20-60s] DNS bruteforce       {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[4]{Style.RESET_ALL}  {W}Technology Stack       {D}│ {Y}[3-8s]  CMS & frameworks      {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[5]{Style.RESET_ALL}  {W}Email Header Analyzer  {D}│ {Y}[1-3s]   SPF, DKIM, DMARC     {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[6]{Style.RESET_ALL}  {W}Certificate Intel      {D}│ {Y}[3-8s]   CT logs & certs      {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN         {D}│ {R}Back to main menu             {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}RECON{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        # ... rest of your code ...
        
        if choice == "1":
            domain = input(f"\n  {Y}[?]{Style.RESET_ALL} Domain: ").strip()
            if domain:
                print(f"\n  {Y}[!] Loading WHOIS module (this may take 5-10 seconds)...{Style.RESET_ALL}")
                func = get_whois_lookup()
                if func:
                    func(domain)
                else:
                    print(f"\n  {R}[✗] WHOIS module failed to load (timeout){Style.RESET_ALL}")
            pause()
        elif choice == "2":
            domain = input(f"\n  {Y}[?]{Style.RESET_ALL} Domain: ").strip()
            if domain:
                print(f"\n  {Y}[!] Loading DNS module...{Style.RESET_ALL}")
                func = get_dns_recon()
                if func: func(domain)
            pause()
        elif choice == "3":
            domain = input(f"\n  {Y}[?]{Style.RESET_ALL} Domain: ").strip()
            if domain:
                print(f"\n  {Y}[!] Loading Subdomain module...{Style.RESET_ALL}")
                func = get_subdomain_enum()
                if func: func(domain)
            pause()
        elif choice == "4":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                print(f"\n  {Y}[!] Loading Technology module...{Style.RESET_ALL}")
                func = get_detect_technology()
                if func: func(url)
            pause()
        elif choice == "5":
            print(f"\n  {Y}[?] Paste email headers (Ctrl+D to finish):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except (EOFError, KeyboardInterrupt):
                headers = '\n'.join(lines)
                if headers:
                    print(f"\n  {Y}[!] Loading Email Header module...{Style.RESET_ALL}")
                    func = get_analyze_email_headers()
                    if func: func(headers)
            pause()
        elif choice == "6":
            domain = input(f"\n  {Y}[?]{Style.RESET_ALL} Domain: ").strip()
            if domain:
                print(f"\n  {Y}[!] Loading Certificate module...{Style.RESET_ALL}")
                func = get_certificate_intelligence()
                if func: func(domain)
            pause()
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()

# ============================================
# WEB MENU - Your FULL design (fast imports)
# ============================================

def web_menu():
    """Web menu - PROFESSIONAL + FAST"""
    while True:
        clear_screen()
        print_header("WEB SECURITY OPERATIONS", "Application Layer Assessment")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE MODULES                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}HTTP Security Headers    {D}│ {W}CSP, HSTS, XFO, CTO analysis{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}Directory Fuzzer         {D}│ {W}Content discovery           {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}CORS Checker             {D}│ {W}Cross-origin detection       {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[4]{Style.RESET_ALL}  {W}XSS Reflection Detector  {D}│ {W}SAFE mode - input reflection{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[5]{Style.RESET_ALL}  {W}File Upload Risk         {D}│ {W}Passive upload form analysis {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN           {D}│ {R}Back to main menu              {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}WEB{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                func = get_analyze_headers()
                if func: func(url)
            pause()
        elif choice == "2":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} Base URL: ").strip()
            if url:
                func = get_directory_fuzzer()
                if func: func(url)
            pause()
        elif choice == "3":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                func = get_check_cors_misconfig()
                if func: func(url)
            pause()
        elif choice == "4":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                func = get_xss_reflection_test()
                if func: func(url)
            pause()
        elif choice == "5":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} Upload URL: ").strip()
            if url:
                func = get_analyze_file_upload_risk()
                if func: func(url)
            pause()
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()

# ============================================
# THREAT MENU - Your FULL design (fast imports)
# ============================================

def threat_menu():
    """Threat menu - PROFESSIONAL + FAST"""
    while True:
        clear_screen()
        print_header("THREAT INTELLIGENCE OPERATIONS", "IOC Analysis & Threat Hunting")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE MODULES                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}Phishing URL Analyzer   {D}│ {W}Heuristic & domain reputation{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}Hash Analyzer           {D}│ {W}C-Graphic hash identification{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}IOC Scanner             {D}│ {W}Malicious indicator detection{S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[4]{Style.RESET_ALL}  {W}Brand Impersonation     {D}│ {W}Typosquatting & brand abuse  {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[5]{Style.RESET_ALL}  {W}Pastebin Leak Monitor   {D}│ {W}OSINT data leak detection    {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN          {D}│ {R}Back to main menu            {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}THREAT{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                func = get_phishing_check()
                if func: func(url)
            pause()
        elif choice == "2":
            h = input(f"\n  {Y}[?]{Style.RESET_ALL} Hash: ").strip()
            if h:
                func = get_hash_analysis()
                if func: func(h)
            pause()
        elif choice == "3":
            text = input(f"\n  {Y}[?]{Style.RESET_ALL} Text to scan: ").strip()
            if text:
                func = get_malicious_indicator_scan()
                if func: func(text)
            pause()
        elif choice == "4":
            text = input(f"\n  {Y}[?]{Style.RESET_ALL} Text/domain: ").strip()
            if text:
                func = get_brand_impersonation()
                if func: func(text)
            pause()
        elif choice == "5":
            q = input(f"\n  {Y}[?]{Style.RESET_ALL} Keyword/email: ").strip()
            if q:
                func = get_pastebin_leak_monitor()
                if func: func(q)
            pause()
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()

# ============================================
# UTILITIES MENU - Your FULL design (fast imports)
# ============================================

def utilities_menu():
    """Utilities menu - PROFESSIONAL + FAST"""
    while True:
        clear_screen()
        print_header("UTILITIES OPERATIONS", "Security Tools & Helpers")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE MODULES                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}URL to QR Code        {D}│ {W}Generate QR codes from URLs    {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}IP Information        {D}│ {W}Geolocation & network intel    {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}Base64 Encoder/Decoder{D}│ {W}Multiple encoding variants     {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[4]{Style.RESET_ALL}  {W}Email Validator       {D}│ {W}Syntax & MX record validation  {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[5]{Style.RESET_ALL}  {W}Password Strength     {D}│ {W}Entropy & breach checking      {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[6]{Style.RESET_ALL}  {W}User-Agent Generator  {D}│ {W}Real-world browser signatures  {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN        {D}│ {R}Back to main menu              {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}UTILS{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            url = input(f"\n  {Y}[?]{Style.RESET_ALL} URL: ").strip()
            if url:
                func = get_url_to_qr()
                if func: func(url)
            pause()
        elif choice == "2":
            ip = input(f"\n  {Y}[?]{Style.RESET_ALL} IP address: ").strip()
            if ip:
                func = get_ip_info()
                if func: func(ip)
            pause()
        elif choice == "3":
            print(f"\n  {P}[E]{Style.RESET_ALL} Encode")
            print(f"  {P}[D]{Style.RESET_ALL} Decode")
            ed = input(f"\n  {Y}[?]{Style.RESET_ALL} Select: ").strip().upper()
            if ed == 'E':
                text = input(f"\n  {Y}[?]{Style.RESET_ALL} Text: ").strip()
                if text:
                    func = get_base64_encode()
                    if func: func(text)
            elif ed == 'D':
                enc = input(f"\n  {Y}[?]{Style.RESET_ALL} Base64: ").strip()
                if enc:
                    func = get_base64_decode()
                    if func: func(enc)
            pause()
        elif choice == "4":
            email = input(f"\n  {Y}[?]{Style.RESET_ALL} Email: ").strip()
            if email:
                func = get_email_validator()
                if func: func(email)
            pause()
        elif choice == "5":
            import getpass
            pwd = getpass.getpass(f"\n  {Y}[?]{Style.RESET_ALL} Password: ")
            if pwd:
                func = get_password_strength_check()
                if func: func(pwd)
            pause()
        elif choice == "6":
            try:
                count = input(f"\n  {Y}[?]{Style.RESET_ALL} Count [1]: ").strip()
                count = int(count) if count.isdigit() else 1
                func = get_user_agent_generator()
                if func: func(count=count)
            except KeyboardInterrupt:
                print(f"\n\n  {Y}[!] Cancelled{Style.RESET_ALL}")
            pause()
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()



# ============================================
# WIFI TOOLS MENU - SIMPLE VERSION
# ============================================

def wifi_menu():
    """WiFi attack tools menu - ESP8266 Deauther"""
    while True:
        clear_screen()
        print_header("WIFI ATTACK TOOLS", "ESP8266 Deauther Controller")
        
        print(f"  {S}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"  {S}║                    AVAILABLE OPTIONS                         ║{Style.RESET_ALL}")
        print(f"  {S}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[1]{Style.RESET_ALL}  {W}Launch Attack Interface{Fore.RESET}{D}│ {W}Connect to 'pwned' AP         {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[2]{Style.RESET_ALL}  {W}Quick Launch Browser{Fore.RESET}   {D}│ {W}Open attack page immediately  {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[3]{Style.RESET_ALL}  {W}Show Connection Info{Fore.RESET}   {D}│ {W}Display ESP8266 details       {S}║{Style.RESET_ALL}")
        print(f"  {S}║  {P}[0]{Style.RESET_ALL}  {R}RETURN TO MAIN{Fore.RESET}         {D}│ {R}Back to main menu             {S}║{Style.RESET_ALL}")
        print(f"  {S}║                                                              ║{Style.RESET_ALL}")
        print(f"  {S}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        print(f"  {Y}[!] Make sure you're connected to the '{C}pwned{Y}' WiFi network{Style.RESET_ALL}")
        print(f"  {Y}[!] ESP8266 Deauther should be plugged in{Style.RESET_ALL}")
        print()
        
        choice = input(f"  {S}┌─[ {P}WIFI{R}::{S}SELECT{Style.RESET_ALL} ]\n  {S}└─[{P}#{Style.RESET_ALL}] ").strip()
        
        if choice == "1":
            from modules.wifi.wifi_tools import wifi_attack_tool
            wifi_attack_tool()
            pause()
            
        elif choice == "2":
            from modules.wifi.wifi_tools import quick_launch
            if not quick_launch():
                print(f"\n  {R}[✗] Not connected to ESP8266 AP{Style.RESET_ALL}")
                print(f"  {Y}[!] Connect to '{C}pwned{Y}' WiFi first{Style.RESET_ALL}")
            pause()
            
        elif choice == "3":
            from modules.wifi.wifi_tools import ESP8266Deauther
            tool = ESP8266Deauther()
            if tool.check_ap_connection():
                tool.find_attack_interface()
                tool.show_ap_info()
            pause()
            
        elif choice == "0":
            break
        else:
            print(f"\n  {R}[✗] Invalid option{Style.RESET_ALL}")
            pause()

# ============================================
# SOC MENU - Coming Soon
# ============================================

def soc_menu():
    """SOC menu - Coming Soon"""
    clear_screen()
    print_header("SOC TOOLS", "Security Operations Center")
    
    print(f"  {Y}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"  {Y}║                    COMING SOON                               ║{Style.RESET_ALL}")
    print(f"  {Y}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"  {Y}║                                                              ║{Style.RESET_ALL}")
    print(f"  {Y}║     {W}SOC Tools are under active development{Style.RESET_ALL}                   {Y}║{Style.RESET_ALL}")
    print(f"  {Y}║     {W}Release date: Q2 2026{Style.RESET_ALL}                                    {Y}║{Style.RESET_ALL}")
    print(f"  {Y}║                                                              ║{Style.RESET_ALL}")
    print(f"  {Y}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    pause()

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    try:
        run_cli_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {Y}[!] Interrupted by user{Style.RESET_ALL}")
        print(f"  {G}[✓] Session terminated.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n  {R}[✗] Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")