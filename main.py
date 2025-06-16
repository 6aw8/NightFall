version = "0.1.0"
import time
from datetime import timedelta
import threading
from pystyle import Colorate, Colors
import os
import subprocess
import sys
# Import specific functions from nuker.py
from core.nuker import (
    nuker_art, delete_channels, delete_roles, kick_all, ban_all,
    create_channels, create_roles, create_webhooks, delete_webhooks,
    spam_webhooks, set_server_name, set_server_icon, destroy_server, 
)
from core import nuker
from colorama import Fore, Style, init
import re
import ctypes
import json
from datetime import datetime
import asyncio # <-- THIS IS CRUCIAL
import discord # <-- THIS IS CRUCIAL
from discord.ext import commands
import webbrowser
from core.settings import *
from core.raider import *
from core.webhooks import *
from core.misc import *
from core.tools import *
from core.help import *
import json
import tls_client
import base64
import threading
import time
from urllib.parse import urlparse, parse_qs


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
nuker.set_http_client_for_bot(bot, proxy_url=None)


def opencmdhelpfile():
    cmdhelpfile = os.path.join("updates", "cmdhelp.txt")
    os.startfile(cmdhelpfile)



serverurl = "https://discord.gg/qHgcF8bdbQ"

# Open URL in the default browser
def opendiscordserver():
  webbrowser.open(serverurl)



BOT_CLIENT_ID = ""
BOT_CLIENT_SECRET = ""
BOT_REDIRECT_URI = "https://localhost:80/"
BOT_TOKEN = ""
SERVER_ID = ""



#ARTS 
settings_art = r'''
                        [01] > Back             [02] > Count Tokens     [03] > View Tokens
'''
raider_art = r'''
                        [01] > Back             [02] > Raider           [03] > Pastebin Raider
                        [04] > List Raider      [05] > Typing           [06] > Message
                        [07] > Server Joiner (risky)
'''
webhooks_art = r'''
                        [01] > Back             [02] > Webhook Spam     [03] > Pastebin Spam
'''
tools_art = r'''
               [01] > Back      [02] > Token Checker    [03] > Nitro Generator    [04] Token Generator 
'''
help_art = r'''
                        [01] > Back             [02] > Command usage         [03] > Our Discord
'''

changeuser_art = r'''

                                   _   ___       __    __  ______      ____
                                  / | / (_)___ _/ /_  / /_/ ____/___ _/ / /
                                 /  |/ / / __ `/ __ \/ __/ /_  / __ `/ / /
                                / /|  / / /_/ / / / / /_/ __/ / /_/ / / /
                               /_/ |_/_/\__, /_/ /_/\__/_/    \__,_/_/_/
                                       /____/

                                  ____________________________________


                               [01] > Back             [02] > Change Username


'''


#USERNAME MANAGEMENT
CONFIG_FILE = os.path.join("assets", "username", "name.json") # For username reference

def get_username():
    # Ensure directory exists before reading/writing
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            return data.get("username")
    else:
        username = input("What would you like to set your username as?: ")
        with open(CONFIG_FILE, "w") as file:
            json.dump({"username": username}, file)
        return username

username = get_username()

def greet(username):
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 17:
        greeting = "Good afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    print(f"{greeting}, {username}.")

def changeuser():
    os.system('title CHANGEUSER')
    os.system('cls')
    print(changeuser_art)
    inps = input("[OPTION] > ")
    while True:
      if inps == "1":
         break
      elif inps == "2":
          newusername = input("[?] What would you like  your new username to be?: ")
          # Ensure directory exists before writing
          os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
          with open(CONFIG_FILE, "w") as file:
            json.dump({"username": newusername}, file)
            print(f"Successfully changed username from '{username}' to '{newusername}' ")
            time.sleep(3)
            break
      else:
          print("[!] Please enter a valid input. ")
          time.sleep(3)
          break

