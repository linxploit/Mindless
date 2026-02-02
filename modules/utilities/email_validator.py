import re
from colorama import Fore, Style


def email_validator(email):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           EMAIL VALIDATOR             ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝\n")

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email):
        print(Fore.GREEN + f"[ VALID ] {email}")
    else:
        print(Fore.RED + f"[ INVALID ] {email}")

    print(Fore.CYAN + "\n[*] Email validation completed")
