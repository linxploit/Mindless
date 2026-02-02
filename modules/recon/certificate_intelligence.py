import requests
from colorama import Fore, Style


def banner(title):
    print(Fore.CYAN + "\n╔" + "═" * 46 + "╗")
    print(Fore.CYAN + f"║  {title.center(42)}  ║")
    print(Fore.CYAN + "╚" + "═" * 46 + "╝" + Style.RESET_ALL)


def section(title):
    print(Fore.MAGENTA + f"\n[ {title} ]" + Style.RESET_ALL)


def crtsh_certificate_intel(domain, limit=30):
    """
    Passive TLS certificate intelligence using crt.sh
    """

    banner("TLS CERTIFICATE INTELLIGENCE")
    section("CERTIFICATE TRANSPARENCY (crt.sh)")

    print(Fore.WHITE + "[*] Source : Public Certificate Transparency Logs")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + domain)
    print(Fore.YELLOW + "[!] Passive enumeration only\n")

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()

        data = r.json()
        discovered = set()

        for entry in data:
            names = entry.get("name_value", "")
            for n in names.split("\n"):
                n = n.strip().lower()
                if n.endswith(domain):
                    discovered.add(n)

        if not discovered:
            print(Fore.YELLOW + "  [!] No certificate-derived domains found")
            return []

        print(Fore.GREEN + f"  [+] Discovered {len(discovered)} unique domains\n")

        for i, d in enumerate(sorted(discovered), 1):
            if i > limit:
                print(Fore.YELLOW + f"\n  [!] Output truncated at {limit} entries")
                break
            print(Fore.CYAN + f"      ├─ {d}")

        print(Fore.CYAN + "\n[*] Certificate intelligence completed\n")
        return list(discovered)

    except Exception as e:
        print(Fore.RED + f"\n  [-] Certificate intelligence failed: {e}")
        return []