#UPDATE CHECKS
def checkupdate():
    batch_file = os.path.join("updates", "updatecheck.bat")
    # Ensure the 'updates' directory exists for the batch file
    os.makedirs(os.path.dirname(batch_file), exist_ok=True)
    # On Windows, 'start cmd /c' opens a new command prompt and runs the command
    # On Linux/macOS, this specific command will likely not work directly.
    if sys.platform.startswith('win'):
        subprocess.Popen(['start', 'cmd', '/c', batch_file], shell=True)
    else:
        print(Fore.YELLOW + "[!] Update check using .bat file is only supported on Windows." + Style.RESET_ALL)
        print(Fore.YELLOW + "    Please manually check for updates." + Style.RESET_ALL)


# Time Functions for Elapsed Time using ctypes module.
def safe_title(text):
    return re.sub(r'[^a-zA-Z0-9 :|_\-]', '', text)

def set_terminal_title(title):
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except Exception as e:
            # This can happen if not running in a true console (e.g., some IDEs)
            pass
    elif sys.platform == 'darwin' or sys.platform.startswith('linux'):
        sys.stdout.write(f"\x1b]0;{title}\x07")
        sys.stdout.flush()
    # No else: for unsupported platforms, just don't set title

def run_elapsed_time_title():
    start_time = time.time()
    try:
        while True:
            elapsed_seconds = time.time() - start_time
            time_delta = timedelta(seconds=int(elapsed_seconds))
            formatted_time = str(time_delta)
            title_text = f"NightFall | Developers Edition | Elapsed Time: {formatted_time}"
            cleaned_title = safe_title(title_text)

            set_terminal_title(cleaned_title)
            time.sleep(1)
    except Exception as e:
        print(f"\nAn error occurred in update thread: {e}")


init(autoreset=True)

# Class to hold the bot instance for main.py (this is a temporary client)
class NightFallBot(discord.ext.commands.Bot): # Corrected: discord.ext.commands.Bot changed to discord.commands.Bot
    def __init__(self, bot_token_file):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self._ready_event = asyncio.Event()
        self.bot_token_file = bot_token_file

    async def on_ready(self):
        print(Fore.GREEN + f"[>] NightFall CLI client ready. Logged in as {self.user}" + Style.RESET_ALL)
        self._ready_event.set()

    async def wait_until_ready_and_connected(self):
        # Wait for the bot to connect and be ready
        await self._ready_event.wait()
        # Add a small delay after on_ready fires to ensure guild cache is populated
        await asyncio.sleep(2)

    async def start_cli_bot(self):
        # Get the token for the CLI bot
        cli_bot_token = None
        try:
            with open(self.bot_token_file, 'r') as f:
                cli_bot_token = "" #Enter bot token here
        except FileNotFoundError:
            print(Fore.RED + "[-] Bot token file not found for CLI client. Please ensure 'assets/config/bottoken.txt' exists." + Style.RESET_ALL)
            return
        except Exception as e:
            print(Fore.RED + f"[-] Error reading bot token for CLI client: {e}" + Style.RESET_ALL)
            return

        if cli_bot_token:
            try:
                await self.start(cli_bot_token) # Use self.start() here to run in existing loop
            except discord.LoginFailure:
                print(Fore.RED + "[-] Invalid bot token for CLI client. Please check 'assets/config/bottoken.txt'." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[-] An unexpected error occurred while starting the CLI bot: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "[-] No bot token found for CLI client, cannot start bot operations." + Style.RESET_ALL)

# Global bot instance for the CLI, to be used for getting guild objects etc.
# Pass the full path to the token file during instantiation
CLI_BOT_TOKEN_FILE = os.path.join(os.path.dirname(__file__), "assets", "config", "bottoken.txt")
cli_bot = NightFallBot(CLI_BOT_TOKEN_FILE)


