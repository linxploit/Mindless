from datetime import datetime
from colorama import Fore, Style


INDICATORS = [
    "malware",
    "virus",
    "trojan",
    "ransomware"
]


def malicious_indicator_scan(text):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║     MALICIOUS INDICATOR SCANNER       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Keyword-based inspection")
    print(Fore.WHITE + "[*] Scope  : Textual threat indicators\n")

    found = [i for i in INDICATORS if i in text.lower()]

    if found:
        print(Fore.RED + "[ ALERT ] Malicious indicators detected:")
        for indicator in found:
            print(Fore.YELLOW + f"  - {indicator}")
    else:
        print(Fore.GREEN + "[ CLEAN ] No malicious indicators found")

    print(Fore.WHITE + f"[*] Timestamp : {datetime.now()}")
    print(Fore.CYAN + "\n[*] Indicator scanning completed")
