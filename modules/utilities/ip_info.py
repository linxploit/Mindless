import requests
from colorama import Fore, Style


def ip_info(ip):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           IP INFO FINDER              ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Public IP lookup")
    print(Fore.WHITE + "[*] Source : ipinfo.io\n")

    try:
        r = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=10
        )
        data = r.json()

        for key in [
            "ip",
            "hostname",
            "city",
            "region",
            "country",
            "org"
        ]:
            if key in data:
                print(f"{key:<10}: {data[key]}")

    except Exception as error:
        print(Fore.RED + f"[ ERROR ] {error}")

    print(Fore.CYAN + "\n[*] IP lookup completed")
