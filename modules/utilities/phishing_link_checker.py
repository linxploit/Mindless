from colorama import Fore, Style


def check_phishing(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        PHISHING LINK CHECKER          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Heuristic keyword scan")
    print(Fore.WHITE + "[*] Scope  : URL pattern inspection\n")

    suspicious_keywords = [
        "login",
        "secure",
        "account",
        "update",
        "verify"
    ]

    flagged = [k for k in suspicious_keywords if k in url.lower()]

    if flagged:
        print(
            Fore.RED +
            f"[ ALERT ] Suspicious keywords detected : {flagged}"
        )
    else:
        print(
            Fore.GREEN +
            "[ CLEAN ] No obvious suspicious patterns detected"
        )

    print(Fore.CYAN + "\n[*] Phishing check completed")
