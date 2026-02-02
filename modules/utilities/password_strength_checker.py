import re
from colorama import Fore, Style


def password_strength_check(password):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║       PASSWORD STRENGTH ANALYZER      ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝\n")

    length = len(password) >= 8
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    digit = re.search(r"[0-9]", password)
    special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

    score = sum([
        length,
        bool(upper),
        bool(lower),
        bool(digit),
        bool(special)
    ])

    print(f"Length >= 8        : {'Yes' if length else 'No'}")
    print(f"Uppercase Letter  : {'Yes' if upper else 'No'}")
    print(f"Lowercase Letter  : {'Yes' if lower else 'No'}")
    print(f"Digit             : {'Yes' if digit else 'No'}")
    print(f"Special Character : {'Yes' if special else 'No'}\n")

    if score <= 2:
        print(Fore.RED + "[ WEAK ] Password Strength : Weak")
    elif score == 3 or score == 4:
        print(Fore.YELLOW + "[ OKAY ] Password Strength : Medium")
    else:
        print(Fore.GREEN + "[ STRONG ] Password Strength : Strong")

    print(Fore.CYAN + "\n[*] Password analysis completed")
