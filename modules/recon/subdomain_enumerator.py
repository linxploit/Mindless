import dns.resolver
from colorama import Fore, Style

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "test", "dev",
    "api", "admin", "portal", "vpn"
]

def subdomain_enum(domain):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║       SUBDOMAIN ENUMERATION           ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")
    print(Fore.WHITE + "[*] Method : Common Wordlist + DNS Resolution")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + domain)
    print(Fore.YELLOW + "[!] Note   : Not exhaustive\n")

    found = False

    for sub in COMMON_SUBDOMAINS:
        subdomain = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(subdomain, "A")
            print(
                Fore.GREEN + "[+] Found  : " +
                Fore.LIGHTGREEN_EX + subdomain
            )
            found = True
        except:
            pass

    if not found:
        print(Fore.RED + "[-] No subdomains found using common list")

    print(Fore.CYAN + "\n[*] Subdomain enumeration completed")
