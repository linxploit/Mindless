#!/usr/bin/env python3
# Red Harbor - OffSec Toolkit
# ICAT Project

import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Import CLI menu
from cli.menu import run_cli_menu

def main():
    run_cli_menu()


if __name__ == "__main__":
    main()
