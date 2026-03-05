#!/usr/bin/env python3
"""
MINDLESS-REDOPS :: CLI Banners
Professional ASCII Art Banners & UI Elements
Author: ICAT Project | Linxploit.xyz
"""

from colorama import Fore, Style, init
import platform

init(autoreset=True)

# Detect Windows for character compatibility
IS_WINDOWS = platform.system().lower() == 'windows'

# Professional box-drawing characters
if IS_WINDOWS:
    # Windows-compatible ASCII
    H_LINE = "="
    V_LINE = "|"
    TL_CORNER = "+"
    TR_CORNER = "+"
    BL_CORNER = "+"
    BR_CORNER = "+"
else:
    # Linux/Unix Unicode box drawing
    H_LINE = "═"
    V_LINE = "║"
    TL_CORNER = "╔"
    TR_CORNER = "╗"
    BL_CORNER = "╚"
    BR_CORNER = "╝"

def kali_dragon():
    """Display Kali Dragon ASCII art - Professional Red Team Aesthetic"""
    print(Fore.RED + Style.BRIGHT + r"""
       .oXXXXXXXXXXXXXXXXXXo.
     .oXXXXX/XXXXXXXX\XXXXXXXo.
    /XXXXXX-\XXXXXXXX/-XXXXXXXx\
   dXXXXXX/XX\XXXXXX/XX\XXXXXXXXb
  XXXXXXXXXXXX\XXXX/XXXXXXXXXXXXX
  XXX'~   ~`OO8bXXXd8OO'~  ~`XXXXX
  9XX'        `98v8P'         `XXP'
   9X.        .db|db.         .XP
    )b. .dbo.dP'`v'`9b.odb. .dX(
  ,dXXXXXXXXXXb     dXXXXXXXXXXb.
 dXXXXXXXXXXP'   .   `9XXXXXXXXXXb
dXXXXXXXXXXXb   d|b   dXXXXXXXXXXXb
9XXb'  `XXXXXb.dX|Xb.dXXXXX'  `dXXP
 `'     9XXXXXX(   )XXXXXXP     `'
         XXXX X.`N'.X XXXX
         XP^X'`O   0'`X^XX
         X. R  `   '  9 )X
         `K  `       '  7'
          `             ' 
    """ + Style.RESET_ALL)
    print()

def main_banner():
    print(Fore.GREEN + Style.BRIGHT + r"""
 __  __ ___ _   _ ____  _     _____ ____ ____    _ 
|  \/  |_ _| \ | |  _ \| |   | ____/ ___/ ___|  | |
| |\/| || ||  \| | | | | |   |  _| \___ \___ \  | |
| |  | || || |\  | |_| | |___| |___ ___) |__) | |_|
|_|  |_|___|_| \_|____/|_____|_____|____/____/  (_)

    """+ Style.RESET_ALL)
    
    print(Fore.WHITE + Style.BRIGHT + f"""
    ┌────────────────────────────────────────────────────────────────┐
    │                    BLUE TEAM OPERATIONS FRAMEWORK              │
    │                    Mindless RedOps v3.1 - Red Harbor           │
    │                    ICAT Project | Linxploit.xyz                │
    └────────────────────────────────────────────────────────────────┘
    """ + Style.RESET_ALL)
    print()