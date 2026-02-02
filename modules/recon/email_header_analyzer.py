from colorama import Fore, Style

def analyze_email_headers(raw_headers):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        EMAIL HEADER ANALYSIS          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")
    print(Fore.WHITE + "[*] Scope  : Header-level indicators only\n")

    lines = raw_headers.splitlines()

    received = []
    spf = None
    dkim = None

    for line in lines:
        l = line.lower()
        if l.startswith("received:"):
            received.append(line)
        if "spf=" in l:
            spf = line
        if "dkim=" in l:
            dkim = line

    print(Fore.BLUE + "[ Received Chain ]")
    if received:
        for r in received:
            print(Fore.GREEN + "➜ " + Fore.WHITE + r)
    else:
        print(Fore.RED + "No Received headers found")

    print(Fore.BLUE + "\n[ Authentication Results ]")
    print(
        Fore.YELLOW + "SPF  : " +
        (Fore.GREEN + spf if spf else Fore.RED + "Not found")
    )
    print(
        Fore.YELLOW + "DKIM : " +
        (Fore.GREEN + dkim if dkim else Fore.RED + "Not found")
    )

    print(
        Fore.MAGENTA +
        "\n[!] Note: Header analysis does NOT prove message legitimacy"
    )
