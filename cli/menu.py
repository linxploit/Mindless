from colorama import Fore, Style

# Banners
from cli.banners import main_banner, kali_dragon

# Recon modules
from modules.recon.whois_intelligence import whois_lookup
from modules.recon.dns_recon_mapper import dns_recon
from modules.recon.subdomain_enumerator import subdomain_enum
from modules.recon.technology_stack_detector import detect_technology
from modules.recon.email_header_analyzer import analyze_email_headers


# Network modules
from modules.network.smart_port_scanner import smart_port_scan
from modules.network.live_host_discovery import live_host_discovery
from modules.network.ssl_tls_inspector import inspect_ssl_tls
from modules.network.firewall_waf_detector import detect_firewall_waf
from modules.network.ip_reputation_checker import check_ip_reputation

#Utilities
from modules.utilities.url_to_qr import url_to_qr
from modules.utilities.ip_info import ip_info
from modules.utilities.email_validator import email_validator
from modules.utilities.password_strength import password_strength_check
from modules.utilities.base64_tool import base64_encode
from modules.utilities.user_agent_generator import user_agent_generator



# Web security modules
from modules.websec.http_security_header_analyzer import analyze_headers
from modules.websec.directory_endpoint_fuzzer import directory_fuzzer
from modules.websec.cors_misconfiguration_checker import check_cors_misconfig
from modules.websec.xss_reflection_detector import xss_reflection_test
from modules.websec.file_upload_risk_analyzer import analyze_file_upload_risk


# Threat intel modules
from modules.threat_intel.phishing_url_analyzer import phishing_check
from modules.threat_intel.hash_analyzer import hash_analysis
from modules.threat_intel.pastebin_monitor import pastebin_leak_monitor
from modules.threat_intel.malicious_indicator_scanner import malicious_indicator_scan
from modules.threat_intel.brand_impersonation_detector import brand_impersonation


# =========================
# MAIN MENU
# =========================
def run_cli_menu():
    # Show banner ONCE
    kali_dragon()
    main_banner()

    while True:
        print(Fore.CYAN + """
[1] Reconnaissance Tools
[2] Network Tools
[3] Web Security Tools
[4] Threat Intelligence Tools
[5] Utilities
[0] Exit

""")

        choice = input(Fore.YELLOW + "Select: ").strip()

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
        elif choice == "0":
            print(Fore.RED + "Exiting Mindless, Stay Hungary.")
            break
        else:
            print(Fore.RED + "Invalid option.")


# =========================
# RECON MENU
# =========================
def recon_menu():
    while True:
        print("""
[ Reconnaissance ]
[1] WHOIS Intelligence
[2] DNS Recon Mapper
[3] Subdomain Enumerator
[4] Technology Stack Detector
[5] Email Header Analyzer
[0] Back
""")
        choice = input("Select: ").strip()

        if choice == "1":
            domain = input("Enter domain: ").strip()
            whois_lookup(domain)
            input("\nPress Enter to continue...")

        elif choice == "2":
            domain = input("Enter domain: ").strip()
            dns_recon(domain)
            input("\nPress Enter to continue...")

        elif choice == "3":
            domain = input("Enter domain: ").strip()
            subdomain_enum(domain)
            input("\nPress Enter to continue...")

        elif choice == "4":
            url = input("Enter URL (http/https): ").strip()
            detect_technology(url)
            input("\nPress Enter to continue...")

        elif choice == "5":
            header_file = input("Enter email header file path: ").strip()
            analyze_email_headers(header_file)
            input("\nPress Enter to continue...")

        elif choice == "0":
            return

        else:
            print("Invalid option.")


# =========================
# NETWORK MENU
# =========================
def network_menu():
    while True:
        print("""
[ Network ]
[1] Smart Port Scanner
[2] Live Host Discovery
[3] SSL / TLS Inspector
[4] Firewall / WAF Detector
[5] IP Reputation Checker
[0] Back
""")
        choice = input("Select: ").strip()

        if choice == "1":
            target = input("Enter IP / Host: ").strip()
            smart_port_scan(target)
            input("\nPress Enter to continue...")

        elif choice == "2":
            subnet = input("Enter subnet (e.g. 192.168.1.0/24): ").strip()
            live_host_discovery(subnet)
            input("\nPress Enter to continue...")

        elif choice == "3":
            host = input("Enter host (domain/IP): ").strip()
            inspect_ssl_tls(host)
            input("\nPress Enter to continue...")

        elif choice == "4":
            url = input("Enter URL (http/https): ").strip()
            detect_firewall_waf(url)
            input("\nPress Enter to continue...")

        elif choice == "5":
            ip = input("Enter IP address: ").strip()
            check_ip_reputation(ip)
            input("\nPress Enter to continue...")

        elif choice == "0":
            return

        else:
            print("Invalid option.")

