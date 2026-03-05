#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: TECHNOLOGY STACK DETECTOR
Advanced Web Technology Fingerprinting & CMS Detection
Author: ICAT Project | Linxploit.xyz
"""

import requests
import re
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class TechnologyStackDetector:
    """Advanced web technology detection and fingerprinting"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║              TECHNOLOGY STACK DETECTOR v2.0                   ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Web server signatures
    SERVER_SIGNATURES = {
        'Apache': [r'Apache(?:/(\d+\.\d+\.\d+))?', r'Apache'],
        'Nginx': [r'nginx(?:/(\d+\.\d+\.\d+))?', r'nginx'],
        'IIS': [r'Microsoft-IIS(?:/(\d+\.\d+))?', r'IIS'],
        'Tomcat': [r'Apache-Coyote', r'Tomcat'],
        'Jetty': [r'Jetty(?:\((\d+\.\d+\.\d+)\))?'],
        'Caddy': [r'Caddy'],
        'Lighttpd': [r'lighttpd(?:/(\d+\.\d+\.\d+))?'],
        'LiteSpeed': [r'LiteSpeed'],
        'OpenResty': [r'OpenResty'],
        'Gunicorn': [r'gunicorn'],
        'Node.js': [r'Node\.js'],
        'Express': [r'Express'],
    }
    
    # Programming languages / frameworks
    FRAMEWORK_SIGNATURES = {
        # PHP
        'PHP': [r'X-Powered-By: PHP/(\d+\.\d+\.\d+)', r'php'],
        'Laravel': [r'X-Powered-By: Laravel', r'Laravel', r'__laravel', r'laravel_session'],
        'Symfony': [r'Symfony', r'__symfony'],
        'CodeIgniter': [r'CodeIgniter', r'ci_session'],
        'WordPress': [r'wp-content', r'wp-includes', r'wordpress', r'WordPress'],
        'Drupal': [r'Drupal', r'X-Drupal-Cache', r'drupal'],
        'Joomla': [r'Joomla', r'X-Joomla-Cache'],
        'Magento': [r'Magento', r'X-Magento'],
        'PrestaShop': [r'PrestaShop'],
        
        # Python
        'Django': [r'X-Django', r'django', r'csrftoken'],
        'Flask': [r'Flask', r'flask'],
        'FastAPI': [r'FastAPI'],
        'Pyramid': [r'Pyramid'],
        'Tornado': [r'Tornado'],
        
        # Ruby
        'Ruby on Rails': [r'Rails', r'X-Rails'],
        'Sinatra': [r'Sinatra'],
        
        # Java
        'Spring': [r'Spring', r'X-Application-Context'],
        'JSF': [r'JSF', r'JavaServer Faces'],
        'Struts': [r'Struts'],
        'Play': [r'Play Framework'],
        
        # JavaScript (Node.js)
        'Next.js': [r'Next.js', r'X-Nextjs'],
        'Nuxt.js': [r'Nuxt.js'],
        'Gatsby': [r'Gatsby'],
        'Vue.js': [r'vue', r'__vue__'],
        'React': [r'react', r'React'],
        'Angular': [r'angular', r'ng-'],
        'jQuery': [r'jquery', r'jQuery'],
        
        # .NET
        'ASP.NET': [r'X-AspNet', r'ASP.NET', r'__VIEWSTATE'],
        'ASP.NET MVC': [r'ASP.NET MVC'],
        'Blazor': [r'Blazor'],
    }
    
    # CMS signatures
    CMS_SIGNATURES = {
        'WordPress': {
            'headers': [],
            'html': [r'wp-content', r'wp-includes', r'WordPress'],
            'meta': [r'generator" content="WordPress'],
            'paths': ['/wp-admin', '/wp-login.php', '/wp-json']
        },
        'Drupal': {
            'headers': ['X-Drupal-Cache', 'X-Drupal-Dynamic-Cache'],
            'html': [r'drupal', r'Drupal'],
            'meta': [r'generator" content="Drupal'],
            'paths': ['/user', '/node', '/sites/default']
        },
        'Joomla': {
            'headers': ['X-Joomla-Cache'],
            'html': [r'joomla', r'Joomla'],
            'meta': [r'generator" content="Joomla'],
            'paths': ['/administrator', '/index.php?option=']
        },
        'Magento': {
            'headers': ['X-Magento'],
            'html': [r'magento', r'Magento'],
            'meta': [],
            'paths': ['/admin', '/skin/frontend', '/media/catalog']
        },
        'PrestaShop': {
            'headers': [],
            'html': [r'prestashop', r'PrestaShop'],
            'meta': [r'generator" content="PrestaShop'],
            'paths': ['/admin', '/modules', '/themes']
        },
        'Shopify': {
            'headers': ['X-Shopify'],
            'html': [r'shopify'],
            'meta': [],
            'paths': []
        },
        'Wix': {
            'headers': ['X-Wix'],
            'html': [r'Wix'],
            'meta': [],
            'paths': []
        },
        'Squarespace': {
            'headers': [],
            'html': [r'Squarespace'],
            'meta': [],
            'paths': []
        },
    }
    
    # Analytics & tracking
    ANALYTICS_SIGNATURES = {
        'Google Analytics': [r'google-analytics', r'ga\.js', r'gtag'],
        'Google Tag Manager': [r'googletagmanager'],
        'Facebook Pixel': [r'fbq\(', r'connect\.facebook\.net'],
        'Hotjar': [r'hotjar'],
        'Mixpanel': [r'mixpanel'],
        'Segment': [r'segment\.com'],
        'Amplitude': [r'amplitude'],
        'Matomo': [r'matomo', r'piwik'],
        'Cloudflare': [r'cloudflare'],
        'New Relic': [r'newrelic'],
    }
    
    # CDN signatures
    CDN_SIGNATURES = {
        'Cloudflare': [r'cloudflare'],
        'Akamai': [r'akamai'],
        'Fastly': [r'fastly'],
        'AWS CloudFront': [r'cloudfront'],
        'Azure CDN': [r'azure\.com'],
        'Google Cloud CDN': [r'gstatic\.com', r'googleapis\.com'],
        'StackPath': [r'stackpath'],
        'KeyCDN': [r'keycdn'],
    }
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.response = None
        self.headers = None
        self.html = None
        self.technologies = []
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        self.final_url = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def normalize_url(self, url):
        """Normalize and validate URL"""
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
            
        parsed = urlparse(url)
        self.parsed_url = parsed
        self.domain = parsed.netloc
        self.url = url
        
        return url
        
    def fetch_page(self, url):
        """Fetch page headers and content"""
        try:
            response = requests.get(
                url,
                timeout=15,
                verify=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                allow_redirects=True
            )
            
            self.response = response
            self.headers = response.headers
            self.html = response.text
            self.final_url = response.url
            
            return True
            
        except requests.exceptions.SSLError:
            # Fallback to HTTP
            try:
                http_url = url.replace('https://', 'http://')
                response = requests.get(
                    http_url,
                    timeout=15,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    allow_redirects=True
                )
                
                self.response = response
                self.headers = response.headers
                self.html = response.text
                self.final_url = response.url
                self.url = http_url
                
                return True
            except:
                return False
                
        except Exception as e:
            return False
            
    def detect_server(self):
        """Detect web server software"""
        server_header = self.headers.get('Server', '')
        
        for server, patterns in self.SERVER_SIGNATURES.items():
            for pattern in patterns:
                match = re.search(pattern, server_header, re.IGNORECASE)
                if match:
                    version = match.group(1) if len(match.groups()) > 0 and match.group(1) else None
                    self.technologies.append({
                        'category': 'Web Server',
                        'name': server,
                        'version': version,
                        'confidence': 'HIGH',
                        'evidence': f'Server header: {server_header}'
                    })
                    return server, version
                    
        if server_header:
            self.technologies.append({
                'category': 'Web Server',
                'name': server_header.split('/')[0],
                'version': server_header.split('/')[1] if '/' in server_header else None,
                'confidence': 'MEDIUM',
                'evidence': f'Server header: {server_header}'
            })
            
        return None, None
        
    def detect_frameworks(self):
        """Detect programming languages and frameworks"""
        # Check headers
        for header, value in self.headers.items():
            header_lower = header.lower()
            value_lower = value.lower()
            
            for framework, patterns in self.FRAMEWORK_SIGNATURES.items():
                for pattern in patterns:
                    if isinstance(pattern, str):
                        if pattern.lower() in header_lower or pattern.lower() in value_lower:
                            self.technologies.append({
                                'category': 'Framework',
                                'name': framework,
                                'confidence': 'HIGH',
                                'evidence': f'Header: {header}: {value[:50]}'
                            })
                            break
                            
        # Check HTML
        if self.html:
            html_lower = self.html.lower()
            
            for framework, patterns in self.FRAMEWORK_SIGNATURES.items():
                for pattern in patterns:
                    if isinstance(pattern, str) and pattern.lower() in html_lower:
                        # Avoid duplicate detection
                        if not any(t['name'] == framework for t in self.technologies):
                            self.technologies.append({
                                'category': 'Framework',
                                'name': framework,
                                'confidence': 'MEDIUM',
                                'evidence': f'HTML contains: {pattern}'
                            })
                            break
                            
    def detect_cms(self):
        """Detect Content Management Systems"""
        if not self.html:
            return
            
        html_lower = self.html.lower()
        
        for cms, signatures in self.CMS_SIGNATURES.items():
            detected = False
            
            # Check headers
            for header in signatures['headers']:
                if header in self.headers:
                    self.technologies.append({
                        'category': 'CMS',
                        'name': cms,
                        'confidence': 'HIGH',
                        'evidence': f'Header: {header}'
                    })
                    detected = True
                    break
                    
            if detected:
                continue
                
            # Check HTML patterns
            for pattern in signatures['html']:
                if pattern.lower() in html_lower:
                    self.technologies.append({
                        'category': 'CMS',
                        'name': cms,
                        'confidence': 'HIGH',
                        'evidence': f'HTML contains: {pattern}'
                    })
                    detected = True
                    break
                    
            if detected:
                continue
                
            # Check meta tags
            for pattern in signatures['meta']:
                if pattern.lower() in html_lower:
                    self.technologies.append({
                        'category': 'CMS',
                        'name': cms,
                        'confidence': 'HIGH',
                        'evidence': f'Meta tag: {pattern}'
                    })
                    break
                    
    def detect_analytics(self):
        """Detect analytics and tracking services"""
        if not self.html:
            return
            
        html_lower = self.html.lower()
        
        for service, patterns in self.ANALYTICS_SIGNATURES.items():
            for pattern in patterns:
                if pattern.lower() in html_lower:
                    self.technologies.append({
                        'category': 'Analytics',
                        'name': service,
                        'confidence': 'HIGH',
                        'evidence': f'Script contains: {pattern}'
                    })
                    break
                    
    def detect_cdn(self):
        """Detect CDN services"""
        if not self.html:
            return
            
        html_lower = self.html.lower()
        
        for cdn, patterns in self.CDN_SIGNATURES.items():
            for pattern in patterns:
                if pattern.lower() in html_lower:
                    self.technologies.append({
                        'category': 'CDN',
                        'name': cdn,
                        'confidence': 'HIGH',
                        'evidence': f'Resource URL contains: {pattern}'
                    })
                    break
                    
    def check_headers(self):
        """Check for additional technology indicators in headers"""
        tech_headers = {
            'X-Powered-By': 'Framework',
            'X-Generator': 'CMS/Generator',
            'Via': 'Proxy/CDN',
            'X-Varnish': 'Varnish Cache',
            'X-Cache': 'Cache',
            'CF-Ray': 'Cloudflare',
            'X-CloudFront-ID': 'AWS CloudFront',
            'X-Akamai-Transformed': 'Akamai',
            'X-Fastly-Request-ID': 'Fastly',
        }
        
        for header, category in tech_headers.items():
            if header in self.headers:
                value = self.headers[header]
                self.technologies.append({
                    'category': category,
                    'name': header,
                    'value': value[:50],
                    'confidence': 'MEDIUM',
                    'evidence': f'Header: {header}: {value[:50]}'
                })
                
    def detect_all(self):
        """Run all detection methods"""
        self.technologies = []
        
        # Run detections
        self.detect_server()
        self.detect_frameworks()
        self.detect_cms()
        self.detect_analytics()
        self.detect_cdn()
        self.check_headers()
        
        # Deduplicate
        unique_techs = {}
        for tech in self.technologies:
            key = f"{tech['category']}:{tech['name']}"
            if key not in unique_techs or unique_techs[key]['confidence'] == 'MEDIUM' and tech['confidence'] == 'HIGH':
                unique_techs[key] = tech
                
        self.technologies = list(unique_techs.values())
        
        return self.technologies
        
    def generate_report(self):
        """Generate comprehensive technology detection report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] TECHNOLOGY STACK REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        # Fix: Use self.final_url if available, otherwise use self.url
        final_url = self.final_url if self.final_url else self.url
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Final URL: {Fore.LIGHTGREEN_EX}{final_url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Status Code: {Fore.LIGHTGREEN_EX}{self.response.status_code if self.response else 'N/A'}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Response Size: {Fore.LIGHTGREEN_EX}{len(self.html) if self.html else 0} bytes{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ TECHNOLOGY STACK ============
        if self.technologies:
            print(f"\n{Fore.CYAN}[ DETECTED TECHNOLOGIES ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            
            # Group by category
            categories = {}
            for tech in self.technologies:
                category = tech['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(tech)
                
            # Display by category
            for category, techs in sorted(categories.items()):
                print(f"\n  {Fore.YELLOW}{category}:{Style.RESET_ALL}")
                
                for tech in techs:
                    name = tech['name']
                    version = tech.get('version', '')
                    confidence = tech['confidence']
                    
                    if confidence == 'HIGH':
                        conf_color = Fore.GREEN
                    elif confidence == 'MEDIUM':
                        conf_color = Fore.YELLOW
                    else:
                        conf_color = Fore.WHITE
                        
                    version_str = f" v{version}" if version else ""
                    print(f"    {Fore.WHITE}• {name}{version_str}{Style.RESET_ALL}")
                    print(f"      └─ Confidence: {conf_color}{confidence}{Style.RESET_ALL}")
                    
                    if 'evidence' in tech:
                        evidence = tech['evidence']
                        if len(evidence) > 60:
                            evidence = evidence[:60] + '...'
                        print(f"      └─ Evidence: {Fore.CYAN}{evidence}{Style.RESET_ALL}")
                        
        else:
            print(f"\n  {Fore.YELLOW}[!] No technologies detected{Style.RESET_ALL}")
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"tech_stack_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'url': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'status_code': self.response.status_code if self.response else None,
            'technologies': self.technologies,
            'headers': dict(self.headers) if self.headers else {}
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_detect(self):
        """Interactive technology detection mode"""
        print(f"{Fore.GREEN}[*] Technology Stack Detector initialized{Style.RESET_ALL}\n")
        
        # Get URL
        url_input = input(f"{Fore.YELLOW}[?] Enter URL to analyze: {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No URL specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Fetching {self.url}...{Style.RESET_ALL}")
        
        self.start_time = datetime.now()
        
        # Fetch page
        if not self.fetch_page(self.url):
            print(f"{Fore.RED}[✗] Failed to fetch URL{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}[✓] Page fetched successfully ({len(self.html)} bytes){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Analyzing technology stack...{Style.RESET_ALL}\n")
        
        # Detect technologies
        self.detect_all()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            self.export_report()
            
        print(f"\n{Fore.GREEN}[✓] Technology detection completed{Style.RESET_ALL}")


def detect_technology(url=None):
    """Main entry point for CLI compatibility"""
    detector = TechnologyStackDetector()
    
    # Display banner
    detector.print_header()
    
    if url:
        # Direct scan mode
        detector.normalize_url(url)
        detector.start_time = datetime.now()
        
        print(f"\n  {Fore.YELLOW}[*] Detecting technology stack for {url}...{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] Fetching and analyzing page{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[i] This may take 5-15 seconds{Style.RESET_ALL}\n")
        
        if detector.fetch_page(detector.url):
            detector.detect_all()
            detector.end_time = datetime.now()
            detector.generate_report()
    else:
        # Interactive mode
        detector.interactive_detect()


if __name__ == "__main__":
    detect_technology()