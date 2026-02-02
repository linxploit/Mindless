import base64
from colorama import Fore, Style


def base64_encode(text):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           BASE64 ENCODER              ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝\n")

    encoded = base64.b64encode(text.encode()).decode()

    print(Fore.WHITE + f"Original Text : {text}")
    print(Fore.GREEN + f"Base64 Output : {encoded}")

    print(Fore.CYAN + "\n[*] Encoding completed")
