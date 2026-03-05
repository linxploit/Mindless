#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: DIRECTORY & ENDPOINT FUZZER
Advanced Web Directory/File Brute Forcing & Content Discovery
Author: ICAT Project | Linxploit.xyz
"""

import requests
import threading
import queue
import time
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import urllib3
import sys
import json

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class DirectoryEndpointFuzzer:
    """Advanced directory/file fuzzer with multi-threading and smart detection"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██�██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ║
    ║  ██╔══██╗██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ║
    ║  ██║  ██║██║██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝ ╚██╗║
    ║  ██║  ██║██║██╔══██╗██╔══╝  ██║        ██║   ██║   ██║██╔══██╗ ██╔╝║
    ║  ██████╔╝██║██║  ██║███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║██╔╝ ║
    ║  ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ║
    ║                    {Fore.CYAN}DIRECTORY FUZZER v2.0{Fore.RED}                       ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Comprehensive wordlist - common sensitive directories and files
    COMMON_PATHS = [
        # Admin panels
        'admin', 'administrator', 'admincp', 'adminarea', 'adminpanel', 'admin1', 'admin2',
        'adm', 'admins', 'dashboard', 'cpanel', 'whm', 'webadmin', 'manager', 'management',
        'controlpanel', 'cp', 'portal', 'adminportal', 'admin-console', 'admin-console',
        
        # Login pages
        'login', 'signin', 'sign-in', 'logon', 'auth', 'authenticate', 'login.php',
        'admin/login', 'user/login', 'wp-login', 'wp-login.php', 'administrator/index.php',
        
        # Configuration files
        '.env', 'config.php', 'config', 'configuration', 'settings', 'config.xml',
        'config.json', 'database.yml', 'wp-config.php', 'wp-config', 'app.config',
        'web.config', 'application.properties', 'settings.py', 'local.settings.json',
        
        # Backup files
        'backup', 'backups', 'backup.zip', 'backup.tar.gz', 'backup.sql', 'db_backup.sql',
        'dump.sql', 'database.sql', 'db.sql', 'backup.7z', 'backup.rar', 'old', 'bak',
        
        # Version control
        '.git', '.svn', '.hg', '.bzr', 'CVS', '.gitignore', '.git/config',
        '.git/HEAD', '.git/index', '.svn/entries', '.svn/wc.db',
        
        # Development files
        'test', 'tests', 'dev', 'development', 'staging', 'temp', 'tmp', 'demo',
        'sample', 'examples', 'example', 'api-test', 'sandbox', 'playground',
        
        # API endpoints
        'api', 'v1', 'v2', 'v3', 'api/v1', 'api/v2', 'rest', 'graphql', 'swagger',
        'swagger-ui', 'api-docs', 'docs', 'documentation', 'apidocs', 'openapi',
        
        # Upload directories
        'uploads', 'upload', 'files', 'media', 'images', 'img', 'assets', 'static',
        'public', 'downloads', 'download', 'userfiles', 'user_uploads', 'attachments',
        
        # Common CMS paths
        'wp-content', 'wp-includes', 'wp-admin', 'wp-json', 'wp', 'wordpress',
        'drupal', 'joomla', 'magento', 'magento2', 'shopify', 'prestashop',
        'phpmyadmin', 'phpMyAdmin', 'pma', 'myadmin', 'mysql', 'phpPgAdmin',
        
        # Sensitive files
        '.htaccess', '.htpasswd', 'robots.txt', 'sitemap.xml', 'sitemap.xml.gz',
        'crossdomain.xml', 'clientaccesspolicy.xml', 'security.txt',
        
        # Common web shells (for detection, not exploitation)
        'shell', 'webshell', 'cmd', 'exec', 'c99.php', 'r57.php', 'b374k.php',
        
        # Logs and debugging
        'logs', 'log', 'error_log', 'error.log', 'access.log', 'debug.log',
        'wp-content/debug.log', 'install.log', 'installer-log.txt',
        
        # Default credentials
        '.well-known', '.well-known/security.txt', '.well-known/acme-challenge',
        
        # Additional common paths
        'cgi-bin', 'cgi', 'scripts', 'includes', 'inc', 'classes', 'lib', 'library',
        'vendor', 'node_modules', 'bower_components', 'composer.json', 'package.json',
        'webhook', 'webhooks', 'callback', 'callbacks', 'webmention',
        'status', 'health', 'healthcheck', 'health-check', 'ping', 'heartbeat',
        'metrics', 'stats', 'statistics', 'analytics', 'monitoring',
    ]
    
    # File extensions to try
    EXTENSIONS = ['', '.php', '.asp', '.aspx', '.jsp', '.do', '.action', '.html', '.htm', '.txt', '.json', '.xml']
    
    # HTTP status codes that indicate existence
    VALID_STATUS_CODES = [200, 201, 202, 204, 301, 302, 303, 307, 308, 401, 403, 405, 500]
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.base_url = None
        self.found_paths = []
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.total_paths = 0
        self.completed = 0
        self.threads = 20
        self.timeout = 5
        self.recursive = False
        self.recursive_depth = 1
        self.extensions = False
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_url(self, url):
        """Normalize and validate URL"""
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
            
        parsed = urlparse(url)
        self.parsed_url = parsed
        self.domain = parsed.netloc
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.url = url.rstrip('/')
        
        return url
        
    def load_custom_wordlist(self, wordlist_path):
        """Load custom wordlist from file"""
        try:
            with open(wordlist_path, 'r') as f:
                paths = [line.strip() for line in f if line.strip()]
                self.COMMON_PATHS.extend(paths)
                print(f"{Fore.GREEN}[✓] Loaded {len(paths)} custom paths from {wordlist_path}{Style.RESET_ALL}")
                return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load wordlist: {e}{Style.RESET_ALL}")
            return False
            
    def worker(self):
        """Thread worker function"""
        while not self.queue.empty():
            try:
                path = self.queue.get_nowait()
                self.fuzz_path(path)
            except queue.Empty:
                break
            finally:
                self.queue.task_done()
                
    def fuzz_path(self, path):
        """Test a single path"""
        test_url = f"{self.url}/{path.lstrip('/')}"
        
        try:
            response = requests.get(
                test_url,
                timeout=self.timeout,
                verify=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                allow_redirects=False  # Don't follow redirects automatically
            )
            
            status = response.status_code
            
            if status in self.VALID_STATUS_CODES:
                content_length = len(response.content) if response.content else 0
                
                with self.lock:
                    self.found_paths.append({
                        'url': test_url,
                        'status': status,
                        'size': content_length,
                        'title': self.extract_title(response.text),
                        'content_type': response.headers.get('Content-Type', 'Unknown'),
                        'server': response.headers.get('Server', 'Unknown'),
                    })
                    
                    # Color-code based on status
                    if status == 200:
                        status_color = Fore.GREEN
                    elif status in [301, 302, 307, 308]:
                        status_color = Fore.CYAN
                    elif status in [401, 403]:
                        status_color = Fore.YELLOW
                    elif status in [500, 502, 503]:
                        status_color = Fore.RED
                    else:
                        status_color = Fore.MAGENTA
                        
                    size_display = f"{content_length:,} bytes" if content_length < 1024*1024 else f"{content_length/1024/1024:.2f} MB"
                    
                    print(f"  {status_color}[{status}]{Style.RESET_ALL} {test_url:<60} {Fore.WHITE}[{size_display}]{Style.RESET_ALL}")
                    
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except Exception:
            pass
            
        # Update progress
        with self.lock:
            self.completed += 1
            if self.completed % 10 == 0 or self.completed == self.total_paths:
                progress = (self.completed / self.total_paths) * 100
                bar_length = 30
                filled = int(bar_length * self.completed / self.total_paths)
                bar = '#' * filled + '-' * (bar_length - filled)
                print(f"\r{Fore.CYAN}[{bar}] {self.completed}/{self.total_paths} ({progress:.1f}%) | Found: {len(self.found_paths)}{Style.RESET_ALL}", end="")
                
    def start_fuzzing(self):
        """Start the fuzzing process"""
        self.found_paths = []
        self.completed = 0
        
        # Build path list
        paths_to_test = []
        
        if self.extensions:
            # Test each path with different extensions
            for path in self.COMMON_PATHS:
                for ext in self.EXTENSIONS:
                    paths_to_test.append(f"{path}{ext}")
        else:
            paths_to_test = self.COMMON_PATHS
            
        self.total_paths = len(paths_to_test)
        
        # Add paths to queue
        for path in paths_to_test:
            self.queue.put(path)
            
        print(f"\n{Fore.GREEN}[*] Target: {self.url}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Threads: {self.threads} | Timeout: {self.timeout}s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Testing {self.total_paths} paths{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] This may take several minutes...{Style.RESET_ALL}\n")
        
        # Create and start threads
        threads = []
        for _ in range(min(self.threads, self.total_paths)):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
            
        # Wait for all threads
        for t in threads:
            try:
                t.join()
            except:
                pass
                
        self.queue.join()
        print()  # New line after progress
        
    def extract_title(self, html):
        """Extract page title from HTML"""
        try:
            start = html.find('<title>')
            end = html.find('</title>')
            if start != -1 and end != -1:
                title = html[start + 7:end].strip()
                return title[:50] + '...' if len(title) > 50 else title
        except:
            pass
        return ''
        
    def generate_report(self):
        """Generate comprehensive fuzzing report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] DIRECTORY FUZZING REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Base URL: {Fore.LIGHTGREEN_EX}{self.base_url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Paths Tested: {Fore.LIGHTGREEN_EX}{self.total_paths}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Paths Found: {Fore.LIGHTGREEN_EX}{len(self.found_paths)}{Style.RESET_ALL}")
        
        if self.found_paths:
            # Sort by status code
            sorted_paths = sorted(self.found_paths, key=lambda x: x['status'])
            
            print(f"\n{Fore.CYAN}[ DISCOVERED PATHS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}\n")
            
            # Group by status code
            status_groups = {}
            for path in sorted_paths:
                status = path['status']
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(path)
                
            for status in sorted(status_groups.keys()):
                if status == 200:
                    status_color = Fore.GREEN
                    status_desc = "OK"
                elif status in [301, 302, 307, 308]:
                    status_color = Fore.CYAN
                    status_desc = "REDIRECT"
                elif status in [401, 403]:
                    status_color = Fore.YELLOW
                    status_desc = "FORBIDDEN/UNAUTHORIZED"
                elif status in [500, 502, 503]:
                    status_color = Fore.RED
                    status_desc = "SERVER ERROR"
                else:
                    status_color = Fore.MAGENTA
                    status_desc = "OTHER"
                    
                print(f"\n  {status_color}[{status}] {status_desc}{Style.RESET_ALL} - {len(status_groups[status])} paths")
                
                for path in status_groups[status][:10]:  # Show first 10 of each status
                    print(f"    ├─ {path['url']}")
                    if path['title']:
                        print(f"    │  └─ Title: {Fore.WHITE}{path['title']}{Style.RESET_ALL}")
                        
                if len(status_groups[status]) > 10:
                    print(f"    └─ ... and {len(status_groups[status]) - 10} more")
                    
            # ============ SECURITY IMPLICATIONS ============
            print(f"\n{Fore.CYAN}[ SECURITY IMPLICATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Check for sensitive findings
            sensitive_patterns = {
                '.git': 'Git repository exposed - possible source code disclosure',
                '.env': 'Environment file exposed - possible credentials disclosure',
                'wp-config.php': 'WordPress config exposed - database credentials at risk',
                'phpmyadmin': 'phpMyAdmin exposed - database management interface',
                'admin': 'Admin panel exposed - potential brute force target',
                'backup': 'Backup files exposed - possible sensitive data leakage',
                'api': 'API endpoint discovered - check for missing authentication',
                'login': 'Login page discovered - potential credential stuffing target',
            }
            
            for path in self.found_paths:
                url_lower = path['url'].lower()
                for pattern, implication in sensitive_patterns.items():
                    if pattern in url_lower:
                        print(f"  {Fore.RED}[!] {implication}{Style.RESET_ALL}")
                        print(f"      └─ {path['url']}")
                        break
                        
            # ============ RECOMMENDATIONS ============
            print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            recommendations = []
            
            # Check for exposed admin panels
            admin_paths = [p for p in self.found_paths if 'admin' in p['url'].lower() and p['status'] == 200]
            if admin_paths:
                recommendations.append("Implement IP whitelisting or VPN for admin panels")
                recommendations.append("Add multi-factor authentication to admin interfaces")
                
            # Check for exposed version control
            vc_paths = [p for p in self.found_paths if '.git' in p['url'].lower() or '.svn' in p['url'].lower()]
            if vc_paths:
                recommendations.append("Remove .git/.svn directories from production server")
                
            # Check for exposed config files
            config_paths = [p for p in self.found_paths if '.env' in p['url'].lower() or 'config' in p['url'].lower()]
            if config_paths:
                recommendations.append("Move configuration files outside webroot")
                recommendations.append("Set proper file permissions (644 for files, 755 for directories)")
                
            # Check for exposed backups
            backup_paths = [p for p in self.found_paths if 'backup' in p['url'].lower() or '.sql' in p['url'].lower()]
            if backup_paths:
                recommendations.append("Remove backup files from public directories")
                recommendations.append("Store backups in secure, non-web-accessible locations")
                
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {rec}")
            else:
                print(f"  {Fore.GREEN}[✓] No critical security issues identified{Style.RESET_ALL}")
                
        else:
            print(f"\n{Fore.RED}  [!] No directories or files discovered{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"fuzzer_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'base_url': self.base_url,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'paths_tested': self.total_paths,
            'paths_found': len(self.found_paths),
            'discovered_paths': self.found_paths,
            'configuration': {
                'threads': self.threads,
                'timeout': self.timeout,
                'extensions': self.extensions,
                'recursive': self.recursive,
                'recursive_depth': self.recursive_depth
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive fuzzing mode"""
        print(f"{Fore.GREEN}[*] Directory/Endpoint Fuzzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced content discovery with multi-threading{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter target URL (e.g., https://example.com): {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        # Configure scan
        print(f"\n{Fore.CYAN}Scan Configuration:{Style.RESET_ALL}")
        
        try:
            threads = input(f"{Fore.YELLOW}[?] Threads (default 20): {Style.RESET_ALL}").strip()
            self.threads = int(threads) if threads else 20
            
            timeout = input(f"{Fore.YELLOW}[?] Timeout (seconds, default 5): {Style.RESET_ALL}").strip()
            self.timeout = int(timeout) if timeout else 5
            
            extensions = input(f"{Fore.YELLOW}[?] Test file extensions? (php,asp,aspx,jsp,html) (y/n): {Style.RESET_ALL}").strip().lower()
            self.extensions = extensions == 'y'
            
            wordlist = input(f"{Fore.YELLOW}[?] Custom wordlist file? (press Enter to skip): {Style.RESET_ALL}").strip()
            if wordlist:
                self.load_custom_wordlist(wordlist)
                
        except ValueError:
            print(f"{Fore.RED}[✗] Invalid input, using defaults{Style.RESET_ALL}")
            self.threads = 20
            self.timeout = 5
            self.extensions = False
            
        self.start_time = datetime.now()
        self.start_fuzzing()
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.found_paths:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] Directory fuzzing completed{Style.RESET_ALL}")


def directory_fuzzer(url=None):
    """Main entry point for CLI compatibility"""
    fuzzer = DirectoryEndpointFuzzer()
    
    # Display banner
    fuzzer.print_header()
    
    if url:
        # Direct scan mode
        fuzzer.normalize_url(url)
        fuzzer.start_time = datetime.now()
        fuzzer.start_fuzzing()
        fuzzer.end_time = datetime.now()
        fuzzer.generate_report()
    else:
        # Interactive mode
        fuzzer.interactive_scan()


if __name__ == "__main__":
    directory_fuzzer()
