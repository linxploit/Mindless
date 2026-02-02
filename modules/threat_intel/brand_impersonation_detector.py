from colorama import Fore, Style


def brand_impersonation(text):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║     BRAND IMPERSONATION DETECTOR      ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Keyword-based inspection")
    print(Fore.WHITE + "[*] Scope  : Brand name abuse detection\n")

    brands = [
        "google",
        "microsoft",
        "paypal",
        "apple",
        "amazon"
    ]

    detected = []

    for brand in brands:
        if brand.lower() in text.lower():
            detected.append(brand)

    if detected:
        print(Fore.RED + "[ ALERT ] Potential brand impersonation detected:")
        for brand in detected:
            print(Fore.YELLOW + f"  - {brand}")
    else:
        print(Fore.GREEN + "[ CLEAN ] No brand impersonation detected")

    print(Fore.CYAN + "\n[*] Brand analysis completed")
