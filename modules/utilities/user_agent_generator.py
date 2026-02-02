import random
import time
from colorama import Fore, Style

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",

    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) "
    "Gecko/20100101 Firefox/121.0",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) "
    "Gecko/20100101 Firefox/119.0",

    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",

    # Mobile
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
]


def user_agent_generator(
    rotate=False,
    count=1,
    delay=2,
    copy=False,
    export_file=None,
    return_header=False
):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        USER-AGENT GENERATOR           ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : Random selection")
    print(Fore.WHITE + "[*] Scope  : Browser & mobile agents\n")

    generated = []

    for i in range(count):
        ua = random.choice(USER_AGENTS)
        generated.append(ua)

        print(Fore.GREEN + "[ GENERATED ] User-Agent:")
        print(Fore.WHITE + ua + "\n")

        if rotate and i < count - 1:
            time.sleep(delay)

    if copy:
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(generated[-1])
            print(Fore.GREEN + "[ COPIED ] User-Agent copied to clipboard")
        else:
            print(Fore.YELLOW + "[ WARN ] pyperclip not installed")

    if export_file:
        try:
            with open(export_file, "w", encoding="utf-8") as f:
                for ua in generated:
                    f.write(ua + "\n")
            print(Fore.GREEN + f"[ SAVED ] User-Agents saved to {export_file}")
        except Exception as e:
            print(Fore.RED + f"[ ERROR ] Failed to save file: {e}")

    if return_header:
        print(Fore.CYAN + "\n[*] Header-ready output enabled")
        return {"User-Agent": generated[-1]}

    print(Fore.CYAN + "\n[*] User-Agent generation completed")
