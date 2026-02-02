from urllib.parse import urlparse
from colorama import Fore, Style


def phishing_check(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        PHISHING URL ANALYZER          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : URL heuristic checks")
    print(Fore.WHITE + "[*] Scope  : Basic structural analysis\n")

    parsed = urlparse(url)
    indicators = []

    if parsed.scheme != "https":
        indicators.append("Non-HTTPS URL")

    if len(parsed.netloc.split(".")) > 3:
        indicators.append("Suspicious subdomain depth")

    if "-" in parsed.netloc:
        indicators.append("Hyphen in domain (possible spoofing)")

    if indicators:
        print(Fore.RED + "[ ALERT ] Potential phishing indicators detected:")
        for indicator in indicators:
            print(Fore.YELLOW + f"  - {indicator}")
    else:
        print(Fore.GREEN + "[ CLEAN ] No obvious phishing indicators found")

    print(Fore.CYAN + "\n[*] Phishing analysis completed")
