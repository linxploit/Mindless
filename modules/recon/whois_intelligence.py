import whois
import socket
from colorama import Fore, Style

from backend.integrations.censys_client import CensysClient
from modules.recon.certificate_intelligence import crtsh_certificate_intel


# ---------------- UI HELPERS ----------------
def banner(title):
    print(Fore.CYAN + "\n╔" + "═" * 46 + "╗")
    print(Fore.CYAN + f"║  {title.center(42)}  ║")
    print(Fore.CYAN + "╚" + "═" * 46 + "╝" + Style.RESET_ALL)


def section(title):
    print(Fore.MAGENTA + f"\n[ {title} ]" + Style.RESET_ALL)


def item(label, value):
    if value:
        print(Fore.GREEN + "  [+] " + Fore.WHITE + f"{label}: {value}")


# ---------------- MAIN RECON FUNCTION ----------------
def whois_lookup(domain, use_censys=True):

    result = {
        "domain": domain,
        "whois": {},
        "certificates": [],
        "censys": {}
    }

    banner("WHOIS & DOMAIN INTELLIGENCE")

    # ================= WHOIS =================
    section("WHOIS REGISTRATION DATA")

    try:
        w = whois.whois(domain)

        whois_data = {
            "Registrar": w.get("registrar"),
            "Creation Date": w.get("creation_date"),
            "Expiration Date": w.get("expiration_date"),
            "Organization": w.get("org") or w.get("organization"),
            "Country": w.get("country"),
            "Name Servers": ", ".join(w.get("name_servers", [])) if w.get("name_servers") else None
        }

        result["whois"] = whois_data

        for k, v in whois_data.items():
            item(k, v)

    except Exception as e:
        print(Fore.RED + f"  [-] WHOIS lookup failed: {e}")

    # ================= CERTIFICATE INTEL (crt.sh) =================
    section("TLS CERTIFICATE INTELLIGENCE")

    try:
        cert_domains = crtsh_certificate_intel(domain)
        result["certificates"] = cert_domains

        if cert_domains:
            for d in cert_domains[:15]:
                print(Fore.WHITE + f"      ├─ {d}")
        else:
            print(Fore.YELLOW + "  [!] No certificate-derived domains found")

    except Exception as e:
        print(Fore.RED + f"  [-] Certificate intel failed: {e}")

    # ================= CENSYS ENRICHMENT =================
    if use_censys:
        section("CENSYS PASSIVE INFRASTRUCTURE")

        try:
            ip = socket.gethostbyname(domain)
            censys = CensysClient()
            censys_data = censys.get_host_asset(ip)

            result["censys"] = censys_data

            item("Resolved IP", ip)
            item("ASN", censys_data.get("autonomous_system", {}).get("asn"))
            item("ASN Org", censys_data.get("autonomous_system", {}).get("organization"))
            item("Country", censys_data.get("location", {}).get("country"))

            services = censys_data.get("services", [])
            if services:
                print(Fore.GREEN + "\n  [+] Exposed Services")
                for s in services[:10]:
                    port = s.get("port")
                    service = s.get("service_name")
                    print(Fore.WHITE + f"      ├─ Port {port} → {service}")

        except Exception as e:
            print(Fore.RED + f"  [-] Censys enrichment failed: {e}")

    print(Fore.CYAN + "\n[*] Domain intelligence completed\n" + Style.RESET_ALL)
    return result