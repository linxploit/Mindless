import requests
from colorama import Fore, Style

def check_ip_reputation(ip):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        IP REPUTATION CHECK            ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Source : Public OSINT (ipinfo.io)")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + ip)
    print(Fore.YELLOW + "[!] Contextual intelligence only\n")

    try:
        r = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=10
        )
        data = r.json()

        print(Fore.BLUE + "[ IP Profile ]")
        for key in ["ip", "hostname", "city", "region", "country", "org"]:
            if key in data:
                print(
                    Fore.YELLOW + f"{key.capitalize():<10}: " +
                    Fore.WHITE + str(data[key])
                )

        print(
            Fore.CYAN +
            "\n[*] Reputation check completed"
        )
        print(
            Fore.YELLOW +
            "[!] This does NOT confirm malicious activity"
        )

    except Exception as e:
        print(Fore.RED + "\n[!] Failed to retrieve IP intelligence")
        print(Fore.RED + f"Reason : {e}")
