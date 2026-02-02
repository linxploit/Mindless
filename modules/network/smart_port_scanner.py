import socket
import threading
from queue import Queue
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt"
}

TIMEOUT = 0.6
THREADS = 50


def smart_port_scan(target):
    print(Fore.CYAN + "\n╔══════════════════════════════════════════╗")
    print(Fore.CYAN + "║        MINDLESS :: SMART PORT SCAN        ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════╝")

    print(Fore.WHITE + f"[*] Target     : {Fore.LIGHTGREEN_EX}{target}")
    print(Fore.WHITE + "[*] Scan Type  : TCP Connect")
    print(Fore.WHITE + f"[*] Threads    : {THREADS}")
    print(Fore.YELLOW + "[!] Not stealthy | Firewall may affect results\n")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(Fore.RED + "[!] Failed to resolve target")
        return

    port_queue = Queue()
    open_ports = []
    lock = threading.Lock()

    for port in COMMON_PORTS:
        port_queue.put(port)

    def worker():
        while not port_queue.empty():
            port = port_queue.get()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(TIMEOUT)
                result = sock.connect_ex((target_ip, port))

                if result == 0:
                    try:
                        sock.send(b"\r\n")
                        banner = sock.recv(1024).decode(errors="ignore").strip()
                    except Exception:
                        banner = ""

                    service = COMMON_PORTS.get(port, "Unknown")

                    with lock:
                        open_ports.append((port, service, banner))
                        print(
                            Fore.GREEN +
                            f"[ OPEN ] Port {port:<5} | {service:<10} " +
                            (Fore.CYAN + f"| Banner: {banner[:40]}" if banner else "")
                        )

                sock.close()
            except Exception:
                pass
            finally:
                port_queue.task_done()

    start_time = datetime.now()

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    try:
        port_queue.join()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Scan interrupted by user")
        return

    duration = (datetime.now() - start_time).total_seconds()

    print(Fore.CYAN + "\n" + "─" * 50)
    if not open_ports:
        print(Fore.RED + "[ CLOSED ] No common open ports detected")
    else:
        print(Fore.CYAN + f"[*] Open Ports Found : {len(open_ports)}")

    print(Fore.WHITE + f"[*] Scan Duration   : {duration:.2f}s")
    print(Fore.CYAN + "─" * 50)
