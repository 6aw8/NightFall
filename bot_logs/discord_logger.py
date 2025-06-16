# bot_logs/discord_logger.py
import discord
from discord.ext import commands
import sys
import os
import datetime
import asyncio

# --- Configuration (Adjust path if bottoken.txt is not in a common root) ---
# Assuming bottoken.txt is at your_project/assets/config/bottoken.txt
# If discord_logger.py is in bot_logs/, then it needs to go up one level then into assets/config
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up two levels from this script
BOT_TOKEN_FILE = os.path.join(PROJECT_ROOT, "assets", "config", "bottoken.txt")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "discord_bot_log.txt") # Log file in project root


# --- Bot Setup ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- Logging Redirection ---
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        # Ensure the log directory exists
        log_dir = os.path.dirname(filename)
        os.makedirs(log_dir, exist_ok=True)
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# --- Bot Events (same as before) ---
@bot.event
async def on_ready():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{current_time}] [INFO] Bot is ready. Logged in as {bot.user}")
    print(f"[{current_time}] [INFO] User ID: {bot.user.id}")
    print(f"[{current_time}] [INFO] Connected to {len(bot.guilds)} guilds:")
    for guild in bot.guilds:
        print(f"[{current_time}] [INFO]     - {guild.name} (ID: {guild.id})")
    print(f"[{current_time}] [INFO] All bot activity will be logged to '{os.path.abspath(LOG_FILE_PATH)}'")
    print(f"[{current_time}] [INFO] You can close this window at any time, but the bot will stop.")

@bot.event
async def on_message(message):
    pass # Suppress message events

@bot.event
async def on_error(event, *args, **kwargs):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [ERROR] An error occurred in event '{event}':", file=sys.stderr)
    print(f"[{current_time}] [ERROR] Args: {args}", file=sys.stderr)
    print(f"[{current_time}] [ERROR] Kwargs: {kwargs}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)


# --- Main execution for the logger process ---
if __name__ == "__main__":
    sys.stdout = Logger(LOG_FILE_PATH)
    sys.stderr = sys.stdout

    bot_token = None
    try:
        with open(BOT_TOKEN_FILE, 'r') as f:
            bot_token = f.read().strip()
    except FileNotFoundError:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL] Bot token file not found at {BOT_TOKEN_FILE}")
        sys.exit(1)
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL] Error reading bot token: {e}")
        sys.exit(1)

    if bot_token:
        try:
            bot.run(bot_token)
        except discord.LoginFailure:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL] Invalid bot token. Please check {BOT_TOKEN_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL] An unexpected error occurred while starting the bot: {e}")
            sys.exit(1)
    else:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL] No bot token found, cannot start bot.")
        sys.exit(1)