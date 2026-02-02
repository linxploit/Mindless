import requests
from colorama import Fore, Style

COMMON_PATHS = [
    "admin",
    "login",
    "dashboard",
    "uploads",
    "api",
    "test",
    "backup"
]

def directory_fuzzer(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║   DIRECTORY & ENDPOINT FUZZER         ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Wordlist : Common sensitive paths")
    print(Fore.WHITE + "[*] Method   : HTTP status inspection")
    print(Fore.YELLOW + "[!] Not exhaustive\n")

    found = False

    for path in COMMON_PATHS:
        test_url = f"{url.rstrip('/')}/{path}"

        try:
            r = requests.get(test_url, timeout=5)
            if r.status_code in [200, 301, 302, 403]:
                print(
                    Fore.GREEN +
                    f"[ FOUND ] {test_url:<40} ({r.status_code})"
                )
                found = True
        except:
            pass

    if not found:
        print(
            Fore.RED +
            "[ NOT FOUND ] No common endpoints detected"
        )

    print(Fore.CYAN + "\n[*] Directory fuzzing completed")
