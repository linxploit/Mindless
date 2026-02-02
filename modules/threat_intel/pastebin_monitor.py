import requests
from colorama import Fore, Style


def pastebin_leak_monitor(query):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║      PASTEBIN / LEAK MONITOR          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Public search simulation")
    print(Fore.WHITE + "[*] Scope  : OSINT-safe surface scan\n")

    try:
        response = requests.get(
            f"https://pastebin.com/search?q={query}",
            timeout=10
        )

        if query.lower() in response.text.lower():
            print(
                Fore.RED +
                f"[ LEAK ] Query '{query}' found in public pastes"
            )
        else:
            print(
                Fore.GREEN +
                f"[ CLEAN ] Query '{query}' not found in public pastes"
            )

    except Exception as error:
        print(Fore.YELLOW + f"[ ERROR ] {error}")

    print(Fore.CYAN + "\n[*] Pastebin monitoring completed")