class nightfall:
    def __init__(self):
        self.start_time = time.time()
        self.banner_art = r'''

                                   _   ___       __    __  ______      ____
                                  / | / (_)___ _/ /_  / /_/ ____/___ _/ / /
                                 /  |/ / / __ `/ __ \/ __/ /_  / __ `/ / /
                                / /|  / / /_/ / / / / /_/ __/ / /_/ / / /
                               /_/ |_/_/\__, /_/ /_/\__/_/    \__,_/_/_/
                                       /____/

                                  ____________________________________

'''
        self.home_art = r'''
                        [01] > Settings         [02] > Raider           [03] > Webhooks
                        [04] > Tools            [05] > Nuker            [06] > Help
                        [07] > Exit             [08] > Change Username  [09] > Updates

'''
        self.bot = cli_bot # Reference to the global cli_bot instance

    async def setup(self): # Make setup async
        os.system('cls')
        await self.homemenu() # Await homemenu

    def banner(self):
        print(Colorate.Vertical(Colors.white_to_black, self.banner_art))


    async def homemenu(self): # Make homemenu async
        while True:
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, self.home_art))
            username = get_username()
            greet(username)
            print(" ")
            inp = input(F"[MENU] > ")

            if inp == "1":
                await self.settingsmenu() # Await settingsmenu
            elif inp == "2":
                await self.raidermenu() # Await raidermenu
            elif inp == "3":
                await self.webhooksmenu() # Await webhooksmenu
            elif inp == "4":
                await self.toolsmenu() # Await toolsmenu
            elif inp == "5":
                await self.nukermenu() # Await nukermenu
            elif inp == "6":
                await self.helpmenu() # Await helpmenu
            elif inp == "7":
                await exitnf() # Await exitnf
            elif inp == "8":
                changeuser() # This is synchronous, no await needed
            elif inp == "9":
                checkupdate() # This is synchronous, no await needed

            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)


    async def settingsmenu(self): # Make settingsmenu async
        while True:
            os.system('title SETTINGS')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, settings_art))
            inp = input(F"[SETTINGS] > ")

            if inp == "1":
                print(f"[-] {Fore.RED}Returning to Home Menu..." + Style.RESET_ALL)
                break
            elif inp == "2":
                counttokens()
            elif inp == "3":
                viewtokens()
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)


    async def raidermenu(self): # Make raidermenu async
        while True:
            os.system('title RAIDER')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, raider_art))
            inp = input(F"[RAIDER] > ")

            if inp == "1":
                break
            elif inp == "2":
                os.system("cls")
                self.banner()
                raider()
            elif inp == "3":
                os.system("cls")
                self.banner()
                pastebinraider()
            elif inp == "4":
                os.system("cls")
                self.banner()
                listraider()
                input(Fore.MAGENTA + "[?] Press any key to continue!" + Fore.RESET)
            elif inp == "5":
                os.system("cls")
                self.banner()
                typing()
            elif inp == "6":
                os.system("cls")
                self.banner()
                message()
            elif inp == "7":
                serverjoin()
                time.sleep(3)
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)


    async def webhooksmenu(self): # Make webhooksmenu async
        while True:
            os.system('title WEBHOOKS')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, webhooks_art))
            inp = input(F"[WEBHOOKS] > ")

            if inp == "1":
                break
            if inp == "2":
                os.system("cls")
                self.banner()
                webhookspam()
            if inp == "3":
                os.system("cls")
                self.banner()
                pastebinwebspam()
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)


    async def toolsmenu(self): # Make toolsmenu async
        while True:
            os.system('title TOOLS')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, tools_art))
            inp = input(F"[TOOLS] > ")

            if inp == "1":
                break
            if inp == "2":
                os.system("cls")
                self.banner()
                checker()
            if inp == "3":
                os.system("cls")
                self.banner()
                nitrogen()
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)


    async def nukermenu(self): # Make nukermenu async
        os.system('cls')
        self.banner()
        print(Colorate.Vertical(Colors.white_to_black, nuker_art))
        # Ensure the CLI bot is ready before trying to get guild info
        print(Fore.YELLOW + "[!] Ensuring CLI bot is ready to fetch guild information..." + Style.RESET_ALL)
        await self.bot.wait_until_ready_and_connected() # Await here
        print(Fore.GREEN + "[+] CLI bot functional." + Style.RESET_ALL)

        guild_id_str = input(Fore.CYAN + "[?] Enter the Guild ID to nuke: " + Style.RESET_ALL)
        try:
            guild_id = int(guild_id_str)
        except ValueError:
            print(Fore.RED + "[-] Invalid Guild ID. Please enter a number." + Style.RESET_ALL)
            time.sleep(2)
            return

        guild = self.bot.get_guild(guild_id)

        if not guild:
            print(Fore.RED + "[-] Bot is not in the specified guild or invalid Guild ID." + Style.RESET_ALL)
            print(Fore.YELLOW + "    Please ensure the bot is invited to the guild you want to target." + Style.RESET_ALL)
            time.sleep(3)
            return

        while True:
            os.system('title NUKER')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, nuker_art))
            print(Fore.YELLOW + f"[>] Current Guild: {guild.name} (ID: {guild.id})" + Style.RESET_ALL)
            inp = input(F"[NUKER] > ")

            if inp == "1":
                break # Exit the nuker menu loop and return to homemenu
            elif inp == "2":
                await delete_channels(guild) # Await the async function
            elif inp == "3":
                await delete_roles(guild) # Await the async function
            elif inp == "4":
                await kick_all(guild) # Await the async function
            elif inp == "5":
                await ban_all(guild) # Await the async function
            elif inp == "6":
                await create_channels(guild) # Await the async function
            elif inp == "7": # Corrected from original: added create_roles
                await create_roles(guild) # Await the async function
            elif inp == "8":
                await create_webhooks(guild) # Await the async function
            elif inp == "9":
                await delete_webhooks(guild) # Await the async function
            elif inp == "10":
                await spam_webhooks(guild) # Await the async function
            elif inp == "11":
                await set_server_name(guild) # Await the async function
            elif inp == "12":
                await set_server_icon(guild) # Await the async function
            elif inp == "13":
                await destroy_server(guild)
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)
                continue # Use continue to stay in the loop, not self.nukermenu()

            # Only pause and clear if an action was attempted
            input(Fore.MAGENTA + "[?] Press any key to continue to nuker menu..." + Fore.RESET)
            os.system('cls')


    async def helpmenu(self): # Make helpmenu async
        while True:
            os.system('title HELP')
            os.system('cls')
            self.banner()
            print(Colorate.Vertical(Colors.white_to_black, help_art))
            inp = input(F"[HELP] > ")

            if inp == "1":
                break
            elif inp == "2":
                opencmdhelpfile()
            elif inp == "3":
                opendiscordserver()
            else:
                print(Fore.RED + "[-] Invalid Option, Please Try Again!" + Fore.RESET)
                time.sleep(1)
                continue # Use continue to stay in the loop, not self.helpmenu()




