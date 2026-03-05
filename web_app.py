#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: WEB INTERFACE
Professional Red Team Operations Framework - Web Edition
Author: ICAT Project | Linxploit.xyz
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os
import json
import threading
import queue
import uuid
from datetime import datetime
import secrets
import builtins
from io import StringIO

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================
# GLOBAL OUTPUT CAPTURE - FIX FOR WEB DISPLAY
# ============================================

# Store original print
original_print = builtins.print

# Global variable to store captured output
_CAPTURED_OUTPUT = ""

def web_print(*args, **kwargs):
    """Custom print that captures output for web"""
    global _CAPTURED_OUTPUT
    
    # Convert args to string
    output = ' '.join(str(arg) for arg in args)
    
    # Add to captured output
    _CAPTURED_OUTPUT += output + '\n'
    
    # Also print to console for debugging
    original_print(*args, **kwargs)

# Replace print with our web version
builtins.print = web_print

# ============================================
# LAZY LOADING CACHE - Same as CLI version
# ============================================

_MODULE_CACHE = {}

def lazy_import(module_path, function_name):
    """Import a module only when needed and cache it"""
    cache_key = f"{module_path}.{function_name}"
    
    if cache_key not in _MODULE_CACHE:
        try:
            module = __import__(module_path, fromlist=[function_name])
            _MODULE_CACHE[cache_key] = getattr(module, function_name)
        except Exception as e:
            print(f"[!] Failed to load {module_path}.{function_name}: {e}")
            _MODULE_CACHE[cache_key] = None
    
    return _MODULE_CACHE[cache_key]

# ============================================
# MODULE LOADERS - Same as CLI version
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

# Recon modules
def get_whois_lookup():
    return lazy_import('modules.recon.whois_intelligence', 'whois_lookup')

def get_dns_recon():
    return lazy_import('modules.recon.dns_recon_mapper', 'dns_recon')

def get_subdomain_enum():
    return lazy_import('modules.recon.subdomain_enumerator', 'subdomain_enum')

def get_detect_technology():
    return lazy_import('modules.recon.technology_stack_detector', 'detect_technology')

def get_analyze_email_headers():
    return lazy_import('modules.recon.email_header_analyzer', 'analyze_email_headers')

def get_certificate_intelligence():
    return lazy_import('modules.recon.certificate_intelligence', 'certificate_intelligence')

# ============================================
# FLASK APPLICATION
# ============================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Store job results
job_results = {}

# ============================================
# ASYNC JOB HANDLER - WITH OUTPUT CAPTURE
# ============================================

class AsyncJob:
    """Handle async execution of tools with output capture"""
    
    def __init__(self, func, *args, **kwargs):
        self.job_id = str(uuid.uuid4())[:8]
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result_queue = queue.Queue()
        self.thread = None
        self.status = "pending"
        self.start_time = datetime.now()
        self.end_time = None
        
    def start(self):
        """Start the job in a background thread"""
        self.status = "running"
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        return self.job_id
        
    def _run(self):
        """Run the function and capture output"""
        global _CAPTURED_OUTPUT
        
        # Clear previous output
        _CAPTURED_OUTPUT = ""
        
        try:
            # Run the function - it will print using our web_print
            result = self.func(*self.args, **self.kwargs)
            
            # Get captured output
            output = _CAPTURED_OUTPUT
            
            self.result_queue.put({
                'status': 'success',
                'output': output,
                'result': result
            })
            self.status = "completed"
            
        except Exception as e:
            self.result_queue.put({
                'status': 'error',
                'error': str(e),
                'output': _CAPTURED_OUTPUT + f"\nERROR: {str(e)}"
            })
            self.status = "failed"
        finally:
            self.end_time = datetime.now()
            
    def get_result(self):
        """Get job result if available"""
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', 
                         version="2.0.0", 
                         codename="Red Harbor",
                         now=datetime.now)

# ============================================
# MODULE CATEGORY PAGES
# ============================================

