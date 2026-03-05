#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: BRAND IMPERSONATION DETECTOR
Advanced Brand Abuse & Typosquatting Detection
Author: ICAT Project | Linxploit.xyz
"""

import re
import json
import socket
import whois
import difflib
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse

init(autoreset=True)

class BrandImpersonationDetector:
    """Advanced brand impersonation and typosquatting detection"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██████╗  █████╗ ███╗   ██╗██████╗     ██╗███╗   ███╗██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗ ║
    ║  ██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗    ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║ ║
    ║  ██████╔╝██████╔╝███████║██╔██╗ ██║██║  ██║    ██║██╔████╔██║██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║███████║   ██║   ██║██║   ██║██╔██╗ ██║ ║
    ║  ██╔══██╗██╔══██╗██╔══██║██║╚██╗██║██║  ██║    ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║ ║
    ║  ██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝    ██║██║ ╚═╝ ██║██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║ ║
    ║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ║
    ║                    {Fore.CYAN}BRAND IMPERSONATION DETECTOR v2.0{Fore.RED}               ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Major brands to monitor
    BRAND_DATABASE = {
        'google': {
            'domains': ['google.com', 'gmail.com', 'youtube.com', 'googlemail.com'],
            'keywords': ['google', 'gmail', 'youtube', 'android', 'chrome', 'gmail'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'microsoft': {
            'domains': ['microsoft.com', 'windows.com', 'office.com', 'outlook.com', 'live.com', 'msn.com'],
            'keywords': ['microsoft', 'windows', 'office', 'outlook', 'hotmail', 'msn', 'azure', 'xbox'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'apple': {
            'domains': ['apple.com', 'icloud.com', 'me.com', 'mac.com'],
            'keywords': ['apple', 'icloud', 'iphone', 'ipad', 'mac', 'itunes', 'appstore'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'amazon': {
            'domains': ['amazon.com', 'aws.amazon.com', 'amazonaws.com', 'primevideo.com', 'audible.com'],
            'keywords': ['amazon', 'aws', 'prime', 'kindle', 'alexa', 'audible'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'facebook': {
            'domains': ['facebook.com', 'fb.com', 'instagram.com', 'whatsapp.com', 'messenger.com'],
            'keywords': ['facebook', 'fb', 'instagram', 'whatsapp', 'messenger', 'meta'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'twitter': {
            'domains': ['twitter.com', 't.co'],
            'keywords': ['twitter', 'tweet', 'twit'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'paypal': {
            'domains': ['paypal.com', 'paypal.me'],
            'keywords': ['paypal', 'paypal'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'netflix': {
            'domains': ['netflix.com'],
            'keywords': ['netflix'],
            'severity': 'HIGH',
            'color': Fore.RED
        },
        'linkedin': {
            'domains': ['linkedin.com'],
            'keywords': ['linkedin', 'linkedin'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'github': {
            'domains': ['github.com'],
            'keywords': ['github', 'git'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'adobe': {
            'domains': ['adobe.com'],
            'keywords': ['adobe', 'photoshop', 'acrobat'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'dropbox': {
            'domains': ['dropbox.com'],
            'keywords': ['dropbox'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'spotify': {
            'domains': ['spotify.com'],
            'keywords': ['spotify'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'ebay': {
            'domains': ['ebay.com'],
            'keywords': ['ebay'],
            'severity': 'HIGH',
            'color': Fore.YELLOW
        },
        'bankofamerica': {
            'domains': ['bankofamerica.com'],
            'keywords': ['bankofamerica', 'boa', 'bofa'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'wellsfargo': {
            'domains': ['wellsfargo.com'],
            'keywords': ['wellsfargo'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'chase': {
            'domains': ['chase.com'],
            'keywords': ['chase'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        },
        'capitalone': {
            'domains': ['capitalone.com'],
            'keywords': ['capitalone'],
            'severity': 'CRITICAL',
            'color': Fore.RED
        }
    }
    
    # Typosquatting patterns
    TYPOSQUATTING_PATTERNS = [
        # Missing character
        (r'gogle', 'google'),
        (r'googl', 'google'),
        (r'microsof', 'microsoft'),
        (r'micrsoft', 'microsoft'),
        (r'appl', 'apple'),
        (r'amzon', 'amazon'),
        (r'facebok', 'facebook'),
        (r'twiter', 'twitter'),
        (r'paypal', 'paypal'),
        
        # Extra character
        (r'gooogle', 'google'),
        (r'microsoftt', 'microsoft'),
        (r'applee', 'apple'),
        (r'amazoon', 'amazon'),
        
        # Character substitution
        (r'g00gle', 'google'),
        (r'm1cr0s0ft', 'microsoft'),
        (r'4pple', 'apple'),
        (r'4m4zon', 'amazon'),
        (r'f4ceb00k', 'facebook'),
        
        # Common TLD abuse
        (r'google\.(com\.)?[a-z]{2}$', 'google'),
        (r'microsoft\.(com\.)?[a-z]{2}$', 'microsoft'),
        (r'apple\.(com\.)?[a-z]{2}$', 'apple'),
        
        # Homograph attacks (simplified)
        (r'gооgle', 'google'),  # Cyrillic 'o'
        (r'аpple', 'apple'),    # Cyrillic 'a'
        (r'раypal', 'paypal'),  # Cyrillic 'p' and 'a'
    ]
    
    def __init__(self):
        self.input_text = None
        self.input_type = None
        self.input_name = None
        self.detections = []
        self.scan_summary = {
            'total_detections': 0,
            'by_brand': {},
            'by_severity': {}
        }
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        """Display professional banner"""
        print(self.BANNER)
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def load_input(self, text, input_type='text', input_name=None):
        """Load input for scanning"""
        self.input_text = text
        self.input_type = input_type
        self.input_name = input_name or 'Unknown Source'
        
    def extract_domains(self):
        """Extract domains from text"""
        domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        return list(set(re.findall(domain_pattern, self.input_text, re.IGNORECASE)))
        
    def extract_urls(self):
        """Extract URLs from text"""
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[-\w$.+!*\'(),;:@&=?/~#%]*)?'
        return list(set(re.findall(url_pattern, self.input_text, re.IGNORECASE)))
        
    def calculate_similarity(self, domain, brand_domain):
        """Calculate string similarity between domain and brand domain"""
        return difflib.SequenceMatcher(None, domain.lower(), brand_domain.lower()).ratio()
        
    def detect_brand_mentions(self):
        """Detect direct brand mentions"""
        for brand, info in self.BRAND_DATABASE.items():
            for keyword in info['keywords']:
                # Check for standalone word
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, self.input_text, re.IGNORECASE):
                    self.detections.append({
                        'brand': brand.capitalize(),
                        'type': 'Direct Mention',
                        'indicator': keyword,
                        'severity': 'INFO',
                        'description': f'Direct mention of {brand.capitalize()} brand',
                        'recommendation': 'Legitimate use - no action required',
                        'context': self.get_context(keyword)
                    })
                    break
                    
    def detect_typosquatting(self):
        """Detect typosquatting attempts"""
        domains = self.extract_domains()
        urls = self.extract_urls()
        
        # Check domains
        for domain in domains:
            domain_lower = domain.lower()
            
            # Check against brand domains
            for brand, info in self.BRAND_DATABASE.items():
                for brand_domain in info['domains']:
                    # Check for exact match of brand domain
                    if domain_lower == brand_domain:
                        self.detections.append({
                            'brand': brand.capitalize(),
                            'type': 'Legitimate Domain',
                            'indicator': domain,
                            'severity': 'INFO',
                            'description': f'Legitimate {brand.capitalize()} domain',
                            'recommendation': 'No action required',
                            'context': self.get_context(domain)
                        })
                        break
                        
                    # Check for subdomain of brand domain
                    elif domain_lower.endswith('.' + brand_domain):
                        self.detections.append({
                            'brand': brand.capitalize(),
                            'type': 'Subdomain',
                            'indicator': domain,
                            'severity': 'LOW',
                            'description': f'Subdomain of {brand.capitalize()}',
                            'recommendation': 'Verify subdomain ownership',
                            'context': self.get_context(domain)
                        })
                        break
                        
                    # Check for typosquatting
                    elif brand_domain in domain_lower or domain_lower in brand_domain:
                        similarity = self.calculate_similarity(domain_lower, brand_domain)
                        
                        if similarity > 0.7 and similarity < 1.0:
                            severity = 'HIGH' if similarity > 0.85 else 'MEDIUM'
                            
                            self.detections.append({
                                'brand': brand.capitalize(),
                                'type': 'Typosquatting',
                                'indicator': domain,
                                'severity': severity,
                                'similarity': f'{similarity:.1%}',
                                'description': f'Domain similar to {brand.capitalize()}',
                                'recommendation': 'Investigate for phishing/brand abuse',
                                'context': self.get_context(domain)
                            })
                            break
                            
        # Check URLs
        for url in urls:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            for brand, info in self.BRAND_DATABASE.items():
                for brand_domain in info['domains']:
                    if brand_domain in domain and domain != brand_domain:
                        self.detections.append({
                            'brand': brand.capitalize(),
                            'type': 'Suspicious URL',
                            'indicator': url,
                            'severity': 'HIGH',
                            'description': f'URL contains {brand.capitalize()} but is not official domain',
                            'recommendation': 'Block and investigate',
                            'context': self.get_context(url)
                        })
                        break
                        
    def detect_pattern_based_abuse(self):
        """Detect pattern-based brand abuse"""
        text_lower = self.input_text.lower()
        
        for pattern, brand in self.TYPOSQUATTING_PATTERNS:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # Get the full match
                if isinstance(match, tuple):
                    match = match[0]
                    
                self.detections.append({
                    'brand': brand.capitalize(),
                    'type': 'Pattern-Based Abuse',
                    'indicator': match,
                    'severity': 'HIGH',
                    'description': f'Known typosquatting pattern for {brand.capitalize()}',
                    'recommendation': 'Block domain and report to brand security team',
                    'context': self.get_context(match)
                })
                
    def detect_suspicious_tlds(self):
        """Detect suspicious TLD usage with brand names"""
        domains = self.extract_domains()
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
        
        for domain in domains:
            domain_lower = domain.lower()
            
            for tld in suspicious_tlds:
                if domain_lower.endswith(tld):
                    # Check if domain contains any brand name
                    for brand, info in self.BRAND_DATABASE.items():
                        for keyword in info['keywords']:
                            if keyword in domain_lower.replace(tld, ''):
                                self.detections.append({
                                    'brand': brand.capitalize(),
                                    'type': 'Suspicious TLD',
                                    'indicator': domain,
                                    'severity': 'CRITICAL',
                                    'description': f'{brand.capitalize()} brand with suspicious TLD {tld}',
                                    'recommendation': 'Immediate investigation and blocking required',
                                    'context': self.get_context(domain)
                                })
                                break
                                
    def get_context(self, indicator, context_chars=50):
        """Get surrounding context for indicator"""
        if not self.input_text:
            return ''
            
        pos = self.input_text.lower().find(indicator.lower())
        if pos == -1:
            return ''
            
        start = max(0, pos - context_chars)
        end = min(len(self.input_text), pos + len(indicator) + context_chars)
        
        context = self.input_text[start:end]
        # Highlight the indicator
        context = context.replace(indicator, f"{Fore.RED}{indicator}{Fore.WHITE}")
        
        return context
        
    def generate_summary(self):
        """Generate scan summary"""
        self.scan_summary = {
            'total_detections': len(self.detections),
            'by_brand': {},
            'by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        }
        
        for detection in self.detections:
            brand = detection['brand']
            severity = detection['severity']
            
            self.scan_summary['by_brand'][brand] = self.scan_summary['by_brand'].get(brand, 0) + 1
            self.scan_summary['by_severity'][severity] = self.scan_summary['by_severity'].get(severity, 0) + 1
            
    def check_domain_registration(self, domain):
        """Check domain registration details via WHOIS"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date),
                'days_old': (datetime.now() - (w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)).days if w.creation_date else 'Unknown'
            }
        except:
            return None
            
    def generate_report(self):
        """Generate comprehensive brand impersonation report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] BRAND IMPERSONATION DETECTION REPORT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Source: {Fore.LIGHTGREEN_EX}{self.input_name}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Input Type: {Fore.LIGHTGREEN_EX}{self.input_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Content Size: {Fore.LIGHTGREEN_EX}{len(self.input_text)} characters{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ SCAN SUMMARY ============
        print(f"\n{Fore.CYAN}[ SCAN SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}Total Detections: {Fore.LIGHTGREEN_EX}{self.scan_summary['total_detections']}{Style.RESET_ALL}")
        
        # Severity breakdown
        print(f"\n  {Fore.WHITE}Severity Breakdown:{Style.RESET_ALL}")
        for severity, count in self.scan_summary['by_severity'].items():
            if count > 0:
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
                    
                print(f"    {color}[{severity}]{Style.RESET_ALL}: {count}")
                
        # Brand breakdown
        if self.scan_summary['by_brand']:
            print(f"\n  {Fore.WHITE}Affected Brands:{Style.RESET_ALL}")
            for brand, count in sorted(self.scan_summary['by_brand'].items(), key=lambda x: x[1], reverse=True):
                brand_info = self.BRAND_DATABASE.get(brand.lower(), {})
                brand_color = brand_info.get('color', Fore.WHITE)
                print(f"    {brand_color}→{Style.RESET_ALL} {brand}: {count}")
                
        # ============ DETECTED IMPERSONATIONS ============
        if self.detections:
            print(f"\n{Fore.CYAN}[ DETECTED IMPERSONATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
            
            # Group by severity
            severity_groups = {}
            for detection in self.detections:
                severity = detection['severity']
                if severity not in severity_groups:
                    severity_groups[severity] = []
                severity_groups[severity].append(detection)
                
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                if severity in severity_groups:
                    if severity == 'CRITICAL':
                        print(f"\n  {Fore.RED}{Style.BRIGHT}[{severity} IMPERSONATIONS]{Style.RESET_ALL}")
                    elif severity == 'HIGH':
                        print(f"\n  {Fore.RED}[{severity} IMPERSONATIONS]{Style.RESET_ALL}")
                    elif severity == 'MEDIUM':
                        print(f"\n  {Fore.YELLOW}[{severity} IMPERSONATIONS]{Style.RESET_ALL}")
                    elif severity == 'LOW':
                        print(f"\n  {Fore.CYAN}[{severity} IMPERSONATIONS]{Style.RESET_ALL}")
                    else:
                        print(f"\n  {Fore.GREEN}[{severity} MENTIONS]{Style.RESET_ALL}")
                        
                    for i, detection in enumerate(severity_groups[severity][:15], 1):
                        brand = detection['brand']
                        brand_info = self.BRAND_DATABASE.get(brand.lower(), {})
                        brand_color = brand_info.get('color', Fore.WHITE)
                        
                        print(f"\n    {i}. {brand_color}{brand}{Style.RESET_ALL} - {detection['type']}")
                        print(f"       ├─ Indicator: {Fore.WHITE}{detection['indicator']}{Style.RESET_ALL}")
                        print(f"       ├─ Description: {Fore.WHITE}{detection['description']}{Style.RESET_ALL}")
                        print(f"       ├─ Recommendation: {Fore.GREEN}{detection['recommendation']}{Style.RESET_ALL}")
                        
                        if 'similarity' in detection:
                            print(f"       ├─ Similarity: {Fore.YELLOW}{detection['similarity']}{Style.RESET_ALL}")
                            
                        if detection.get('context'):
                            print(f"       └─ Context: {detection['context'][:100]}...")
                            
                    if len(severity_groups[severity]) > 15:
                        print(f"\n       ... and {len(severity_groups[severity]) - 15} more detections")
                        
        else:
            print(f"\n  {Fore.GREEN}[✓] No brand impersonation detected{Style.RESET_ALL}")
            
        # ============ DOMAIN INVESTIGATION ============
        suspicious_domains = [d['indicator'] for d in self.detections 
                            if d['type'] in ['Typosquatting', 'Suspicious TLD', 'Suspicious URL']]
        
        if suspicious_domains:
            print(f"\n{Fore.CYAN}[ DOMAIN INVESTIGATION ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"\n  {Fore.YELLOW}[*] Checking suspicious domains...{Style.RESET_ALL}")
            
            for domain in suspicious_domains[:5]:
                # Extract domain from URL if needed
                if domain.startswith('http'):
                    domain = urlparse(domain).netloc
                    
                whois_info = self.check_domain_registration(domain)
                
                if whois_info:
                    print(f"\n    {Fore.WHITE}{domain}{Style.RESET_ALL}")
                    print(f"      ├─ Registrar: {whois_info['registrar']}")
                    print(f"      ├─ Registered: {whois_info['creation_date']}")
                    print(f"      └─ Age: {whois_info['days_old']} days")
                else:
                    print(f"\n    {Fore.WHITE}{domain}{Style.RESET_ALL}")
                    print(f"      └─ {Fore.YELLOW}WHOIS information unavailable{Style.RESET_ALL}")
                    
        # ============ THREAT ASSESSMENT ============
        print(f"\n{Fore.CYAN}[ THREAT ASSESSMENT ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        critical_count = self.scan_summary['by_severity'].get('CRITICAL', 0)
        high_count = self.scan_summary['by_severity'].get('HIGH', 0)
        
        if critical_count > 0:
            print(f"""
  {Fore.RED}{Style.BRIGHT}[!] ACTIVE BRAND IMPERSONATION CAMPAIGN DETECTED{Style.RESET_ALL}
  
  Critical findings indicate:
  • Active typosquatting domains
  • Suspicious TLDs abusing brand names
  • Potential phishing infrastructure
  
  Immediate action required:
  • Block identified domains
  • Contact brand security team
  • Issue takedown requests
  • Alert customers/users
            """)
        elif high_count > 0:
            print(f"""
  {Fore.RED}[!] SUSPICIOUS BRAND ACTIVITY DETECTED{Style.RESET_ALL}
  
  • Multiple potential impersonation attempts
  • Investigate highlighted domains
  • Monitor for phishing campaigns
            """)
        elif self.detections:
            print(f"""
  {Fore.YELLOW}[i] MINOR BRAND MENTIONS DETECTED{Style.RESET_ALL}
  
  • Mostly legitimate mentions
  • Some suspicious patterns found
  • Routine monitoring recommended
            """)
        else:
            print(f"""
  {Fore.GREEN}[✓] NO BRAND IMPERSONATION DETECTED{Style.RESET_ALL}
  
  • No suspicious brand usage found
  • Maintain regular monitoring
  • Update brand keywords regularly
            """)
            
        # ============ RECOMMENDATIONS ============
        if critical_count > 0 or high_count > 0:
            print(f"\n{Fore.CYAN}[ TAKEDOWN PROCEDURE ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"""
  1. Document all infringing domains
  2. Send cease & desist letters
  3. File domain disputes (UDRP)
  4. Report to registrars
  5. Contact hosting providers
  6. Submit to anti-phishing orgs
  7. Monitor for new registrations
            """)
            
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"brand_scan_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'source': self.input_name,
            'input_type': self.input_type,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'summary': self.scan_summary,
            'detections': self.detections
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive brand impersonation scanning mode"""
        print(f"{Fore.GREEN}[*] Brand Impersonation Detector initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Advanced typosquatting and brand abuse detection{Style.RESET_ALL}\n")
        
        # Get input method
        print(f"{Fore.CYAN}Input Options:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Direct text/domain input")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Load from file")
        print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Scan single domain")
        
        choice = input(f"\n{Fore.YELLOW}[?] Select input method: {Style.RESET_ALL}").strip()
        
        content = ""
        content_name = ""
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}[?] Enter text/domains/URLs to scan (Ctrl+D to finish):{Style.RESET_ALL}")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except (EOFError, KeyboardInterrupt):
                content = '\n'.join(lines)
                content_name = "Direct Text Input"
                
        elif choice == "2":
            filename = input(f"{Fore.YELLOW}[?] Enter file path: {Style.RESET_ALL}").strip()
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                content_name = filename
                print(f"{Fore.GREEN}[✓] Loaded {len(content)} characters from {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
                return
                
        elif choice == "3":
            domain = input(f"{Fore.YELLOW}[?] Enter domain to scan: {Style.RESET_ALL}").strip()
            content = domain
            content_name = f"Domain: {domain}"
            
        else:
            print(f"{Fore.RED}[✗] Invalid option{Style.RESET_ALL}")
            return
            
        if not content.strip():
            print(f"{Fore.RED}[✗] No content to scan{Style.RESET_ALL}")
            return
            
        self.load_input(content, input_type='text', input_name=content_name)
        
        print(f"\n{Fore.YELLOW}[*] Scanning for brand impersonation...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Run all detection methods
        self.detect_brand_mentions()
        self.detect_typosquatting()
        self.detect_pattern_based_abuse()
        self.detect_suspicious_tlds()
        
        # Generate summary
        self.generate_summary()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.detections:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] Brand impersonation scan completed{Style.RESET_ALL}")


def brand_impersonation(text=None, filename=None):
    """Main entry point for CLI compatibility"""
    detector = BrandImpersonationDetector()
    
    # Display banner
    detector.print_header()
    
    if filename:
        # Scan file
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            detector.load_input(content, input_type='file', input_name=filename)
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load file: {e}{Style.RESET_ALL}")
            return
    elif text:
        # Direct scan
        detector.load_input(text, input_type='direct', input_name='Direct Input')
    else:
        # Interactive mode
        detector.interactive_scan()
        return
        
    detector.start_time = datetime.now()
    detector.detect_brand_mentions()
    detector.detect_typosquatting()
    detector.detect_pattern_based_abuse()
    detector.detect_suspicious_tlds()
    detector.generate_summary()
    detector.end_time = datetime.now()
    detector.generate_report()


if __name__ == "__main__":
    brand_impersonation()