# =========================
# WEB SECURITY MENU
# =========================
def web_menu():
    while True:
        print("""
[ Web Security ]
[1] HTTP Security Header Analyzer
[2] Directory / Endpoint Fuzzer
[3] CORS Misconfiguration Checker
[4] XSS Reflection Detector
[5] File Upload Risk Analyzer
[0] Back
""")
        choice = input("Select: ").strip()

        if choice == "1":
            url = input("Enter URL: ").strip()
            analyze_headers(url)
            input("\nPress Enter to continue...")

        elif choice == "2":
            url = input("Enter base URL (e.g. https://site.com): ").strip()
            directory_fuzzer(url)
            input("\nPress Enter to continue...")

        elif choice == "3":
            url = input("Enter URL: ").strip()
            check_cors_misconfig(url)
            input("\nPress Enter to continue...")

        elif choice == "4":
            url = input("Enter URL: ").strip()
            xss_reflection_test(url)
            input("\nPress Enter to continue...")

        elif choice == "5":
            url = input("Enter upload endpoint URL: ").strip()
            analyze_file_upload_risk(url)
            input("\nPress Enter to continue...")

        elif choice == "0":
            return

        else:
            print("Invalid option.")



# =========================
# THREAT INTEL MENU
# =========================
def threat_menu():
    while True:
        print("""
[ Threat Intelligence ]
[1] Phishing URL Analyzer
[2] Brand Impersonation Detector
[3] Hash Analyzer
[4] Malicious Indicator Scanner
[5] Pastebin / Leak Monitor
[0] Back
""")
        choice = input("Select: ").strip()

        if choice == "1":
            url = input("Enter URL: ").strip()
            phishing_check(url)
            input("\nPress Enter to continue...")

        elif choice == "2":
            text = input("Enter text / domain / message: ").strip()
            brand_impersonation(text)
            input("\nPress Enter to continue...")

        elif choice == "3":
            h = input("Enter hash: ").strip()
            hash_analysis(h)
            input("\nPress Enter to continue...")

        elif choice == "4":
            text = input("Enter text / log / content: ").strip()
            malicious_indicator_scan(text)
            input("\nPress Enter to continue...")

        elif choice == "5":
            query = input("Enter keyword / email / domain: ").strip()
            pastebin_leak_monitor(query)
            input("\nPress Enter to continue...")

        elif choice == "0":
            return

        else:
            print("Invalid option.")

def utilities_menu():
    while True:
        print("""
[ Utilities ]
[1] URL to QR Code
[2] IP Information Finder
[3] Base64 Encoder
[4] Password Strength Checker
[5] User-Agent Generator
[0] Back
""")
        choice = input("Select: ").strip()

        if choice == "1":
            url = input("Enter URL: ").strip()
            url_to_qr(url)
            input("\nPress Enter to continue...")

        elif choice == "2":
            ip = input("Enter IP address: ").strip()
            ip_info(ip)
            input("\nPress Enter to continue...")

        elif choice == "3":
            text = input("Enter text: ").strip()
            base64_encode(text)
            input("\nPress Enter to continue...")

        elif choice == "4":
            pwd = input("Enter password: ").strip()
            password_strength_check(pwd)
            input("\nPress Enter to continue...")

        elif choice == "5":
            try:
                count = int(input("How many User-Agents to generate? [default 1]: ") or 1)
                rotate = input("Rotate User-Agents? (y/n): ").lower() == "y"
                copy = input("Copy last User-Agent to clipboard? (y/n): ").lower() == "y"

                export = input("Save to file? (y/n): ").lower()
                export_file = None
                if export == "y":
                    export_file = input("Enter filename (e.g. agents.txt): ").strip()

                user_agent_generator(
                    rotate=rotate,
                    count=count,
                    copy=copy,
                    export_file=export_file
                )

            except KeyboardInterrupt:
                print("\n[!] Operation cancelled by user")

            input("\nPress Enter to continue...")

        elif choice == "0":
            return

        else:
            print("Invalid option.")