@app.route('/recon')
def recon_page():
    """Reconnaissance tools page"""
    return render_template('recon.html', now=datetime.now)

@app.route('/network')
def network_page():
    """Network security tools page"""
    return render_template('network.html', now=datetime.now)

@app.route('/websec')
def websec_page():
    """Web security tools page"""
    return render_template('websec.html', now=datetime.now)

@app.route('/threat')
def threat_page():
    """Threat intelligence tools page"""
    return render_template('threat.html', now=datetime.now)

@app.route('/utilities')
def utilities_page():
    """Utilities tools page"""
    return render_template('utilities.html', now=datetime.now)

# ============================================
# API ENDPOINTS - Execute tools asynchronously
# ============================================

@app.route('/api/run/<category>/<tool>', methods=['POST'])
def run_tool(category, tool):
    """Execute a tool asynchronously"""
    data = request.json
    job = None
    
    # ============ NETWORK TOOLS ============
    if category == 'network':
        if tool == 'port_scan':
            func = get_smart_port_scan()
            job = AsyncJob(func, data.get('target'))
        elif tool == 'host_discovery':
            func = get_live_host_discovery()
            job = AsyncJob(func, data.get('subnet'))
        elif tool == 'ssl_tls':
            func = get_inspect_ssl_tls()
            job = AsyncJob(func, data.get('host'))
        elif tool == 'waf_detect':
            func = get_detect_firewall_waf()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'ip_reputation':
            func = get_check_ip_reputation()
            job = AsyncJob(func, data.get('ip'))
    
    # ============ RECON TOOLS ============
    elif category == 'recon':
        if tool == 'whois':
            func = get_whois_lookup()
            job = AsyncJob(func, data.get('domain'))
        elif tool == 'dns':
            func = get_dns_recon()
            job = AsyncJob(func, data.get('domain'))
        elif tool == 'subdomain':
            func = get_subdomain_enum()
            job = AsyncJob(func, data.get('domain'))
        elif tool == 'tech_stack':
            func = get_detect_technology()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'email_headers':
            func = get_analyze_email_headers()
            job = AsyncJob(func, data.get('headers'))
        elif tool == 'certificate':
            func = get_certificate_intelligence()
            job = AsyncJob(func, data.get('domain'))
    
    # ============ WEB SECURITY TOOLS ============
    elif category == 'websec':
        if tool == 'headers':
            func = get_analyze_headers()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'directory_fuzzer':
            func = get_directory_fuzzer()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'cors':
            func = get_check_cors_misconfig()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'xss':
            func = get_xss_reflection_test()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'file_upload':
            func = get_analyze_file_upload_risk()
            job = AsyncJob(func, data.get('url'))
    
    # ============ THREAT INTELLIGENCE ============
    elif category == 'threat':
        if tool == 'phishing':
            func = get_phishing_check()
            job = AsyncJob(func, data.get('url'))
        elif tool == 'hash':
            func = get_hash_analysis()
            job = AsyncJob(func, data.get('hash'))
        elif tool == 'ioc':
            func = get_malicious_indicator_scan()
            job = AsyncJob(func, data.get('text'))
        elif tool == 'brand':
            func = get_brand_impersonation()
            job = AsyncJob(func, data.get('text'))
        elif tool == 'pastebin':
            func = get_pastebin_leak_monitor()
            job = AsyncJob(func, data.get('query'))
    
    # ============ UTILITIES ============
    elif category == 'utilities':
        if tool == 'ip_info':
            func = get_ip_info()
            job = AsyncJob(func, data.get('ip'))
        elif tool == 'email_validator':
            func = get_email_validator()
            job = AsyncJob(func, data.get('email'))
        elif tool == 'password_strength':
            func = get_password_strength_check()
            job = AsyncJob(func, data.get('password'))
        elif tool == 'base64_encode':
            func = get_base64_encode()
            job = AsyncJob(func, data.get('text'))
        elif tool == 'base64_decode':
            func = get_base64_decode()
            job = AsyncJob(func, data.get('encoded'))
        elif tool == 'user_agent':
            func = get_user_agent_generator()
            count = int(data.get('count', 1))
            job = AsyncJob(func, count=count)
        elif tool == 'qr_code':
            func = get_url_to_qr()
            job = AsyncJob(func, data.get('url'))
    
    if job:
        job_id = job.start()
        job_results[job_id] = job
        return jsonify({'job_id': job_id, 'status': 'started'})
    
    return jsonify({'error': 'Tool not found'}), 404

