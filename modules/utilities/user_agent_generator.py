#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: USER-AGENT GENERATOR
Advanced Browser & Device User-Agent String Generator
Author: ICAT Project | Linxploit.xyz
"""

import random
import json
import time
from datetime import datetime
from colorama import Fore, Style, init

# Try to import pyperclip for clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

init(autoreset=True)

class UserAgentGenerator:
    """Advanced user-agent string generator with real-world browser data"""
    
    BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██╗   ██╗███████╗███████╗██████╗     █████╗  ██████╗ ███████╗███╗   ██╗████████╗██╗  ██╗ ██████╗  ║
    ║  ██║   ██║██╔════╝██╔════╝██╔══██╗   ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██║  ██║██╔═══██╗ ║
    ║  ██║   ██║███████╗█████╗  ██████╔╝   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████║██║   ██║ ║
    ║  ██║   ██║╚════██║██╔══╝  ██╔══██╗   ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║   ██║ ║
    ║  ╚██████╔╝███████║███████╗██║  ██║   ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝ ║
    ║   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ║
    ║                    {Fore.GREEN} ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ {Fore.CYAN} ║
    ║                    {Fore.GREEN}██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗{Fore.CYAN} ║
    ║                    {Fore.GREEN}██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝{Fore.CYAN} ║
    ║                    {Fore.GREEN}██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗{Fore.CYAN} ║
    ║                    {Fore.GREEN}╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║{Fore.CYAN} ║
    ║                    {Fore.GREEN} ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{Fore.CYAN} ║
    ║                    {Fore.GREEN}USER-AGENT GENERATOR v2.0{Fore.CYAN}                         ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Comprehensive User-Agent database by category
    USER_AGENTS = {
        'chrome': {
            'name': 'Google Chrome',
            'agents': [
                # Windows Chrome
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                
                # Mac Chrome
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                
                # Linux Chrome
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            ]
        },
        'firefox': {
            'name': 'Mozilla Firefox',
            'agents': [
                # Windows Firefox
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
                
                # Mac Firefox
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
                
                # Linux Firefox
                "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            ]
        },
        'edge': {
            'name': 'Microsoft Edge',
            'agents': [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            ]
        },
        'safari': {
            'name': 'Apple Safari',
            'agents': [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.5 Safari/605.1.15",
            ]
        },
        'mobile_ios': {
            'name': 'iOS Mobile',
            'agents': [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            ]
        },
        'mobile_android': {
            'name': 'Android Mobile',
            'agents': [
                "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 14; Samsung SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.80 Mobile Safari/537.36",
            ]
        },
        'bot': {
            'name': 'Search Bot',
            'agents': [
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
                "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
                "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
                "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
            ]
        },
        'linux': {
            'name': 'Linux Desktop',
            'agents': [
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            ]
        },
        'mac': {
            'name': 'macOS',
            'agents': [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            ]
        },
        'windows': {
            'name': 'Windows',
            'agents': [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            ]
        },
        'legacy': {
            'name': 'Legacy Browsers',
            'agents': [
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
            ]
        },
        'custom': {
            'name': 'Custom Build',
            'agents': []
        }
    }
    
    def __init__(self):
        self.generated_agents = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def get_categories(self):
        """Get list of available categories"""
        return list(self.USER_AGENTS.keys())
        
    def get_category_names(self):
        """Get dictionary of category names"""
        return {k: v['name'] for k, v in self.USER_AGENTS.items()}
        
    def generate(self, categories=None, count=1, rotate=False):
        """Generate user-agent strings"""
        self.generated_agents = []
        
        # If no categories specified, use all
        if not categories:
            categories = self.get_categories()
            # Exclude custom if empty
            if 'custom' in categories and not self.USER_AGENTS['custom']['agents']:
                categories.remove('custom')
                
        for i in range(count):
            if rotate and i > 0:
                # Rotate through categories
                category = categories[i % len(categories)]
            else:
                # Random category
                category = random.choice(categories)
                
            # Get random agent from category
            agents = self.USER_AGENTS[category]['agents']
            if agents:
                agent = random.choice(agents)
            else:
                # Fallback to Chrome if category empty
                agent = random.choice(self.USER_AGENTS['chrome']['agents'])
                category = 'chrome'
                
            self.generated_agents.append({
                'index': i + 1,
                'category': category,
                'category_name': self.USER_AGENTS[category]['name'],
                'user_agent': agent,
                'length': len(agent)
            })
            
        return self.generated_agents
        
    def add_custom_agent(self, user_agent):
        """Add custom user-agent to database"""
        self.USER_AGENTS['custom']['agents'].append(user_agent)
        return len(self.USER_AGENTS['custom']['agents'])
        
    def clear_custom_agents(self):
        """Clear all custom agents"""
        self.USER_AGENTS['custom']['agents'] = []
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(text)
                return True
            except:
                return False
        return False
        
    def generate_headers(self, user_agent):
        """Generate complete HTTP headers with user-agent"""
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        return headers
        
    def generate_report(self):
        """Generate user-agent generation report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] USER-AGENT GENERATION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Generated: {Fore.LIGHTGREEN_EX}{len(self.generated_agents)} user-agent(s){Style.RESET_ALL}")
        print(f"{Fore.WHITE}Categories Used: {Fore.LIGHTGREEN_EX}{len(set(a['category'] for a in self.generated_agents))}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ GENERATED AGENTS ============
        print(f"\n{Fore.CYAN}[ GENERATED USER-AGENTS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
        
        # Group by category
        categories_used = {}
        for agent in self.generated_agents:
            cat = agent['category']
            if cat not in categories_used:
                categories_used[cat] = []
            categories_used[cat].append(agent)
            
        for cat, agents in categories_used.items():
            cat_name = self.USER_AGENTS[cat]['name']
            print(f"\n  {Fore.YELLOW}{cat_name}:{Style.RESET_ALL} {len(agents)} agent(s)")
            
            for agent in agents:
                ua = agent['user_agent']
                print(f"\n    [{agent['index']}] {Fore.CYAN}{ua[:100]}{'...' if len(ua) > 100 else ''}{Style.RESET_ALL}")
                print(f"        └─ Length: {agent['length']} chars")
                
                # Copy command
                print(f"        └─ Copy: {Fore.YELLOW}user_agent_generator.py --copy {agent['index']}{Style.RESET_ALL}")
                
        # ============ STATISTICS ============
        print(f"\n{Fore.CYAN}[ STATISTICS ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Average length
        avg_length = sum(a['length'] for a in self.generated_agents) / len(self.generated_agents) if self.generated_agents else 0
        print(f"\n  {Fore.WHITE}Average Length:{Style.RESET_ALL} {avg_length:.1f} characters")
        
        # Shortest/Longest
        if self.generated_agents:
            shortest = min(self.generated_agents, key=lambda x: x['length'])
            longest = max(self.generated_agents, key=lambda x: x['length'])
            print(f"  {Fore.WHITE}Shortest:{Style.RESET_ALL} {shortest['length']} chars ({shortest['category_name']})")
            print(f"  {Fore.WHITE}Longest:{Style.RESET_ALL} {longest['length']} chars ({longest['category_name']})")
            
        # ============ HTTP HEADERS EXAMPLE ============
        if self.generated_agents:
            print(f"\n{Fore.CYAN}[ HTTP HEADERS EXAMPLE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            headers = self.generate_headers(self.generated_agents[0]['user_agent'])
            print(f"\n  {Fore.WHITE}Complete header set for request:{Style.RESET_ALL}\n")
            for key, value in headers.items():
                print(f"    {key}: {value}")
                
        # ============ USAGE EXAMPLES ============
        print(f"\n{Fore.CYAN}[ USAGE EXAMPLES ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"""
  {Fore.WHITE}Python Requests:{Style.RESET_ALL}
    headers = {{
        'User-Agent': '{self.generated_agents[0]["user_agent"][:50]}...'
    }}
    response = requests.get(url, headers=headers)
    
  {Fore.WHITE}Command Line:{Style.RESET_ALL}
    python user_agent_generator.py --chrome --count 5 --copy
    
  {Fore.WHITE}Selenium WebDriver:{Style.RESET_ALL}
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent={self.generated_agents[0]["user_agent"][:50]}...')
        """)
        
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export generated agents to file"""
        if not filename:
            filename = f"user_agents_{self.scan_id}.txt"
            
        try:
            with open(filename, 'w') as f:
                for agent in self.generated_agents:
                    f.write(f"# {agent['category_name']} - Agent {agent['index']}\n")
                    f.write(f"{agent['user_agent']}\n\n")
                    
            print(f"{Fore.GREEN}[✓] User-agents exported to: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            return None
            
    def interactive_generate(self):
        """Interactive user-agent generation mode"""
        print(f"{Fore.GREEN}[*] User-Agent Generator initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Real-world browser and device signatures{Style.RESET_ALL}\n")
        
        # Show categories
        print(f"{Fore.CYAN}Available Categories:{Style.RESET_ALL}")
        categories_list = []
        for i, (key, value) in enumerate(self.USER_AGENTS.items(), 1):
            if key != 'custom' or value['agents']:
                print(f"  {Fore.WHITE}[{i}]{Style.RESET_ALL} {value['name']}")
                categories_list.append(key)
                
        print(f"  {Fore.WHITE}[A]{Style.RESET_ALL} All categories")
        print(f"  {Fore.WHITE}[R]{Style.RESET_ALL} Random selection")
        
        # Get category selection
        choice = input(f"\n{Fore.YELLOW}[?] Select categories (comma-separated numbers, or A/R): {Style.RESET_ALL}").strip()
        
        selected_categories = []
        if choice.upper() == 'A':
            selected_categories = [c for c in categories_list if c != 'custom' or self.USER_AGENTS['custom']['agents']]
        elif choice.upper() == 'R':
            # Random 3 categories
            selected_categories = random.sample([c for c in categories_list if c != 'custom'], min(3, len(categories_list)))
        else:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            for idx in indices:
                if 1 <= idx <= len(categories_list):
                    selected_categories.append(categories_list[idx - 1])
                    
        if not selected_categories:
            print(f"{Fore.RED}[✗] No valid categories selected{Style.RESET_ALL}")
            return
            
        # Get count
        try:
            count = int(input(f"{Fore.YELLOW}[?] Number of agents to generate (default 1): {Style.RESET_ALL}").strip() or "1")
            count = max(1, min(100, count))
        except:
            count = 1
            
        # Rotate option
        rotate = input(f"{Fore.YELLOW}[?] Rotate through categories? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        # Copy option
        copy_last = input(f"{Fore.YELLOW}[?] Copy last agent to clipboard? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        # Export option
        export = input(f"{Fore.YELLOW}[?] Export to file? (y/n): {Style.RESET_ALL}").strip().lower()
        export_file = None
        if export == 'y':
            export_file = input(f"{Fore.YELLOW}[?] Filename (default: auto-generate): {Style.RESET_ALL}").strip() or None
            
        # Custom agent
        add_custom = input(f"{Fore.YELLOW}[?] Add custom user-agent? (y/n): {Style.RESET_ALL}").strip().lower()
        if add_custom == 'y':
            custom_ua = input(f"{Fore.YELLOW}[?] Enter custom user-agent string: {Style.RESET_ALL}").strip()
            if custom_ua:
                self.add_custom_agent(custom_ua)
                print(f"{Fore.GREEN}[✓] Custom agent added{Style.RESET_ALL}")
                
        self.start_time = datetime.now()
        
        # Generate agents
        self.generate(categories=selected_categories, count=count, rotate=rotate)
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Copy to clipboard
        if copy_last and self.generated_agents:
            if self.copy_to_clipboard(self.generated_agents[-1]['user_agent']):
                print(f"{Fore.GREEN}[✓] Copied to clipboard{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Clipboard not available (install pyperclip){Style.RESET_ALL}")
                
        # Export to file
        if export_file or export == 'y':
            filename = self.export_report(export_file)
            
        print(f"\n{Fore.GREEN}[✓] User-agent generation completed{Style.RESET_ALL}")


def user_agent_generator(rotate=False, count=1, copy=False, export_file=None, return_header=False):
    """Main entry point for CLI compatibility"""
    generator = UserAgentGenerator()
    
    # Display banner
    generator.print_header()
    
    # Generate agents
    generator.start_time = datetime.now()
    generator.generate(categories=None, count=count, rotate=rotate)
    generator.end_time = datetime.now()
    
    # Generate report
    generator.generate_report()
    
    # Copy to clipboard
    if copy and generator.generated_agents:
        if generator.copy_to_clipboard(generator.generated_agents[-1]['user_agent']):
            print(f"{Fore.GREEN}[✓] Copied to clipboard{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Clipboard not available (install pyperclip){Style.RESET_ALL}")
            
    # Export to file
    if export_file:
        generator.export_report(export_file)
        
    # Return header dict if requested
    if return_header and generator.generated_agents:
        return generator.generate_headers(generator.generated_agents[-1]['user_agent'])
        
    return generator.generated_agents


if __name__ == "__main__":
    import sys
    
    generator = UserAgentGenerator()
    generator.print_header()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        count = 1
        rotate = False
        copy = False
        export_file = None
        categories = []
        
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i].lower()
            if arg == '--count' or arg == '-c':
                if i + 1 < len(sys.argv):
                    count = int(sys.argv[i + 1])
                    i += 2
                else:
                    i += 1
            elif arg == '--rotate' or arg == '-r':
                rotate = True
                i += 1
            elif arg == '--copy' or arg == '-cp':
                copy = True
                i += 1
            elif arg == '--export' or arg == '-e':
                if i + 1 < len(sys.argv):
                    export_file = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == '--chrome':
                categories.append('chrome')
                i += 1
            elif arg == '--firefox':
                categories.append('firefox')
                i += 1
            elif arg == '--edge':
                categories.append('edge')
                i += 1
            elif arg == '--safari':
                categories.append('safari')
                i += 1
            elif arg == '--mobile':
                categories.append('mobile_ios')
                categories.append('mobile_android')
                i += 1
            elif arg == '--bot':
                categories.append('bot')
                i += 1
            elif arg == '--windows':
                categories.append('windows')
                i += 1
            elif arg == '--mac':
                categories.append('mac')
                i += 1
            elif arg == '--linux':
                categories.append('linux')
                i += 1
            else:
                i += 1
                
        generator.start_time = datetime.now()
        generator.generate(categories if categories else None, count, rotate)
        generator.end_time = datetime.now()
        generator.generate_report()
        
        if copy and generator.generated_agents:
            generator.copy_to_clipboard(generator.generated_agents[-1]['user_agent'])
            
        if export_file:
            generator.export_report(export_file)
    else:
        generator.interactive_generate()