async def exitnf(): # Make exitnf async to properly close bot
    print(Fore.CYAN + "[!] Exiting NightFall. Goodbye!" + Style.RESET_ALL)

    if hasattr(sys, 'bot_process') and sys.bot_process is not None:
        if sys.bot_process.poll() is None: # Check if process is still running
            print(Fore.CYAN + "[!] Terminating Discord bot logging process..." + Style.RESET_ALL)
            sys.bot_process.terminate()
            try:
                sys.bot_process.wait(timeout=5) 
            except subprocess.TimeoutExpired:
                sys.bot_process.kill() 

    if cli_bot and cli_bot.is_ready():
        print(Fore.CYAN + "[!] Closing CLI bot connection..." + Style.RESET_ALL)
        await cli_bot.close()
    sys.exit()


# --- Main asynchronous entry point ---
async def main_async_loop():
    
    asyncio.create_task(cli_bot.start_cli_bot())


    nightfalls = nightfall()
    await nightfalls.setup() 


# Usage
if __name__ == "__main__":
    # --- Synchronous setup before starting the async loop ---
    title_thread = threading.Thread(target=run_elapsed_time_title, daemon=True)
    title_thread.start()
    os.system('cls')
    username = get_username()
    greet(username)

    # Path to the discord_logger.py script
    logger_script_dir = os.path.join(os.path.dirname(__file__), "bot_logs")
    logger_script_path = os.path.join(logger_script_dir, "discord_logger.py")

    # Ensure the bot_logs directory exists
    os.makedirs(logger_script_dir, exist_ok=True)
    command = [sys.executable, logger_script_path]

    sys.bot_process = None # Initialize to None

    try:
        if sys.platform.startswith('win'):
            sys.bot_process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
            print(Fore.YELLOW + "[!] Discord bot logger started in a new console window." + Style.RESET_ALL)
        elif sys.platform == 'darwin':
           
            sys.bot_process = subprocess.Popen(['open', '-a', 'Terminal'] + command)
            print(Fore.YELLOW + "[!] Discord bot logger started in a new Terminal window." + Style.RESET_ALL)
        elif sys.platform.startswith('linux'):
            if subprocess.run(['which', 'gnome-terminal'], capture_output=True).returncode == 0:
                sys.bot_process = subprocess.Popen(['gnome-terminal', '--', sys.executable, logger_script_path])
                print(Fore.YELLOW + "[!] Discord bot logger started in a new Gnome Terminal window." + Style.RESET_ALL)
            elif subprocess.run(['which', 'xterm'], capture_output=True).returncode == 0:
                sys.bot_process = subprocess.Popen(['xterm', '-e', sys.executable, logger_script_path])
                print(Fore.YELLOW + "[!] Discord bot logger started in a new Xterm window." + Style.RESET_ALL)
            else:
                sys.bot_process = subprocess.Popen(command)
                print(Fore.RED + "[-] No common terminal found (gnome-terminal, xterm)." + Style.RESET_ALL)
                print(Fore.YELLOW + "[!] Discord bot logger started without a new window (output may mix with main)." + Style.RESET_ALL)
        else:
            sys.bot_process = subprocess.Popen(command)
            print(Fore.RED + "[-] Unsupported OS for explicit new window creation." + Style.RESET_ALL)
            print(Fore.YELLOW + "[!] Discord bot logger started without a new window (output may mix with main)." + Style.RESET_ALL)

        print(Fore.YELLOW + f"[!] Check '{os.path.abspath('discord_bot_log.txt')}' for bot logs." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[-] Failed to start Discord bot logger process in new window: {e}" + Style.RESET_ALL)
        print(Fore.RED + "    Attempting to run without separate window. Discord messages may appear here." + Style.RESET_ALL)
        sys.bot_process = subprocess.Popen(command)

    # --- Start the main async loop ---
    try:
        asyncio.run(main_async_loop())
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n[!] Main application interrupted. Exiting..." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[CRITICAL ERROR] An unexpected error occurred in the main application loop: {e}" + Style.RESET_ALL)
        import traceback
        traceback.print_exc() # Print full traceback for unexpected errors
    finally:
        # Ensure cleanup even on interruption or error
        if hasattr(sys, 'bot_process') and sys.bot_process is not None:
            if sys.bot_process.poll() is None: # If process is still running
                print(Fore.CYAN + "[!] Terminating Discord bot logging process..." + Style.RESET_ALL)
                sys.bot_process.terminate()
                try:
                    sys.bot_process.wait(timeout=5) # Wait for it to terminate
                except subprocess.TimeoutExpired:
                    sys.bot_process.kill() # Force kill if it doesn't terminate
        # Only attempt to close if cli_bot has been initialized and is connected
        if 'cli_bot' in locals() and cli_bot and cli_bot.is_ready():
            try:
                print(Fore.CYAN + "[!] Closing CLI bot connection..." + Style.RESET_ALL)
                # Need to run this in its own loop if the main loop is already closed or errored out
                # or ensure it's part of the shutdown of the primary event loop.
                asyncio.run(cli_bot.close()) # Run in its own loop if the main loop is gone
            except RuntimeError as e:
                print(Fore.YELLOW + f"[-] Error closing CLI bot: {e} (loop might be closed already)" + Style.RESET_ALL)
        sys.exit(0) # Exit the main process