# ============================================
# JOB STATUS ENDPOINT
# ============================================

@app.route('/api/job/<job_id>')
def job_status(job_id):
    """Get job status and result"""
    job = job_results.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    result = job.get_result()
    if result:
        # Calculate duration
        duration = (job.end_time - job.start_time).total_seconds() if job.end_time else 0
        
        return jsonify({
            'status': job.status,
            'result': result,
            'duration': round(duration, 2),
            'start_time': job.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': job.end_time.strftime('%Y-%m-%d %H:%M:%S') if job.end_time else None
        })
    
    # Still running
    return jsonify({
        'status': job.status,
        'running_time': (datetime.now() - job.start_time).total_seconds()
    })

# ============================================
# QR CODE STATIC FILES
# ============================================

@app.route('/static/qrcodes/<filename>')
def serve_qrcode(filename):
    """Serve generated QR codes"""
    from flask import send_from_directory
    return send_from_directory('static/qrcodes', filename)


# ============================================
# WIFI TOOLS ROUTES
# ============================================

@app.route('/wifi')
def wifi_page():
    """WiFi Tools main page"""
    return render_template('wifi_tools.html', now=datetime.now)

@app.route('/api/wifi/scan', methods=['POST'])
def wifi_scan():
    """Scan for ESP8266 devices"""
    from modules.wifi.esp_scanner import ESP8266Scanner
    
    data = request.json
    scanner = ESP8266Scanner()
    
    devices = []
    
    if data.get('method') in ['wifi', 'all']:
        wifi_devices = scanner.scan_wifi_networks(interface=data.get('interface'))
        devices.extend(wifi_devices)
    
    if data.get('method') in ['arp', 'all']:
        arp_devices = scanner.arp_scan_network()
        devices.extend(arp_devices)
    
    if data.get('method') in ['esp', 'all']:
        esp_devices = scanner.find_esp_ips()
        devices.extend(esp_devices)
    
    # Remove duplicates
    unique_devices = []
    seen = set()
    
    for device in devices:
        key = device.get('bssid') or device.get('ip') or device.get('ssid')
        if key and key not in seen:
            seen.add(key)
            unique_devices.append(device)
    
    return jsonify({'devices': unique_devices})

