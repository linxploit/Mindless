import requests
from colorama import Fore, Style

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Strict-Transport-Security"
]

def analyze_headers(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║   HTTP SECURITY HEADER ANALYZER       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : HTTP response inspection")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + url)
    print(Fore.YELLOW + "[!] Missing headers increase attack surface\n")

    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        for header in SECURITY_HEADERS:
            value = r.headers.get(header)
            if value:
                print(
                    Fore.GREEN +
                    f"[ PRESENT ] {header:<30} → {value}"
                )
            else:
                print(
                    Fore.RED +
                    f"[ MISSING ] {header}"
                )

        print(
            Fore.CYAN +
            "\n[*] Header analysis completed"
        )
        print(
            Fore.YELLOW +
            "[!] Results indicate posture, not exploitation"
        )

    except Exception as e:
        print(Fore.RED + "\n[!] Header analysis failed")
        print(Fore.RED + f"Reason : {e}")
