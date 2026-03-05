#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: FILE UPLOAD RISK ANALYZER
Advanced File Upload Security Assessment & Configuration Auditor
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

class FileUploadRiskAnalyzer:
    """Advanced file upload security analyzer - passive analysis only"""
    
    BANNER = f"""
{Fore.RED}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════════╗
    ║  ███████╗██╗██╗     ███████╗    ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗  ║
    ║  ██╔════╝██║██║     ██╔════╝    ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗ ║
    ║  █████╗  ██║██║     █████╗      ██║   ██║██████╔╝██║     ██║   ██║███████║██████╔╝ ║
    ║  ██╔══╝  ██║██║     ██╔══╝      ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██╔══██╗ ║
    ║  ██║     ██║███████╗███████╗    ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██║  ██║ ║
    ║  ╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║
    ║                    {Fore.CYAN}FILE UPLOAD RISK ANALYZER v2.0{Fore.RED}                ║
    ║                    {Fore.YELLOW}[ PASSIVE ANALYSIS - NO UPLOAD ]{Fore.RED}            ║
    ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    
    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = {
        'php': 'PHP script - RCE risk',
        'php3': 'PHP script - RCE risk',
        'php4': 'PHP script - RCE risk',
        'php5': 'PHP script - RCE risk',
        'phtml': 'PHP script - RCE risk',
        'phps': 'PHP source - info disclosure',
        'asp': 'ASP script - RCE risk',
        'aspx': 'ASP.NET script - RCE risk',
        'asax': 'ASP.NET app file - RCE risk',
        'ascx': 'ASP.NET control - RCE risk',
        'ashx': 'ASP.NET handler - RCE risk',
        'asmx': 'ASP.NET web service - RCE risk',
        'aspq': 'ASP.NET script - RCE risk',
        'jsp': 'Java Server Page - RCE risk',
        'jspx': 'Java Server Page - RCE risk',
        'cfm': 'ColdFusion script - RCE risk',
        'cfml': 'ColdFusion script - RCE risk',
        'pl': 'Perl script - RCE risk',
        'py': 'Python script - RCE risk',
        'rb': 'Ruby script - RCE risk',
        'sh': 'Shell script - RCE risk',
        'exe': 'Executable - malware risk',
        'dll': 'Dynamic library - malware risk',
        'so': 'Shared object - malware risk',
        'dmg': 'macOS installer - malware risk',
        'pif': 'Program information file - malware risk',
        'scr': 'Screensaver - executable risk',
        'hta': 'HTML application - RCE risk',
        'msi': 'Windows installer - malware risk',
        'vbs': 'VBScript - RCE risk',
        'vbe': 'VBScript encrypted - RCE risk',
        'js': 'JavaScript - XSS risk',
        'jse': 'JScript encrypted - RCE risk',
        'wsf': 'Windows script file - RCE risk',
        'wsh': 'Windows script host - RCE risk',
        'ps1': 'PowerShell script - RCE risk',
        'ps1xml': 'PowerShell script - RCE risk',
        'ps2': 'PowerShell script - RCE risk',
        'ps2xml': 'PowerShell script - RCE risk',
        'psc1': 'PowerShell console - RCE risk',
        'psc2': 'PowerShell console - RCE risk',
        'msh': 'Monad shell - RCE risk',
        'msh1': 'Monad shell - RCE risk',
        'msh2': 'Monad shell - RCE risk',
        'mshxml': 'Monad shell - RCE risk',
        'msh1xml': 'Monad shell - RCE risk',
        'msh2xml': 'Monad shell - RCE risk',
        'scf': 'Windows explorer command - RCE risk',
        'lnk': 'Shortcut - malware risk',
        'inf': 'Setup information - malware risk',
        'reg': 'Registry entry - malware risk',
        'svg': 'SVG with script - XSS risk',
        'html': 'HTML file - XSS/phishing risk',
        'htm': 'HTML file - XSS/phishing risk',
        'xhtml': 'HTML file - XSS/phishing risk',
        'xml': 'XML file - XXE risk',
        'xss': 'Cross-site scripting - XSS risk',
    }
    
    # File upload security indicators
    SECURITY_INDICATORS = {
        'client_side_validation': {
            'positive': ['accept="', 'accept=', 'onchange="validate', 'onchange="check'],
            'negative': ['No client-side validation'],
            'description': 'Client-side file validation'
        },
        'file_size_limit': {
            'positive': ['maxlength', 'data-max-size', 'data-max-file-size', 'MAX_FILE_SIZE'],
            'negative': ['No file size limit detected'],
            'description': 'File size restrictions'
        },
        'file_type_restriction': {
            'positive': ['accept="image/', 'accept=".pdf', 'accept=".doc', 'accept="image/*'],
            'negative': ['No file type restrictions'],
            'description': 'File type whitelisting'
        },
        'csrf_protection': {
            'positive': ['csrf', 'token', '_token', 'authenticity_token'],
            'negative': ['No CSRF token detected'],
            'description': 'CSRF protection'
        }
    }
    
    def __init__(self):
        self.url = None
        self.parsed_url = None
        self.domain = None
        self.base_url = None
        self.html_content = None
        self.response_headers = {}
        self.upload_forms = []
        self.security_analysis = {}
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = None
        self.end_time = None
        
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
        
        # Store base URL without path
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.url = url
        
        return url
        
    def fetch_page(self, url):
        """Fetch HTML content from URL"""
        try:
            response = requests.get(
                url,
                timeout=15,
                verify=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                allow_redirects=True
            )
            
            self.html_content = response.text
            self.response_headers = response.headers
            self.final_url = response.url
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to fetch page: {e}{Style.RESET_ALL}")
            return False
            
    def find_upload_forms(self):
        """Find and analyze file upload forms"""
        forms = []
        
        if not self.html_content:
            return forms
            
        # Find all form tags
        form_pattern = r'<form.*?</form>'
        form_matches = re.findall(form_pattern, self.html_content, re.DOTALL | re.IGNORECASE)
        
        for form_html in form_matches:
            # Check if form has file input
            if 'type="file"' in form_html.lower() or "type='file'" in form_html.lower():
                form_data = self.analyze_form(form_html)
                forms.append(form_data)
                
        self.upload_forms = forms
        return forms
        
    def analyze_form(self, form_html):
        """Analyze a single form for security properties"""
        form_data = {
            'action': '',
            'method': 'GET',
            'enctype': '',
            'file_inputs': [],
            'security_features': [],
            'vulnerabilities': [],
            'raw_html': form_html[:200] + '...' if len(form_html) > 200 else form_html
        }
        
        # Extract form action
        action_match = re.search(r'action=[\'"](.*?)[\'"]', form_html, re.IGNORECASE)
        if action_match:
            action = action_match.group(1)
            # Resolve relative URLs
            if action.startswith('/'):
                form_data['action'] = self.base_url + action
            elif action.startswith('http'):
                form_data['action'] = action
            else:
                form_data['action'] = self.url.rstrip('/') + '/' + action.lstrip('/')
        else:
            form_data['action'] = self.url  # Submit to same page
            
        # Extract form method
        method_match = re.search(r'method=[\'"](.*?)[\'"]', form_html, re.IGNORECASE)
        form_data['method'] = method_match.group(1).upper() if method_match else 'GET'
        
        # Extract enctype
        enctype_match = re.search(r'enctype=[\'"](.*?)[\'"]', form_html, re.IGNORECASE)
        form_data['enctype'] = enctype_match.group(1) if enctype_match else 'application/x-www-form-urlencoded'
        
        # Find file inputs
        input_pattern = r'<input.*?>'
        input_matches = re.findall(input_pattern, form_html, re.IGNORECASE)
        
        for input_html in input_matches:
            if 'type="file"' in input_html.lower() or "type='file'" in input_html.lower():
                file_input = {
                    'name': '',
                    'accept': '',
                    'multiple': False,
                    'required': False
                }
                
                # Extract name
                name_match = re.search(r'name=[\'"](.*?)[\'"]', input_html, re.IGNORECASE)
                if name_match:
                    file_input['name'] = name_match.group(1)
                    
                # Extract accept attribute
                accept_match = re.search(r'accept=[\'"](.*?)[\'"]', input_html, re.IGNORECASE)
                if accept_match:
                    file_input['accept'] = accept_match.group(1)
                    
                # Check for multiple attribute
                file_input['multiple'] = 'multiple' in input_html.lower()
                
                # Check for required attribute
                file_input['required'] = 'required' in input_html.lower()
                
                form_data['file_inputs'].append(file_input)
                
        # Analyze security features
        self.analyze_security_features(form_data, form_html)
        
        return form_data
        
    def analyze_security_features(self, form_data, form_html):
        """Analyze form for security features"""
        features = []
        
        # Check for CSRF tokens
        csrf_patterns = ['csrf', 'token', '_token', 'authenticity_token', 'csrf_token', 'xsrf']
        for pattern in csrf_patterns:
            if pattern in form_html.lower():
                features.append({
                    'feature': 'CSRF Protection',
                    'evidence': f'Contains "{pattern}" parameter',
                    'status': 'GOOD'
                })
                break
                
        # Check for MAX_FILE_SIZE
        if 'max_file_size' in form_html.lower() or 'MAX_FILE_SIZE' in form_html:
            features.append({
                'feature': 'File Size Limit',
                'evidence': 'MAX_FILE_SIZE hidden field detected',
                'status': 'GOOD'
            })
            
        # Check for file type restrictions
        for file_input in form_data['file_inputs']:
            if file_input['accept']:
                if 'image/' in file_input['accept'] or 'video/' in file_input['accept'] or 'audio/' in file_input['accept']:
                    features.append({
                        'feature': 'File Type Restriction',
                        'evidence': f"Accept: {file_input['accept']}",
                        'status': 'GOOD'
                    })
                else:
                    features.append({
                        'feature': 'File Type Restriction',
                        'evidence': f"Accept: {file_input['accept']}",
                        'status': 'WARNING'
                    })
                    
        # Check form method
        if form_data['method'] == 'POST':
            features.append({
                'feature': 'POST Method',
                'evidence': 'Form uses POST method',
                'status': 'GOOD'
            })
        else:
            features.append({
                'feature': 'POST Method',
                'evidence': 'Form uses GET method - insecure for file uploads',
                'status': 'CRITICAL'
            })
            
        # Check enctype
        if form_data['enctype'] == 'multipart/form-data':
            features.append({
                'feature': 'Proper Encoding',
                'evidence': 'multipart/form-data encoding',
                'status': 'GOOD'
            })
        else:
            features.append({
                'feature': 'Proper Encoding',
                'evidence': f"{form_data['enctype']} - may not support file uploads properly",
                'status': 'CRITICAL'
            })
            
        form_data['security_features'] = features
        
    def assess_risks(self):
        """Assess security risks of found upload forms"""
        risk_assessment = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }
        
        for form in self.upload_forms:
            # Check for missing CSRF
            csrf_found = any(f['feature'] == 'CSRF Protection' for f in form['security_features'])
            if not csrf_found:
                risk_assessment['high'].append({
                    'form': form['action'],
                    'risk': 'Missing CSRF Protection',
                    'description': 'File upload form lacks anti-CSRF token - vulnerable to cross-site request forgery',
                    'remediation': 'Implement CSRF tokens for all state-changing operations'
                })
                
            # Check for GET method
            if form['method'] == 'GET':
                risk_assessment['critical'].append({
                    'form': form['action'],
                    'risk': 'GET Method for File Upload',
                    'description': 'Form uses GET method - file uploads should always use POST',
                    'remediation': 'Change form method to POST'
                })
                
            # Check for proper encoding
            if form['enctype'] != 'multipart/form-data':
                risk_assessment['critical'].append({
                    'form': form['action'],
                    'risk': 'Improper Form Encoding',
                    'description': f"Form uses {form['enctype']} instead of multipart/form-data",
                    'remediation': 'Set enctype="multipart/form-data"'
                })
                
            # Check file input restrictions
            for file_input in form['file_inputs']:
                if not file_input['accept']:
                    risk_assessment['high'].append({
                        'form': form['action'],
                        'input': file_input['name'],
                        'risk': 'Missing File Type Restrictions',
                        'description': 'No accept attribute - allows any file type',
                        'remediation': 'Implement file type whitelisting using accept attribute and server-side validation'
                    })
                elif '*' in file_input['accept']:
                    risk_assessment['medium'].append({
                        'form': form['action'],
                        'input': file_input['name'],
                        'risk': 'Broad File Type Restriction',
                        'description': f"Accept: {file_input['accept']} - may be too permissive",
                        'remediation': 'Specify exact MIME types instead of wildcards'
                    })
                    
            # Check for multiple file upload
            for file_input in form['file_inputs']:
                if file_input['multiple']:
                    risk_assessment['medium'].append({
                        'form': form['action'],
                        'input': file_input['name'],
                        'risk': 'Multiple File Upload',
                        'description': 'Form allows multiple file uploads - increases attack surface',
                        'remediation': 'Restrict to single file upload unless necessary'
                    })
                    
        return risk_assessment
        
    def generate_report(self):
        """Generate comprehensive file upload risk report"""
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] FILE UPLOAD RISK ASSESSMENT - {self.scan_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Target URL: {Fore.LIGHTGREEN_EX}{self.url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Domain: {Fore.LIGHTGREEN_EX}{self.domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Started: {Fore.LIGHTGREEN_EX}{self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Scan Completed: {Fore.LIGHTGREEN_EX}{self.end_time}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.LIGHTGREEN_EX}{(self.end_time - self.start_time).total_seconds():.2f}s{Style.RESET_ALL}")
        
        # ============ UPLOAD FORM SUMMARY ============
        print(f"\n{Fore.CYAN}[ UPLOAD FORM SUMMARY ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        if not self.upload_forms:
            print(f"\n  {Fore.GREEN}[✓] No file upload forms detected{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}The target page does not contain any file upload functionality{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
            return
            
        print(f"\n  {Fore.YELLOW}[!] Found {len(self.upload_forms)} file upload form(s){Style.RESET_ALL}")
        
        for i, form in enumerate(self.upload_forms, 1):
            print(f"\n  {Fore.CYAN}Form #{i}:{Style.RESET_ALL}")
            print(f"  ├─ Action: {Fore.WHITE}{form['action']}{Style.RESET_ALL}")
            print(f"  ├─ Method: {Fore.YELLOW}{form['method']}{Style.RESET_ALL}")
            print(f"  ├─ Encoding: {Fore.WHITE}{form['enctype']}{Style.RESET_ALL}")
            print(f"  └─ File Inputs: {len(form['file_inputs'])}")
            
            for j, file_input in enumerate(form['file_inputs'], 1):
                print(f"     {j}. Name: {Fore.CYAN}{file_input['name']}{Style.RESET_ALL}")
                if file_input['accept']:
                    print(f"        Accept: {Fore.WHITE}{file_input['accept']}{Style.RESET_ALL}")
                if file_input['multiple']:
                    print(f"        {Fore.YELLOW}[!] Multiple files allowed{Style.RESET_ALL}")
                    
        # ============ SECURITY FEATURES ============
        print(f"\n{Fore.CYAN}[ SECURITY FEATURES DETECTED ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        for i, form in enumerate(self.upload_forms, 1):
            print(f"\n  {Fore.CYAN}Form #{i} Security Controls:{Style.RESET_ALL}")
            
            if form['security_features']:
                for feature in form['security_features']:
                    status = feature['status']
                    if status == 'GOOD':
                        status_color = Fore.GREEN
                    elif status == 'WARNING':
                        status_color = Fore.YELLOW
                    else:
                        status_color = Fore.RED
                        
                    print(f"  ├─ {status_color}[{status}]{Style.RESET_ALL} {feature['feature']}")
                    print(f"  │   └─ {Fore.WHITE}{feature['evidence']}{Style.RESET_ALL}")
            else:
                print(f"  └─ {Fore.RED}[CRITICAL] No security features detected{Style.RESET_ALL}")
                
        # ============ RISK ASSESSMENT ============
        risks = self.assess_risks()
        
        if any(risks.values()):
            print(f"\n{Fore.CYAN}[ RISK ASSESSMENT ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Critical risks
            if risks['critical']:
                print(f"\n  {Fore.RED}[CRITICAL RISKS]{Style.RESET_ALL}")
                for risk in risks['critical']:
                    print(f"  ├─ {risk['risk']}")
                    print(f"  │  ├─ Location: {Fore.WHITE}{risk['form']}{Style.RESET_ALL}")
                    print(f"  │  ├─ Description: {Fore.WHITE}{risk['description']}{Style.RESET_ALL}")
                    print(f"  │  └─ Remediation: {Fore.GREEN}{risk['remediation']}{Style.RESET_ALL}")
                    
            # High risks
            if risks['high']:
                print(f"\n  {Fore.RED}[HIGH RISKS]{Style.RESET_ALL}")
                for risk in risks['high']:
                    print(f"  ├─ {risk['risk']}")
                    print(f"  │  ├─ Location: {Fore.WHITE}{risk['form']}{Style.RESET_ALL}")
                    if 'input' in risk:
                        print(f"  │  ├─ Input: {Fore.WHITE}{risk['input']}{Style.RESET_ALL}")
                    print(f"  │  ├─ Description: {Fore.WHITE}{risk['description']}{Style.RESET_ALL}")
                    print(f"  │  └─ Remediation: {Fore.GREEN}{risk['remediation']}{Style.RESET_ALL}")
                    
            # Medium risks
            if risks['medium']:
                print(f"\n  {Fore.YELLOW}[MEDIUM RISKS]{Style.RESET_ALL}")
                for risk in risks['medium']:
                    print(f"  ├─ {risk['risk']}")
                    print(f"  │  ├─ Location: {Fore.WHITE}{risk['form']}{Style.RESET_ALL}")
                    print(f"  │  ├─ Description: {Fore.WHITE}{risk['description']}{Style.RESET_ALL}")
                    print(f"  │  └─ Remediation: {Fore.GREEN}{risk['remediation']}{Style.RESET_ALL}")
                    
        # ============ SECURE UPLOAD CHECKLIST ============
        print(f"\n{Fore.CYAN}[ SECURE FILE UPLOAD CHECKLIST ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"""
  {Fore.WHITE}✓{Style.RESET_ALL} Use POST method for uploads
  {Fore.WHITE}✓{Style.RESET_ALL} Set enctype="multipart/form-data"
  {Fore.WHITE}✓{Style.RESET_ALL} Implement CSRF protection
  {Fore.WHITE}✓{Style.RESET_ALL} Validate file type on server (MIME, extension)
  {Fore.WHITE}✓{Style.RESET_ALL} Validate file content (magic bytes)
  {Fore.WHITE}✓{Style.RESET_ALL} Set file size limits
  {Fore.WHITE}✓{Style.RESET_ALL} Store files outside webroot
  {Fore.WHITE}✓{Style.RESET_ALL} Use randomized filenames
  {Fore.WHITE}✓{Style.RESET_ALL} Scan files for malware
  {Fore.WHITE}✓{Style.RESET_ALL} Set proper CORS policies
  {Fore.WHITE}✓{Style.RESET_ALL} Implement rate limiting
  {Fore.WHITE}✓{Style.RESET_ALL} Log all upload attempts
        """)
        
        # ============ RECOMMENDATIONS ============
        if self.upload_forms:
            print(f"\n{Fore.CYAN}[ RECOMMENDATIONS ]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            recommendations = []
            
            # Check for missing CSRF
            if risks['high'] and any(r['risk'] == 'Missing CSRF Protection' for r in risks['high']):
                recommendations.append("Add CSRF tokens to all file upload forms")
                
            # Check for GET method
            if risks['critical'] and any(r['risk'] == 'GET Method for File Upload' for r in risks['critical']):
                recommendations.append("Change upload form method from GET to POST")
                
            # Check for missing accept attributes
            if risks['high'] and any(r['risk'] == 'Missing File Type Restrictions' for r in risks['high']):
                recommendations.append("Implement file type whitelisting on both client and server side")
                
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {rec}")
            else:
                print(f"  {Fore.GREEN}[✓] No critical recommendations - good security posture{Style.RESET_ALL}")
                
        print(f"\n{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] IMPORTANT: This is a PASSIVE analysis only{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    No files were uploaded or modified{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Server-side validation cannot be tested passively{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}")
        
    def export_report(self, filename=None):
        """Export results to JSON"""
        if not filename:
            filename = f"upload_audit_{self.domain}_{self.scan_id}.json"
            
        report = {
            'scan_id': self.scan_id,
            'target': self.url,
            'domain': self.domain,
            'timestamp': str(self.start_time),
            'duration': (self.end_time - self.start_time).total_seconds(),
            'upload_forms_found': len(self.upload_forms),
            'upload_forms': self.upload_forms,
            'risk_assessment': self.assess_risks(),
            'response_headers': dict(self.response_headers)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4, default=str)
            print(f"{Fore.GREEN}[✓] Report exported to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Export failed: {e}{Style.RESET_ALL}")
            
    def interactive_scan(self):
        """Interactive file upload risk analysis mode"""
        print(f"{Fore.GREEN}[*] File Upload Risk Analyzer initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] PASSIVE MODE - No files will be uploaded{Style.RESET_ALL}\n")
        
        # Get target
        url_input = input(f"{Fore.YELLOW}[?] Enter URL with file upload form: {Style.RESET_ALL}").strip()
        
        if not url_input:
            print(f"{Fore.RED}[✗] No target specified{Style.RESET_ALL}")
            return
            
        self.normalize_url(url_input)
        
        print(f"\n{Fore.YELLOW}[*] Analyzing file upload security on {self.url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Fetching page content...{Style.RESET_ALL}\n")
        
        self.start_time = datetime.now()
        
        # Fetch page
        if not self.fetch_page(self.url):
            return
            
        # Find upload forms
        print(f"{Fore.CYAN}[*] Scanning for file upload forms...{Style.RESET_ALL}")
        self.find_upload_forms()
        
        self.end_time = datetime.now()
        
        # Generate report
        self.generate_report()
        
        # Export option
        if self.upload_forms:
            export = input(f"\n{Fore.YELLOW}[?] Export results to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
            if export == 'y':
                self.export_report()
                
        print(f"\n{Fore.GREEN}[✓] File upload risk analysis completed{Style.RESET_ALL}")


def analyze_file_upload_risk(url=None):
    """Main entry point for CLI compatibility"""
    analyzer = FileUploadRiskAnalyzer()
    
    # Display banner
    analyzer.print_header()
    
    if url:
        # Direct scan mode
        analyzer.normalize_url(url)
        analyzer.start_time = datetime.now()
        analyzer.fetch_page(analyzer.url)
        analyzer.find_upload_forms()
        analyzer.end_time = datetime.now()
        analyzer.generate_report()
    else:
        # Interactive mode
        analyzer.interactive_scan()


if __name__ == "__main__":
    analyze_file_upload_risk()
