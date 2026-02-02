import requests
from colorama import Fore, Style

def check_cors_misconfig(url):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║   CORS MISCONFIGURATION CHECKER       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : OPTIONS request analysis")
    print(Fore.WHITE + "[*] Origin : Simulated untrusted domain\n")

    try:
        r = requests.options(
            url,
            headers={"Origin": "https://evil.example"},
            timeout=10
        )

        origin = r.headers.get("Access-Control-Allow-Origin")
        credentials = r.headers.get("Access-Control-Allow-Credentials")

        print(
            Fore.BLUE +
            "[ CORS RESPONSE HEADERS ]"
        )
        print(f"Allow-Origin      : {origin}")
        print(f"Allow-Credentials : {credentials}")

        if origin == "*" and credentials == "true":
            print(
                Fore.RED +
                "\n[ HIGH RISK ] Insecure CORS configuration detected"
            )
        elif origin:
            print(
                Fore.YELLOW +
                "\n[ REVIEW ] CORS enabled – manual validation required"
            )
        else:
            print(
                Fore.GREEN +
                "\n[ SAFE ] No CORS headers present"
            )

        print(Fore.CYAN + "\n[*] CORS analysis completed")

    except Exception as e:
        print(Fore.RED + "\n[!] CORS analysis failed")
        print(Fore.RED + f"Reason : {e}")
