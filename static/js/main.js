/**
 * MINDLESS-REDOPS :: WEB INTERFACE
 * Main JavaScript for Async Tool Execution
 * Clean output formatter - NO ANSI CODES
 * Author: ICAT Project | Linxploit.xyz
 */

// ============================================
// GLOBAL STATE
// ============================================

const Mindless = {
    currentJobId: null,
    pollingInterval: null,
    resultsElement: null,
    loadingElement: null,
    formElement: null,
    
    // Tool category mapping
    categories: {
        network: {
            port_scan: { name: 'Smart Port Scanner', inputs: ['target'] },
            host_discovery: { name: 'Live Host Discovery', inputs: ['subnet'] },
            ssl_tls: { name: 'SSL/TLS Inspector', inputs: ['host'] },
            waf_detect: { name: 'WAF Detector', inputs: ['url'] },
            ip_reputation: { name: 'IP Reputation Checker', inputs: ['ip'] }
        },
        recon: {
            whois: { name: 'WHOIS Intelligence', inputs: ['domain'] },
            dns: { name: 'DNS Recon Mapper', inputs: ['domain'] },
            subdomain: { name: 'Subdomain Enumerator', inputs: ['domain'] },
            tech_stack: { name: 'Technology Stack Detector', inputs: ['url'] },
            email_headers: { name: 'Email Header Analyzer', inputs: ['headers'] },
            certificate: { name: 'Certificate Intelligence', inputs: ['domain'] }
        },
        websec: {
            headers: { name: 'HTTP Security Headers', inputs: ['url'] },
            directory_fuzzer: { name: 'Directory Fuzzer', inputs: ['url'] },
            cors: { name: 'CORS Checker', inputs: ['url'] },
            xss: { name: 'XSS Reflection Test', inputs: ['url'] },
            file_upload: { name: 'File Upload Risk Analyzer', inputs: ['url'] }
        },
        threat: {
            phishing: { name: 'Phishing URL Analyzer', inputs: ['url'] },
            hash: { name: 'Hash Analyzer', inputs: ['hash'] },
            ioc: { name: 'IOC Scanner', inputs: ['text'] },
            brand: { name: 'Brand Impersonation', inputs: ['text'] },
            pastebin: { name: 'Pastebin Leak Monitor', inputs: ['query'] }
        },
        utilities: {
            ip_info: { name: 'IP Information', inputs: ['ip'] },
            email_validator: { name: 'Email Validator', inputs: ['email'] },
            password_strength: { name: 'Password Strength', inputs: ['password'], sensitive: true },
            base64_encode: { name: 'Base64 Encode', inputs: ['text'] },
            base64_decode: { name: 'Base64 Decode', inputs: ['encoded'] },
            user_agent: { name: 'User-Agent Generator', inputs: ['count'] },
            qr_code: { name: 'QR Code Generator', inputs: ['url'] }
        }
    }
};

// ============================================
// ANSI STRIPPER - CLEAN OUTPUT
// ============================================

/**
 * Strip ALL ANSI escape codes from terminal output
 */
