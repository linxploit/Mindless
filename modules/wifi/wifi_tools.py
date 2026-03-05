#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: ESP8266 WIFI ATTACK TOOL
Connect to ESP8266 Deauther AP and open attack interface
Author: ICAT Project | Linxploit.xyz
"""

import socket
import subprocess
import sys
import os
import time
import webbrowser
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class ESP8266Deauther:
    """Simple tool to connect to ESP8266 Deauther and open attack interface"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗    ██╗██╗███████╗██╗     ██████╗ ███████╗ █████╗ ██╗   ██╗████████╗██╗  ██╗███████╗██████╗  ║
    ║  ██║    ██║██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔════╝██╔══██╗ ║
    ║  ██║ █╗ ██║██║█████╗  ██║     ██║  ██║█████╗  ███████║██║   ██║   ██║   ███████║█████╗  ██████╔╝ ║
    ║  ██║███╗██║██║██╔══╝  ██║     ██║  ██║██╔══╝  ██╔══██║██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗ ║
    ║  ╚███╔███╔╝██║██║     ███████╗██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║ ║
    ║   ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ║
    ║                    {Fore.CYAN}ESP8266 DEAUTHER CONTROLLER v1.0{Fore.RED}                     ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Known ESP8266 Deauther AP patterns
    DEAUTHER_APS = ['pwned', 'deauther', 'esp8266', 'pwned', 'pwned', 'pwned']
    
    # Default ESP8266 AP IP
    ESP_IP = "192.168.4.1"
    
    # Attack interface paths
    ATTACK_PATHS = [
        "/attack.html",
        "/index.html",
        "/",
        "/scan.html",
        "/deauth.html",
        "/beacon.html"
    ]
    
    def __init__(self):
        self.connected = False
        self.esp_ip = None
        self.attack_url = None
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def check_ap_connection(self):
        """Check if connected to ESP8266 AP"""
        print(f"\n{Fore.YELLOW}[*] Checking for ESP8266 Deauther connection...{Style.RESET_ALL}")
        
        # Try to ping the default ESP IP
        try:
            # Platform independent ping
            param = '-n' if sys.platform.lower() == 'win32' else '-c'
            command = ['ping', param, '1', self.ESP_IP]
            
            result = subprocess.run(command, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}[✓] Connected to ESP8266 AP at {self.ESP_IP}{Style.RESET_ALL}")
                self.connected = True
                self.esp_ip = self.ESP_IP
                return True
            else:
                print(f"{Fore.RED}[✗] Not connected to ESP8266 AP{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Please connect to the '{Fore.CYAN}pwned{Fore.YELLOW}' WiFi network first{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[✗] Error checking connection: {e}{Style.RESET_ALL}")
            return False
    
    def find_attack_interface(self):
        """Find the attack interface URL"""
        if not self.connected:
            return None
            
        import socket
        
        print(f"{Fore.YELLOW}[*] Locating attack interface...{Style.RESET_ALL}")
        
        # Try to connect to common paths
        import socket
        
        for path in self.ATTACK_PATHS:
            try:
                # Try to establish socket connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                # Extract port from path if specified
                url = f"{self.esp_ip}:80{path}"
                
                result = sock.connect_ex((self.esp_ip, 80))
                sock.close()
                
                if result == 0:
                    # Port 80 is open, assume web server is running
                    self.attack_url = f"http://{self.esp_ip}{path}"
                    print(f"{Fore.GREEN}[✓] Found attack interface at: {Fore.CYAN}{self.attack_url}{Style.RESET_ALL}")
                    return self.attack_url
                    
            except:
                continue
        
        # If no specific path found, use default
        self.attack_url = f"http://{self.esp_ip}"
        print(f"{Fore.YELLOW}[!] Using default interface: {Fore.CYAN}{self.attack_url}{Style.RESET_ALL}")
        return self.attack_url
    
    def open_attack_interface(self):
        """Open attack interface in default browser"""
        if not self.attack_url:
            print(f"{Fore.RED}[✗] No attack interface URL found{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.YELLOW}[*] Opening attack interface in browser...{Style.RESET_ALL}")
        
        try:
            # Open in default browser
            webbrowser.open(self.attack_url)
            print(f"{Fore.GREEN}[✓] Browser opened to {Fore.CYAN}{self.attack_url}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to open browser: {e}{Style.RESET_ALL}")
            return False
    
    def show_ap_info(self):
        """Show information about the AP"""
        if not self.connected:
            return
            
        print(f"\n{Fore.CYAN}[ ESP8266 DEAUTHER INFORMATION ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}AP IP Address:{Style.RESET_ALL}  {Fore.GREEN}{self.esp_ip}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Web Interface:{Style.RESET_ALL} {Fore.CYAN}{self.attack_url}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Default Login:{Style.RESET_ALL}  admin/admin")
        print()
        print(f"  {Fore.YELLOW}Available Attacks:{Style.RESET_ALL}")
        print(f"    • Deauthentication Attack")
        print(f"    • Beacon Flood")
        print(f"    • Probe Request Flood")
        print(f"    • Evil Portal")
        print(f"    • Handshake Capture")
    
    def run(self):
        """Main execution function"""
        self.print_header()
        
        print(f"{Fore.GREEN}[*] ESP8266 Deauther Controller{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Looking for 'pwned' access point...{Style.RESET_ALL}\n")
        
        # Step 1: Check connection to ESP8266 AP
        if not self.check_ap_connection():
            print(f"\n{Fore.YELLOW}[!] To use this tool:{Style.RESET_ALL}")
            print(f"  1. Plug in your ESP8266 with Deauther firmware")
            print(f"  2. Connect to the '{Fore.CYAN}pwned{Fore.YELLOW}' WiFi network")
            print(f"  3. Run this tool again\n")
            return False
        
        # Step 2: Find attack interface
        self.find_attack_interface()
        
        # Step 3: Show AP info
        self.show_ap_info()
        
        # Step 4: Ask to open browser
        print()
        choice = input(f"{Fore.YELLOW}[?] Open attack interface in browser? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if choice == 'y':
            self.open_attack_interface()
        
        print(f"\n{Fore.GREEN}[✓] ESP8266 Deauther tool completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[i] You can also manually access: {self.attack_url}{Style.RESET_ALL}")
        
        return True
    
    def quick_launch(self):
        """Quick launch - just check and open browser"""
        if self.check_ap_connection():
            self.find_attack_interface()
            if self.attack_url:
                self.open_attack_interface()
                return True
        return False


def wifi_attack_tool():
    """Main entry point for WiFi attack tool"""
    tool = ESP8266Deauther()
    tool.run()


def quick_launch():
    """Quick launch function for menu"""
    tool = ESP8266Deauther()
    return tool.quick_launch()


if __name__ == "__main__":
    wifi_attack_tool()