import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def analyze_file_upload_risk(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║     FILE UPLOAD RISK ANALYZER         ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : HTML form inspection")
    print(Fore.WHITE + "[*] Scope  : Passive analysis only")
    print(Fore.YELLOW + "[!] No file upload attempted\n")

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        forms = soup.find_all("form")
        upload_forms = 0

        for form in forms:
            if form.find("input", {"type": "file"}):
                upload_forms += 1
                print(
                    Fore.GREEN +
                    "[ DETECTED ] File upload form identified"
                )

        if upload_forms == 0:
            print(
                Fore.RED +
                "[ NOT FOUND ] No file upload forms detected"
            )

        print(
            Fore.CYAN +
            "\n[*] File upload analysis completed"
        )
        print(
            Fore.YELLOW +
            "[!] Presence alone does NOT imply vulnerability"
        )

    except Exception as e:
        print(Fore.RED + "\n[!] File upload analysis failed")
        print(Fore.RED + f"Reason : {e}")
