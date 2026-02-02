import qrcode
from colorama import Fore, Style


def url_to_qr(url, filename="qrcode.png", save=True):
    print(Fore.CYAN + "\n╔══════════════════════════════════════╗")
    print(Fore.CYAN + "║        URL TO QR CODE GENERATOR       ║")
    print(Fore.CYAN + "╚══════════════════════════════════════╝")

    print(Fore.WHITE + "[*] Method : QR code generation")
    print(Fore.WHITE + "[*] Scope  : Display & optional save\n")

    try:
        img = qrcode.make(url)

        img.show()

        if save:
            img.save(filename)
            print(Fore.GREEN + f"[ SAVED ] QR code saved as {filename}")

        print(Fore.GREEN + "[ DONE ] QR code displayed successfully")

    except Exception as error:
        print(Fore.RED + f"[ ERROR ] {error}")
