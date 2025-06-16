# All functions and assets not related to a menu will be stored here.

from colorama import Fore, Style, init
import time

# Initialize colorama
init(autoreset=True)

def exitnf():
    print(f"[+] {Fore.GREEN}Exiting...")
    time.sleep(1)
    exit()