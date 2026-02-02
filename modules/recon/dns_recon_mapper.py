import dns.resolver
from colorama import Fore, Style

def dns_recon(domain):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           DNS RECONNAISSANCE          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")
    print(Fore.WHITE + "[*] Source : Direct DNS queries")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + domain)

    record_types = ["A", "AAAA", "MX", "NS", "TXT"]

    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            print(Fore.BLUE + f"\n[{record} Records]")
            for rdata in answers:
                print(Fore.GREEN + "➜ " + Fore.WHITE + str(rdata))

        except dns.resolver.NoAnswer:
            print(Fore.YELLOW + f"\n[{record} Records] No answer")

        except dns.resolver.NXDOMAIN:
            print(Fore.RED + "\n[!] Domain does not exist")
            return

        except Exception as e:
            print(
                Fore.RED +
                f"\n[{record} Records] Error : {e}"
            )

    print(Fore.CYAN + "\n[*] DNS reconnaissance completed")
