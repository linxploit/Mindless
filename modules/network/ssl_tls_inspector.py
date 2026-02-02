import ssl
import socket
from datetime import datetime
from colorama import Fore, Style

def inspect_ssl_tls(host):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           SSL / TLS INSPECTOR         ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")
    print(Fore.WHITE + "[*] Method : SSL handshake on port 443")
    print(Fore.WHITE + "[*] Target : " + Fore.LIGHTGREEN_EX + host + "\n")

    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        not_after = cert.get("notAfter")
        expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        is_valid = expiry > datetime.utcnow()

        print(Fore.BLUE + "[ Certificate Details ]")
        print(Fore.YELLOW + "Issuer     : " + Fore.WHITE + str(cert.get("issuer")))
        print(Fore.YELLOW + "Subject    : " + Fore.WHITE + str(cert.get("subject")))
        print(Fore.YELLOW + "Expires On : " + Fore.WHITE + str(expiry))

        print(
            Fore.YELLOW + "Valid Now  : " +
            (Fore.GREEN + "YES" if is_valid else Fore.RED + "NO")
        )

        print(Fore.CYAN + "\n[*] SSL/TLS inspection completed")

    except Exception as e:
        print(
            Fore.RED +
            "\n[!] SSL inspection failed"
        )
        print(Fore.RED + f"Reason : {e}")