@app.route('/api/wifi/connect', methods=['POST'])
def wifi_connect():
    """Connect to ESP8266 device"""
    from modules.wifi.esp_controller import connect_to_esp
    
    data = request.json
    ip = data.get('ip')
    
    try:
        controller = connect_to_esp(ip)
        return jsonify({
            'status': 'connected',
            'firmware': controller.firmware_type,
            'ip': ip
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wifi/<ip>/info')
def wifi_device_info(ip):
    """Get ESP8266 device info"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    info = controller.get_info()
    
    return jsonify({
        'firmware': controller.firmware_type,
        'info': info
    })

@app.route('/api/wifi/<ip>/attack/<attack_type>', methods=['POST'])
def wifi_start_attack(ip, attack_type):
    """Start WiFi attack"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    result = controller.start_attack(attack_type)
    
    return jsonify(result)

@app.route('/api/wifi/<ip>/stop', methods=['POST'])
def wifi_stop_attack(ip):
    """Stop WiFi attack"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    result = controller.stop_attack()
    
    return jsonify(result)

@app.route('/api/wifi/<ip>/scan')
def wifi_scan_networks(ip):
    """Trigger WiFi scan on ESP8266"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    controller.scan_wifi()
    
    # Get scan results
    results = controller.get_scan_results()
    
    return jsonify({'aps': results})

@app.route('/api/wifi/<ip>/stations')
def wifi_scan_stations(ip):
    """Scan for stations/clients"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    # This would need to be implemented based on firmware
    return jsonify({'stations': []})

@app.route('/api/wifi/<ip>/select/<target_type>', methods=['POST'])
def wifi_select_target(ip, target_type):
    """Select target AP or station"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    data = request.json
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    
    result = controller.select_target(data.get('id'), target_type)
    
    return jsonify(result)

@app.route('/api/wifi/<ip>/ssids')
def wifi_get_ssids(ip):
    """Get SSID list from device"""
    # This would need to be implemented based on firmware
    return jsonify({'ssids': []})

@app.route('/api/wifi/<ip>/ssid/add', methods=['POST'])
def wifi_add_ssid(ip):
    """Add SSID to list"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    data = request.json
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    
    result = controller.add_ssid(data.get('ssid'))
    
    return jsonify(result)

@app.route('/api/wifi/<ip>/ssid/generate', methods=['POST'])
def wifi_generate_ssids(ip):
    """Generate random SSIDs"""
    from modules.wifi.firmware_payloads import generate_beacon_ssids
    
    data = request.json
    count = data.get('count', 10)
    
    ssids = generate_beacon_ssids('default', count)
    
    # Add each SSID to device
    from modules.wifi.esp_controller import ESP8266Controller
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    
    for ssid in ssids:
        controller.add_ssid(ssid)
    
    return jsonify({'ssids': ssids})

@app.route('/api/wifi/<ip>/ssid/clear', methods=['POST'])
def wifi_clear_ssids(ip):
    """Clear all SSIDs"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    
    result = controller.clear_ssids()
    
    return jsonify(result)

@app.route('/api/wifi/<ip>/ssid/remove', methods=['POST'])
def wifi_remove_ssid(ip):
    """Remove SSID from list"""
    # This would need to be implemented based on firmware
    return jsonify({'status': 'ok'})

@app.route('/api/wifi/<ip>/settings', methods=['POST'])
def wifi_save_settings(ip):
    """Save device settings"""
    # This would need to be implemented based on firmware
    return jsonify({'status': 'ok'})

@app.route('/api/wifi/<ip>/config', methods=['POST'])
def wifi_save_config(ip):
    """Save attack configuration"""
    # This would need to be implemented based on firmware
    return jsonify({'status': 'ok'})

@app.route('/api/wifi/<ip>/reboot', methods=['POST'])
def wifi_reboot(ip):
    """Reboot ESP8266 device"""
    from modules.wifi.esp_controller import ESP8266Controller
    
    controller = ESP8266Controller(ip)
    controller.identify_firmware()
    
    result = controller.reboot()
    
    return jsonify(result)

# ============================================
# CLEANUP OLD JOBS
# ============================================

@app.before_request
def cleanup_old_jobs():
    """Remove jobs older than 1 hour"""
    current_time = datetime.now()
    to_remove = []
    for job_id, job in job_results.items():
        if job.end_time and (current_time - job.end_time).total_seconds() > 3600:
            to_remove.append(job_id)
    for job_id in to_remove:
        del job_results[job_id]

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    # Create QR codes directory if it doesn't exist
    os.makedirs('static/qrcodes', exist_ok=True)
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║              MINDLESS-REDOPS :: WEB INTERFACE                  ║
    ║                    Starting Flask Server...                    ║
    ║                                                                ║
    ║           🌐 Local: http://127.0.0.1:5000                     ║
    ║           🌍 Network: http://localhost:5000                   ║
    ║                                                                ║
    ║           Press CTRL+C to stop server                         ║
    ║           ✅ Web output capture ENABLED                        ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)