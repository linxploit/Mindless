from datetime import datetime
from colorama import Fore, Style


HASH_TYPES = {
    "MD5": 32,
    "SHA1": 40,
    "SHA256": 64
}


def hash_analysis(hash_str):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║           HASH ANALYZER               ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Length-based detection")
    print(Fore.WHITE + "[*] Scope  : Static hash inspection\n")

    detected = "Unknown"

    for hash_type, length in HASH_TYPES.items():
        if len(hash_str) == length:
            detected = hash_type
            break

    print(Fore.WHITE + f"[*] Hash      : {hash_str}")
    print(Fore.GREEN + f"[ RESULT ] Detected Type : {detected}")
    print(Fore.WHITE + f"[*] Timestamp : {datetime.now()}")

    print(Fore.CYAN + "\n[*] Hash analysis completed")
