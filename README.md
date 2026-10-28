<div align="center">

# 🛡️ Mindless — RedOps Offensive-Security Toolkit

**A modular Python toolkit for reconnaissance, security inspection, and OSINT — with a CLI and a web dashboard, built on the same code.**

[![Python](https://img.shields.io/badge/python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Academic%20%2F%20Educational-blue)](#license)
[![Status](https://img.shields.io/badge/status-active%20development-yellow)](#limitations--roadmap)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Modules](#-module-catalogue) • [Security & Ethics](#-security--ethical-use) • [Contributing](#-contributing)

</div>

---

## Overview

**Mindless** (codename **Mindless-RedOps** / **Red Harbor**) is an academic cybersecurity toolkit for **reconnaissance, analysis, and security inspection**. It bundles 29+ individually useful security modules — the kind of tools a pentester, bug-bounty hunter, SOC analyst, or student would otherwise stitch together from a dozen separate CLI utilities — behind one consistent interface.

It ships with **two front ends built on the same shared module library**:

- 🖥️ An interactive, colour-coded **command-line menu** (`Mindless.py`)
- 🌐 A **Flask web dashboard** with a terminal-inspired UI (`web_app.py`)

> **Most tools are read-only and safe for demonstrations.** A smaller subset (notably the WiFi attack module and the directory fuzzer) perform active probing — see [Security & Ethical Use](#-security--ethical-use) before running anything against a target you don't own.

---

## ✨ Features

- **29+ security modules** across 6 functional domains — recon, network, web security, threat intel, utilities, and WiFi tooling
- **Dual interface, one codebase** — every module is callable from the terminal menu *and* exposed as a REST-style web endpoint
- **Lazy-loaded modules** — heavy dependencies (`dnspython`, `python-whois`, `Pillow`, etc.) are only imported when a tool is actually used, keeping startup fast
- **Async job runner** — the web dashboard runs tools in background threads and streams live console output back to the browser
- **Consistent reporting** — every module prints a readable terminal report and can export results to JSON/text
- **Terminal-themed web UI** — a dark, "hacker" aesthetic (`static/css/hacker.css`) mirrors the CLI's ANSI colour scheme

---

## 📦 Architecture

```
Mindless-main/
├── Mindless.py                  # CLI entry point
├── web_app.py                   # Flask entry point — all web routes & job runner
├── Requirements.txt              # Base CLI dependencies
├── requirements-web.txt          # Extended dependencies for the web dashboard
├── backend/
│   ├── app.py                    # Minimal Flask app factory
│   ├── config.py                 # Secret key + Censys API credentials
│   └── integrations/
│       └── censys_client.py      # Censys host-asset API wrapper
├── cli/
│   ├── banners.py                 # ASCII banners & terminal UI elements
│   └── menu.py                    # Full interactive CLI menu tree
├── modules/
│   ├── recon/                     # WHOIS, DNS, subdomains, certs, tech-stack, email headers
│   ├── network/                   # Port scanning, host discovery, SSL/TLS, WAF, IP reputation
│   ├── websec/                    # Security headers, fuzzing, CORS, XSS, file-upload risk
│   ├── threat_intel/              # Phishing, brand impersonation, IOCs, hashes, paste leaks
│   ├── utilities/                 # Passwords, email validation, IP info, QR, Base64, UA strings
│   ├── wifi/                      # ESP8266 "Deauther" hardware controller
│   └── soc_tools/                 # Log monitor (placeholder / coming soon)
├── static/                        # CSS + JS for the web dashboard
└── templates/                     # Jinja2 templates (one per domain)
```

**How it fits together:**

- `Mindless.py` initialises the terminal UI and hands off to `cli/menu.py`, which renders the banner, status dashboard, and the main menu. Selecting a domain opens a sub-menu that calls the relevant module's entry-point function.
- `web_app.py` serves the dashboard and exposes `POST /api/run/<category>/<tool>`, which starts the requested module on a background thread and returns a job ID. The front end polls `GET /api/job/<job_id>` and streams output back into the page. A dedicated `/api/wifi/*` family of routes drives the WiFi controller.
- Both entry points use a shared **lazy-import pattern** (`lazy_import(module_path, function_name)`) so modules are only loaded the moment they're used — a single broken module can't take down the whole app.

---

## 🚀 Installation

**Requirements:** Python 3.x, pip

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Mindless.git
cd Mindless

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r Requirements.txt           # CLI only
pip install -r requirements-web.txt       # CLI + Web dashboard
```

### Configuration

`backend/config.py` holds the Flask secret key and the optional [Censys](https://censys.io/) API credentials used by `backend/integrations/censys_client.py`. **Before deploying anywhere beyond local/offline use, move these out of source control** — e.g. with `python-dotenv` and environment variables — and rotate the key.

```python
# backend/config.py
SECRET_KEY = "change-this-key"
CENSYS_API_TOKEN = "your-token-here"
```

---

## 🖥️ Usage

### Command-line interface

```bash
python Mindless.py
```

Navigate the numbered menu to pick a domain (Reconnaissance, Network Security, Web Security, Threat Intelligence, Utilities, WiFi, SOC Tools), then a tool within it, and follow the prompts.

### Web dashboard

```bash
python web_app.py
```

Open the printed local URL in your browser for the full dashboard, or hit the API directly:

```bash
curl -X POST http://localhost:5000/api/run/recon/subdomain_enum \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# → { "job_id": "a1b2c3d4" }

curl http://localhost:5000/api/job/a1b2c3d4
# → { "status": "complete", "output": [ "..." ] }
```

### Using a module directly in Python

Every module is also just an importable function:

```python
from modules.recon.subdomain_enumerator import subdomain_enum
from modules.websec.http_security_header_analyzer import analyze_headers

subdomain_enum("example.com")
analyze_headers("https://example.com")
```

---

## 🧩 Module Catalogue

<details>
<summary><b>🔍 Reconnaissance</b> — <code>modules/recon/</code> (6 modules)</summary>

| Module | Description |
|---|---|
| **WHOIS Intelligence** | Domain registration, expiry, registrar and name-server lookups |
| **DNS Recon Mapper** | A/AAAA/MX/NS/TXT/SOA enumeration and reverse DNS mapping |
| **Subdomain Enumerator** | crt.sh Certificate-Transparency mining + DNS brute-forcing + live resolution |
| **Technology Stack Detector** | Fingerprints CMS, frameworks, and server software from headers/markup |
| **Certificate Intelligence** | TLS certificate chain analysis + crt.sh cross-referencing |
| **Email Header Analyzer** | SPF/DKIM/DMARC parsing and hop-by-hop routing reconstruction |

</details>

<details>
<summary><b>🌐 Network Security</b> — <code>modules/network/</code> (5 modules)</summary>

| Module | Description |
|---|---|
| **Smart Port Scanner** | Multi-threaded TCP scanning with banner grabbing |
| **Live Host Discovery** | Subnet/CIDR sweeps using multiple detection methods |
| **SSL/TLS Security Inspector** | Certificate validity and protocol/cipher security checks |
| **Firewall / WAF Detector** | Signature-based WAF and CDN fingerprinting |
| **IP Reputation Checker** | Multi-source IP threat intelligence and geolocation |

</details>

<details>
<summary><b>🔒 Web Application Security</b> — <code>modules/websec/</code> (5 modules)</summary>

| Module | Description |
|---|---|
| **HTTP Security Header Analyzer** | Audits CSP, HSTS, X-Frame-Options and more against best practice |
| **Directory & Endpoint Fuzzer** | Multi-threaded content discovery against common paths |
| **CORS Misconfiguration Checker** | Detects overly-permissive Cross-Origin configurations |
| **XSS Reflection Detector** | Read-only, context-aware reflected-XSS scanning |
| **File Upload Risk Analyzer** | Passive assessment of file-upload surface configuration |

</details>

<details>
<summary><b>🧠 Threat Intelligence</b> — <code>modules/threat_intel/</code> (6 modules)</summary>

| Module | Description |
|---|---|
| **Phishing URL Analyzer** | URL structure + domain age + SSL + Google Safe Browsing composite score |
| **Brand Impersonation Detector** | Typosquatting/homoglyph detection with WHOIS-backed scoring |
| **Malicious Indicator Scanner** | Extracts and classifies IOCs (IPs, domains, hashes, URLs) |
| **Hash Analyzer** | Identifies likely hash algorithm (MD5/SHA-1/SHA-256/…) |
| **Pastebin / Leak Monitor** | Searches public paste sites for data-leak indicators |
| **Pastebin Monitor (legacy)** | Lightweight earlier version of the leak monitor |

</details>

<details>
<summary><b>🛠️ Utilities</b> — <code>modules/utilities/</code> (9 modules)</summary>

| Module | Description |
|---|---|
| **Password Strength Analyzer** | Entropy, composition, pattern, and common-password checks |
| **Email Validator** | Syntax validation + live MX-record resolution |
| **IP Information Finder** | Geolocation and ASN/organisation lookup |
| **URL → QR Code Generator** | Generates a QR code PNG for any URL |
| **Base64 Encoder/Decoder** | Encode/decode with multiple variant handling |
| **User-Agent Generator** | Realistic UA strings with rotation, bulk generation, clipboard copy |
| **Phishing Link Checker** | Lightweight keyword-based heuristic check |

</details>

<details>
<summary><b>📡 WiFi Tools</b> — <code>modules/wifi/</code> (1 module)</summary>

| Module | Description |
|---|---|
| **ESP8266 Deauther Controller** | Connects to a self-owned ESP8266 "Deauther" board, verifies connectivity, and opens its attack interface. The web dashboard adds remote scan/target-select/SSID-management/attack controls. |

> ⚠️ This is the one module that performs **active wireless attacks** (deauthentication / beacon flooding) rather than passive analysis. See [Security & Ethical Use](#-security--ethical-use).

</details>

<details>
<summary><b>🧪 SOC Tools</b> — <code>modules/soc_tools/</code> (planned)</summary>

| Module | Description |
|---|---|
| **Log Monitor** | Placeholder — prints sample log entries. Labelled "Coming Soon" in the menu. |

</details>

---

## 🔐 Security & Ethical Use

Mindless is built as an **academic / educational toolkit**. Most modules are passive (DNS lookups, header checks, certificate inspection, hash identification, etc.) and safe for demonstrations. A few are not:

- **WiFi Attack Suite** — deauthentication and beacon-flood attacks disrupt wireless service for every device on a targeted network. Only use this against hardware and networks **you own or are explicitly authorised to test**; in most jurisdictions, using it otherwise is illegal.
- **Directory Fuzzer / Port Scanner** — generate a meaningful volume of requests. Only run these against infrastructure you have permission to test.
- **Pastebin Monitor / Brand Impersonation Detector** — query third-party services; respect their rate limits and terms of use.

**Before running any active module:**

1. Confirm you have explicit, documented authorisation to test the target.
2. Treat heuristic verdicts (phishing scores, WAF fingerprints, impersonation matches) as investigative signals, not ground truth — always review manually.
3. Don't expose the web dashboard beyond localhost until authentication is added and secrets are no longer hard-coded (see below).

> ⚠️ **Hard-coded credentials:** `backend/config.py` currently stores the Flask `SECRET_KEY` and Censys API credentials as plain strings in source. Replace these with environment variables before any shared or public deployment.

---

## 📋 Requirements

<details>
<summary><b>Requirements.txt</b> (CLI baseline)</summary>

```
Flask==2.3.3
requests==2.31.0
dnspython==2.4.2
python-whois==0.8.0
beautifulsoup4==4.12.2
qrcode==7.4.2
colorama==0.4.6
pyOpenSSL==23.2.0
certifi==2023.11.17
pyperclip==1.8.2
```

</details>

<details>
<summary><b>requirements-web.txt</b> (Web dashboard, additive)</summary>

```
Flask==2.3.3
Werkzeug==2.3.7
gevent==23.9.1
itsdangerous==2.1.2
MarkupSafe==2.1.3
colorama==0.4.6
requests==2.31.0
urllib3==2.0.7
dnspython==2.4.2
python-whois==0.8.0
cryptography==41.0.7
beautifulsoup4==4.12.2
Pillow==12.1.1
qrcode==7.4.2
pyperclip==1.8.2
pyOpenSSL==23.2.0
certifi==2023.11.17
```

</details>

---

## 🗺️ Limitations & Roadmap

- `password_strength.py` / `password_strength_checker.py` and a couple of other utility files are duplicates pending consolidation.
- `modules/utilities/generate_user_agent.py` is an empty stub superseded by `user_agent_generator.py`.
- The **SOC Tools** domain is an intentional placeholder (`log_monitor.py` prints sample data only).
- The built-in **Censys client** (`backend/integrations/censys_client.py`) isn't yet wired into a menu option or route.
- `signup.html` exists but isn't routed — likely groundwork for a future auth layer.

Contributions addressing any of the above are very welcome.

---

## 🤝 Contributing

Issues and pull requests are welcome. If you're adding a new module, follow the existing pattern in `modules/<domain>/`: a themed banner, a class with the analysis logic, a `generate_report()` method, an `export_report()`/`export_json()` method, and a single public function the CLI/web layer can call.

---

## 📄 License

This project is intended for **academic and educational use**. Add a license file appropriate to your intended distribution (MIT, Apache-2.0, etc.) before publishing publicly. Users are responsible for complying with all applicable laws when using any active-scanning or wireless-attack functionality.

---

<div align="center">

**ICAT Project** · [Linxploit](https://linxploit.com)

</div>
