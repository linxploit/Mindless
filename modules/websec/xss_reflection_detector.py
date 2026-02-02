import requests
from colorama import Fore, Style

def xss_reflection_test(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║      XSS REFLECTION TEST (SAFE)       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Technique : Input reflection analysis")
    print(Fore.WHITE + "[*] Payload   : Non-executable marker")
    print(Fore.YELLOW + "[!] No JavaScript execution performed\n")

    marker = "XSS_TEST_MARKER_123"

    try:
        r = requests.get(
            f"{url}?q={marker}",
            timeout=10
        )

        if marker in r.text:
            print(
                Fore.GREEN +
                "[ REFLECTED ] Input marker found in response body"
            )
            print(
                Fore.YELLOW +
                "[ WARNING   ] Reflection alone does NOT confirm XSS"
            )
        else:
            print(
                Fore.RED +
                "[ NOT FOUND ] No reflection detected"
            )

        print(Fore.CYAN + "\n[*] XSS reflection test completed")

    except Exception as e:
        print(Fore.RED + "\n[!] XSS test failed")
        print(Fore.RED + f"Reason : {e}")