Mindless.stripAnsi = function(text) {
    if (!text) return '';
    // Remove all ANSI escape sequences - comprehensive pattern
    return text
        .replace(/\u001b\[.*?m/g, '')   // ESC [ ... m
        .replace(/\u009b.*?m/g, '')      // CSI
        .replace(/\\x1b\[.*?m/g, '')     // \x1b[ ... m
        .replace(/\[.*?m/g, '')        // literal ESC
        .replace(/\[\d+m/g, '')          // [1m, [31m, etc
        .replace(/\[0m/g, '')           // reset
        .replace(/\[1m/g, '')           // bold
        .replace(/\[31m/g, '')          // red
        .replace(/\[32m/g, '')          // green
        .replace(/\[33m/g, '')          // yellow
        .replace(/\[34m/g, '')          // blue
        .replace(/\[35m/g, '')          // magenta
        .replace(/\[36m/g, '')          // cyan
        .replace(/\[37m/g, '')          // white
        .replace(/\[90m/g, '')          // bright black
        .replace(/\[91m/g, '')          // bright red
        .replace(/\[92m/g, '')          // bright green
        .replace(/\[93m/g, '')          // bright yellow
        .replace(/\[94m/g, '')          // bright blue
        .replace(/\[95m/g, '')          // bright magenta
        .replace(/\[96m/g, '')          // bright cyan
        .replace(/\[97m/g, '');         // bright white
};

/**
 * Format output for clean HTML display - NO ANSI CODES
 */
Mindless.formatOutput = function(text) {
    if (!text) return '';
    
    // First strip ALL ANSI codes
    let clean = this.stripAnsi(text);
    
    // Then add clean HTML formatting based on content patterns
    clean = clean
        // Headers and separators - make them clean
        .replace(/^═+$/gm, '<span style="color: var(--accent-cyan); display: block; margin: 10px 0;">$&</span>')
        .replace(/^─+$/gm, '<span style="color: var(--accent-cyan); display: block; margin: 10px 0;">$&</span>')
        
        // Box drawing characters - preserve but style
        .replace(/^╔.+╗$/gm, '<span style="color: var(--accent-red); display: block;">$&</span>')
        .replace(/^╚.+╝$/gm, '<span style="color: var(--accent-red); display: block;">$&</span>')
        .replace(/^║.+$/gm, '<span style="color: var(--accent-red);">$&</span>')
        
        // Section headers
        .replace(/^\[ (?:[A-Z\s]+) \]$/gm, function(match) {
            return `<span style="color: var(--accent-cyan); font-weight: bold; display: block; margin-top: 15px;">${match}</span>`;
        })
        .replace(/^\[(?:CRITICAL|HIGH|MEDIUM|LOW|INFO)\]/gm, function(match) {
            let color = 'var(--accent-red)';
            if (match.includes('HIGH')) color = 'var(--accent-red)';
            else if (match.includes('MEDIUM')) color = 'var(--accent-yellow)';
            else if (match.includes('LOW')) color = 'var(--accent-cyan)';
            else if (match.includes('INFO')) color = 'var(--accent-green)';
            else color = 'var(--accent-red)';
            return `<span style="color: ${color}; font-weight: bold;">${match}</span>`;
        })
        
        // Status indicators
        .replace(/\[✓\]/g, '<span style="color: var(--accent-green); font-weight: bold;">[✓]</span>')
        .replace(/\[\*\]/g, '<span style="color: var(--accent-cyan);">[*]</span>')
        .replace(/\[!\]/g, '<span style="color: var(--accent-yellow); font-weight: bold;">[!]</span>')
        .replace(/\[✗\]/g, '<span style="color: var(--accent-red); font-weight: bold;">[✗]</span>')
        .replace(/\[i\]/g, '<span style="color: var(--accent-cyan);">[i]</span>')
        .replace(/\[>\]/g, '<span style="color: var(--accent-cyan);">[>]</span>')
        
        // Severity levels
        .replace(/\b(CRITICAL)\b/g, '<span style="color: var(--accent-red); font-weight: bold; background: rgba(255, 59, 63, 0.1); padding: 2px 6px; border-radius: 3px;">$1</span>')
        .replace(/\b(HIGH)\b/g, '<span style="color: var(--accent-red); font-weight: bold;">$1</span>')
        .replace(/\b(MEDIUM)\b/g, '<span style="color: var(--accent-yellow); font-weight: bold;">$1</span>')
        .replace(/\b(LOW)\b/g, '<span style="color: var(--accent-cyan);">$1</span>')
        .replace(/\b(INFO)\b/g, '<span style="color: var(--accent-green);">$1</span>')
        
        // Status values
        .replace(/\b(SUCCESS|COMPLETED|VALID|PASS|ENABLED|OPEN|READY)\b/g, '<span style="color: var(--accent-green); font-weight: bold;">$1</span>')
        .replace(/\b(FAILED|ERROR|INVALID|EXPIRED|DISABLED|CLOSED|BLOCKED)\b/g, '<span style="color: var(--accent-red); font-weight: bold;">$1</span>')
        .replace(/\b(WARNING|CAUTION|EXPIRING|SUSPICIOUS)\b/g, '<span style="color: var(--accent-yellow); font-weight: bold;">$1</span>')
        .replace(/\b(DETECTED|FOUND|INFO|NOTICE)\b/g, '<span style="color: var(--accent-cyan);">$1</span>')
        
        // Domain names, IPs, URLs
        .replace(/\b([a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b/g, '<span style="color: var(--accent-cyan);">$1</span>')
        .replace(/\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/g, '<span style="color: var(--accent-green);">$1</span>')
        .replace(/\b(https?:\/\/[^\s]+)\b/g, '<span style="color: var(--accent-cyan); text-decoration: underline;">$1</span>')
        
        // Key-value pairs
        .replace(/^(\s*)([A-Za-z\s]+):/gm, '$1<span style="color: var(--text-secondary);">$2:</span>')
        
        // File paths
        .replace(/\b([A-Za-z]:\\[^\s]+|\/[^\s]+)\b/g, '<span style="color: var(--accent-yellow);">$1</span>')
        
        // Numbers (ports, counts, etc)
        .replace(/\b(\d+)\b/g, '<span style="color: var(--accent-green);">$1</span>')
        
        // Tree structure characters
        .replace(/├─/g, '<span style="color: var(--accent-cyan);">├─</span>')
        .replace(/└─/g, '<span style="color: var(--accent-cyan);">└─</span>')
        .replace(/│/g, '<span style="color: var(--accent-cyan);">│</span>')
        .replace(/─/g, '<span style="color: var(--accent-cyan);">─</span>');
    
    return clean;
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Format timestamp to readable string
 */
Mindless.formatTimestamp = function(timestamp) {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
};

/**
 * Escape HTML to prevent XSS
 */
Mindless.escapeHtml = function(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

/**
 * Show loading animation
 */
Mindless.showLoading = function(element) {
    if (!element) return;
    element.innerHTML = `
        <div class="loading">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>
        <div style="text-align: center; margin-top: 20px; color: var(--accent-cyan); font-family: monospace;">
            [*] EXECUTING... This may take a few seconds
        </div>
    `;
    element.classList.remove('hidden');
};

/**
 * Hide loading animation
 */
Mindless.hideLoading = function(element) {
    if (!element) return;
    element.innerHTML = '';
    element.classList.add('hidden');
};

/**
 * Show error message
 */
Mindless.showError = function(message, container) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.innerHTML = `
        <strong style="color: var(--accent-red);">[✗] ERROR:</strong> 
        <span style="color: var(--text-primary);">${this.escapeHtml(message)}</span>
    `;
    
    if (container) {
        container.innerHTML = '';
        container.appendChild(errorDiv);
    }
};

/**
 * Show success message
 */
Mindless.showSuccess = function(message, container) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.innerHTML = `
        <strong style="color: var(--accent-green);">[✓] SUCCESS:</strong> 
        <span style="color: var(--text-primary);">${this.escapeHtml(message)}</span>
    `;
    
    if (container) {
        container.appendChild(successDiv);
    }
};

// ============================================
// TOOL EXECUTION
// ============================================

/**
 * Execute a tool via AJAX
 */
Mindless.runTool = function(category, tool, formData) {
    // Show loading
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    
    if (resultsDiv) resultsDiv.innerHTML = '';
    if (loadingDiv) this.showLoading(loadingDiv);
    
    // Prepare request data
    const requestData = {};
    const toolConfig = this.categories[category]?.[tool];
    
    if (toolConfig) {
        toolConfig.inputs.forEach(input => {
            const element = document.getElementById(`${tool}_${input}`);
            if (element) {
                requestData[input] = element.value;
            }
        });
    }
    
    // Make AJAX request
    fetch(`/api/run/${category}/${tool}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        this.currentJobId = data.job_id;
        this.pollJobStatus(data.job_id);
    })
    .catch(error => {
        if (loadingDiv) this.hideLoading(loadingDiv);
        if (resultsDiv) this.showError(error.message, resultsDiv);
    });
};

/**
 * Poll job status
 */
Mindless.pollJobStatus = function(jobId) {
    // Clear existing polling
    if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
    }
    
    // Start polling
    this.pollingInterval = setInterval(() => {
        fetch(`/api/job/${jobId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Update progress based on status
                this.updateJobStatus(data);
                
                // If job completed or failed, stop polling
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(this.pollingInterval);
                    this.pollingInterval = null;
                    this.displayResults(data);
                }
            })
            .catch(error => {
                console.error('Polling error:', error);
                clearInterval(this.pollingInterval);
                this.pollingInterval = null;
                
                const loadingDiv = document.getElementById('loading');
                const resultsDiv = document.getElementById('results');
                if (loadingDiv) this.hideLoading(loadingDiv);
                if (resultsDiv) this.showError(error.message, resultsDiv);
            });
    }, 1000); // Poll every second
};

/**
 * Update job status display
 */
Mindless.updateJobStatus = function(data) {
    const statusElement = document.getElementById('job-status');
    const timeElement = document.getElementById('job-time');
    const progressBar = document.getElementById('progress-bar');
    
    if (statusElement) {
        let statusText = '';
        let statusClass = '';
        
        switch (data.status) {
            case 'pending':
                statusText = '⏳ PENDING';
                statusClass = 'text-yellow';
                break;
            case 'running':
                statusText = '▶ RUNNING';
                statusClass = 'text-cyan';
                break;
            case 'completed':
                statusText = '✓ COMPLETED';
                statusClass = 'text-green';
                break;
            case 'failed':
                statusText = '✗ FAILED';
                statusClass = 'text-red';
                break;
        }
        
        statusElement.innerHTML = `<span class="${statusClass}" style="font-weight: bold;">${statusText}</span>`;
    }
    
    if (timeElement && data.running_time) {
        timeElement.textContent = `${data.running_time.toFixed(1)}s`;
    }
    
    // Update progress bar for long-running tasks
    if (progressBar && data.status === 'running') {
        const currentWidth = parseInt(progressBar.style.width) || 0;
        if (currentWidth < 90) {
            progressBar.style.width = (currentWidth + 2) + '%';
        }
    }
};

/**
 * Display results - CLEAN VERSION - NO ANSI CODES
 */
Mindless.displayResults = function(data) {
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    if (loadingDiv) this.hideLoading(loadingDiv);
    if (!resultsDiv) return;
    
    resultsDiv.innerHTML = '';
    
    if (data.status === 'failed') {
        const errorMsg = data.result?.error || data.error || 'Unknown error';
        this.showError(errorMsg, resultsDiv);
        
        // Also show any output that was captured
        if (data.result?.output) {
            const terminal = document.createElement('div');
            terminal.className = 'results-terminal';
            terminal.style.marginTop = '20px';
            
            const content = document.createElement('div');
            content.className = 'results-content';
            content.style.whiteSpace = 'pre-wrap';
            content.style.fontFamily = 'monospace';
            content.style.fontSize = '13px';
            content.style.lineHeight = '1.6';
            content.style.color = 'var(--accent-yellow)';
            content.innerHTML = this.formatOutput(data.result.output);
            
            terminal.appendChild(content);
            resultsDiv.appendChild(terminal);
        }
        return;
    }
    
    // Create results terminal
    const terminal = document.createElement('div');
    terminal.className = 'results-terminal';
    terminal.style.padding = '20px';
    terminal.style.backgroundColor = '#0a0c0e';
    terminal.style.border = '1px solid var(--border-color)';
    terminal.style.borderRadius = '4px';
    terminal.style.fontFamily = "'Courier New', monospace";
    terminal.style.fontSize = '13px';
    terminal.style.lineHeight = '1.6';
    
    // Header with job info - CLEAN
    const header = document.createElement('div');
    header.className = 'results-header';
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.marginBottom = '20px';
    header.style.paddingBottom = '10px';
    header.style.borderBottom = '1px solid var(--border-color)';
    header.style.color = 'var(--accent-cyan)';
    header.style.fontWeight = 'bold';
    header.innerHTML = `
        <span>
            <span style="color: var(--accent-cyan);">[ JOB ${this.currentJobId || 'EXEC'} ]</span>
            <span style="color: var(--accent-green); margin-left: 10px;">✓ COMPLETED</span>
        </span>
        <span style="color: var(--text-secondary);">Duration: ${data.duration || 0}s</span>
    `;
    terminal.appendChild(header);
    
    // Content - CLEAN, NO ANSI CODES
    const content = document.createElement('div');
    content.className = 'results-content';
    content.style.whiteSpace = 'pre-wrap';
    content.style.wordWrap = 'break-word';
    content.style.fontFamily = "'Courier New', monospace";
    content.style.fontSize = '13px';
    content.style.lineHeight = '1.6';
    content.style.color = '#e6e6e6';
    
    // Get output from result
    let outputText = '';
    if (data.result && data.result.output) {
        outputText = data.result.output;
    } else if (data.result && data.result.result) {
        outputText = JSON.stringify(data.result.result, null, 2);
    } else {
        outputText = 'No output generated';
    }
    
    // FORMAT THE OUTPUT - STRIP ANSI CODES AND ADD CLEAN HTML
    content.innerHTML = this.formatOutput(outputText);
    
    terminal.appendChild(content);
    resultsDiv.appendChild(terminal);
    
    // Add export buttons
    const exportDiv = document.createElement('div');
    exportDiv.className = 'btn-group mt-20';
    exportDiv.style.display = 'flex';
    exportDiv.style.gap = '10px';
    exportDiv.style.marginTop = '20px';
    exportDiv.innerHTML = `
        <button class="btn btn-success" onclick="Mindless.exportResults('json')" style="padding: 8px 16px;">
            <i class="fas fa-file-code"></i> JSON
        </button>
        <button class="btn btn-success" onclick="Mindless.exportResults('txt')" style="padding: 8px 16px;">
            <i class="fas fa-file-alt"></i> TXT
        </button>
        <button class="btn" onclick="Mindless.copyResults()" style="padding: 8px 16px;">
            <i class="fas fa-copy"></i> COPY
        </button>
    `;
    resultsDiv.appendChild(exportDiv);
};

/**
 * Export results to file
 */
Mindless.exportResults = function(format) {
    const resultsDiv = document.getElementById('results');
    const terminal = resultsDiv?.querySelector('.results-terminal');
    const content = terminal?.querySelector('.results-content')?.innerText || 
                    terminal?.innerText || 
                    'No results';
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `mindless_export_${timestamp}.${format}`;
    
    // Strip ANSI codes from exported content
    const cleanContent = this.stripAnsi(content);
    
    const blob = new Blob([cleanContent], { type: format === 'json' ? 'application/json' : 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
};

/**
 * Copy results to clipboard
 */
Mindless.copyResults = function() {
    const resultsDiv = document.getElementById('results');
    const terminal = resultsDiv?.querySelector('.results-terminal');
    const content = terminal?.querySelector('.results-content')?.innerText || 
                    terminal?.innerText || 
                    'No results';
    
    // Strip ANSI codes before copying
    const cleanContent = this.stripAnsi(content);
    
    navigator.clipboard.writeText(cleanContent).then(() => {
        alert('Results copied to clipboard!');
    }).catch(() => {
        alert('Failed to copy to clipboard');
    });
};

/**
 * Initialize tool forms
 */
Mindless.initToolForms = function() {
    // Add event listeners to all tool buttons
    document.querySelectorAll('[data-tool]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const category = button.dataset.category;
            const tool = button.dataset.tool;
            this.runTool(category, tool);
        });
    });
    
    // Initialize form validation
    document.querySelectorAll('.tool-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Validate required fields
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--accent-red)';
                    isValid = false;
                } else {
                    field.style.borderColor = 'var(--border-color)';
                }
            });
            
            if (isValid) {
                const category = form.dataset.category;
                const tool = form.dataset.tool;
                this.runTool(category, tool);
            }
        });
    });
};

/**
 * Initialize tooltips
 */
Mindless.initTooltips = function() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = e.target.dataset.tooltip;
            // Tooltip CSS handles the rest
        });
    });
};

/**
 * Initialize progress bars
 */
Mindless.initProgressBars = function() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const targetWidth = bar.dataset.width || '0';
        setTimeout(() => {
            bar.style.width = targetWidth + '%';
        }, 100);
    });
};

/**
 * Initialize ASCII art responsive sizing
 */
Mindless.initAsciiArt = function() {
    const asciiArt = document.querySelector('.ascii-art');
    if (asciiArt) {
        const containerWidth = asciiArt.parentElement.clientWidth;
        if (containerWidth < 600) {
            asciiArt.style.fontSize = '8px';
        }
    }
};

/**
 * Initialize password visibility toggles
 */
Mindless.initPasswordToggles = function() {
    document.querySelectorAll('.toggle-password').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = document.querySelector(this.dataset.target);
            const icon = this.querySelector('i');
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });
};

/**
 * Download QR code
 */
Mindless.downloadQRCode = function() {
    const img = document.getElementById('qr-code-image');
    if (img && img.src) {
        const link = document.createElement('a');
        link.download = 'mindless-qrcode.png';
        link.href = img.src;
        link.click();
    }
};

// ============================================
// DOCUMENT READY
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    Mindless.initToolForms();
    Mindless.initTooltips();
    Mindless.initProgressBars();
    Mindless.initAsciiArt();
    Mindless.initPasswordToggles();
    
    // Handle window resize for ASCII art
    window.addEventListener('resize', Mindless.initAsciiArt);
});