import socket
import subprocess
import platform
from colorama import Fore, Style

def live_host_discovery():
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        LIVE HOST DISCOVERY            ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    target = input(Fore.YELLOW + "Enter subnet (e.g. 192.168.1): ").strip()

    print(Fore.WHITE + "\n[*] Method : ICMP Echo Requests (ping)")
    print(Fore.WHITE + "[*] Scope  : /24 network scan")
    print(Fore.YELLOW + "[!] Firewalls may block ICMP\n")

    for i in range(1, 255):
        ip = f"{target}.{i}"

        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "500", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "Unknown"

            print(
                Fore.GREEN +
                f"[ ALIVE ] {ip:<15} → {hostname}"
            )

    print(Fore.CYAN + "\n[*] Host discovery completed")
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
