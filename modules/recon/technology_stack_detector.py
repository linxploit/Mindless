import requests
from colorama import Fore, Style

def detect_technology(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║     TECHNOLOGY STACK DETECTION       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")
    print(Fore.WHITE + "[*] Method : Headers + Page Indicators")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + url + "\n")

    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        print(Fore.CYAN + "[ Headers ]")
        header_found = False
        for h in ["Server", "X-Powered-By", "Via"]:
            if h in r.headers:
                print(
                    Fore.GREEN + "[+] " +
                    Fore.WHITE + f"{h:15} : " +
                    Fore.LIGHTGREEN_EX + r.headers[h]
                )
                header_found = True

        if not header_found:
            print(Fore.YELLOW + "[!] No identifying headers found")

        content = r.text.lower()

        print(Fore.CYAN + "\n[ Page Indicators ]")
        indicators = {
            "wordpress": "WordPress",
            "wp-content": "WordPress",
            "laravel": "Laravel",
            "django": "Django",
            "react": "React",
            "vue": "Vue.js"
        }

        detected = False
        for key, tech in indicators.items():
            if key in content:
                print(
                    Fore.GREEN + "[+] Detected : " +
                    Fore.LIGHTGREEN_EX + tech
                )
                detected = True

        if not detected:
            print(Fore.YELLOW + "[!] No obvious technologies detected")

        print(Fore.CYAN + "\n[*] Technology detection completed")

    except Exception as e:
        print(Fore.RED + "[-] Detection failed")
        print(Fore.RED + f"[-] Error : {e}")
