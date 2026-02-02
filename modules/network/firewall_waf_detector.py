import requests
from colorama import Fore, Style

def detect_firewall_waf(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║       FIREWALL / WAF DETECTOR         ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Header & response analysis")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + url)
    print(Fore.YELLOW + "[!] Heuristic-based detection\n")

    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        server = r.headers.get("Server", "").lower()

        waf_signatures = {
            "cloudflare": "Cloudflare",
            "akamai": "Akamai",
            "imperva": "Imperva",
            "sucuri": "Sucuri"
        }

        detected = False

        print(Fore.BLUE + "[ Header Analysis ]")
        for key, name in waf_signatures.items():
            if key in server:
                print(
                    Fore.GREEN +
                    f"[ DETECTED ] Possible WAF: {name}"
                )
                detected = True

        if r.status_code in [401, 403, 406]:
            print(
                Fore.GREEN +
                "[ DETECTED ] Access-restriction HTTP response"
            )

        if not detected:
            print(
                Fore.RED +
                "[ NOT FOUND ] No obvious WAF indicators"
            )

        print(Fore.CYAN + "\n[*] WAF detection completed")

    except Exception as e:
        print(Fore.RED + "\n[!] WAF detection failed")
        print(Fore.RED + f"Reason : {e}")
