# All functions and assets related to raider will be stored here.

from colorama import Fore, Style, init
import time
import threading
import requests
import random
import os
import json
import tls_client
import base64
import threading
import time
from urllib.parse import urlparse, parse_qs

BOT_CLIENT_ID = "1377562348470145174"
BOT_CLIENT_SECRET = "MtTJrqOaPdvafFmOJf1Jh2TceA9GZgzJ"
BOT_REDIRECT_URI = "https://localhost:80/"
BOT_TOKEN = "MTM3NzU2MjM0ODQ3MDE0NTE3NA.GmUZ51.HNWQJdpDrkbMvJZ1vXAoAVjC9Y4K3dzT_re_ng"
SERVER_ID = "1377557745112449105"



raider_art = r'''
                        [01] > Back             [02] > Spammer          [03] > Pastebin
                        [04] > List             [05] > Typing           [06] > Message
                        [07] > Server Joiner (risky)


'''

def raider():
    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()
        
    os.system(f"title RAIDER w/ tokens: {len(tokens)}")  # Use len(tokens) to display the count
    print(Fore.YELLOW + "[>] You are about to start spamming a channel with a custom message." + Style.RESET_ALL)
    chid = input(Fore.MAGENTA + "[?] Enter a Channel ID (or 'b' to go back): " + Style.RESET_ALL)
    if chid.lower() == 'b':
        return  # Go back to main menu

    if not chid.isdigit():
        print(Fore.RED + "[-] Invalid Channel ID. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    msg = input(Fore.MAGENTA + "[?] Enter a Message to Spam (or 'b' to go back): " + Style.RESET_ALL)
    if msg.lower() == 'b':
        return

    if not msg:
        print(Fore.RED + "[-] Message cannot be empty. Please enter a message." + Style.RESET_ALL)
        time.sleep(1)
        return
    
    threadnum = input(Fore.MAGENTA + "[?] How many threads? (Per Token) (or 'b' to go back): " + Style.RESET_ALL)
    if threadnum.lower() == 'b':
        return  # Go back to main menu

    if not threadnum.isdigit():
        print(Fore.RED + "[-] Invalid Thread Number. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = int(threadnum)

    os.system("cls")

    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()

    print(Fore.YELLOW + "[>] Starting spam process with " + str(len(tokens)) + " tokens." + Style.RESET_ALL)

    def spam(token, chid, message):
        while True:
            url = f'https://discord.com/api/v9/channels/{chid}/messages'
            headers = {'Authorization': token}
            data = {'content': message}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code in [200, 204]:
                print(Fore.GREEN + f'Message Successful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Message Unsuccessful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)

    # List to hold threads
    threads = []

    # Start threads for each token based on threadnum
    for token in tokens:
        for _ in range(threadnum):
            thread = threading.Thread(target=spam, args=(token, chid, msg))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def pastebinraider():
    # Read tokens early to know their count
    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()

    os.system(f"title RAIDER w/ tokens: {len(tokens)}")  # Use len(tokens) to display the count
    print(Fore.YELLOW + "[>] You are about to start spamming a channel with messages from Pastebin." + Style.RESET_ALL)
    chid = input(Fore.MAGENTA + "[?] Enter a Channel ID (or 'b' to go back): " + Style.RESET_ALL)
    if chid.lower() == 'b':
        return  # Go back to main menu

    if not chid.isdigit():
        print(Fore.RED + "[-] Invalid Channel ID. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = input(Fore.MAGENTA + "[?] How many threads? (Per Token) (or 'b' to go back): " + Style.RESET_ALL)
    if threadnum.lower() == 'b':
        return  # Go back to main menu

    if not threadnum.isdigit():
        print(Fore.RED + "[-] Invalid Thread Number. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = int(threadnum)

    os.system("cls")

    # Messages are read after validating the inputs
    with open('assets/messages/tokens/pastebin.txt') as f:
        messages = f.read().splitlines()

    print(Fore.YELLOW + "[>] Starting spam process with " + str(len(tokens)) + " tokens and " + str(len(messages)) + " messages." + Style.RESET_ALL)

    def spam(token, chid):
        while True:
            message = random.choice(messages)
            url = f'https://discord.com/api/v9/channels/{chid}/messages'
            headers = {'Authorization': token}
            data = {'content': message}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code in [200, 204]:
                print(Fore.GREEN + f'Message Successful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Message Unsuccessful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)

    # List to hold threads
    threads = []

    # Start threads for each token based on threadnum
    for token in tokens:
        for _ in range(threadnum):
            thread = threading.Thread(target=spam, args=(token, chid))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def typing():
        # Read tokens early to know their count
    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()

    os.system(f"title RAIDER w/ tokens: {len(tokens)}")  # Use len(tokens) to display the count
    print(Fore.YELLOW + "[>] You are about to start typing in a channel." + Style.RESET_ALL)
    chid = input(Fore.MAGENTA + "[?] Enter a Channel ID (or 'b' to go back): " + Style.RESET_ALL)
    if chid.lower() == 'b':
        return

    threadnum = input(Fore.MAGENTA + "[?] How many threads? (Per Token) (or 'b' to go back): " + Style.RESET_ALL)
    if threadnum.lower() == 'b':
        return  # Go back to main menu

    if not threadnum.isdigit():
        print(Fore.RED + "[-] Invalid Thread Number. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = int(threadnum)
    
    os.system("cls")

    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()

    print(Fore.YELLOW + "[>] Starting typing process with " + str(len(tokens)) + " tokens." + Style.RESET_ALL)

    def spam(token, chid):
        while True:
            url = f'https://discord.com/api/v9/channels/{chid}/typing'
            headers = {'Authorization': token}

            response = requests.post(url, headers=headers)

            if response.status_code in [200, 204]:
                print(Fore.GREEN + f'[+] Request Successful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'[-] Request Unsuccessful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            
            time.sleep(3)
    
    threads = []

    # Start a thread for each token
    for token in tokens:
        thread = threading.Thread(target=spam, args=(token, chid))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def message():
        print(Fore.YELLOW + "[>] You are about to send a single message using all tokens in a channel." + Style.RESET_ALL)
        chid = input(Fore.MAGENTA + "[?] Enter a Channel ID (or 'b' to go back): " + Style.RESET_ALL)
        if chid.lower() == 'b':
            return

        if not chid.isdigit():
            print(Fore.RED + "[-] Invalid Channel ID. Please enter a numeric value." + Style.RESET_ALL)
            time.sleep(1)
            message()
        
        msg = input(Fore.MAGENTA + "[?] Enter a Message to Send (or 'b' to go back): " + Style.RESET_ALL)
        if msg.lower() == 'b':
            return
        
        if not msg:
            print(Fore.RED + "[-] Message cannot be empty. Please enter a message." + Style.RESET_ALL)
            time.sleep(1)
            message()
        
        os.system("cls")

        with open('assets/config/tokens.txt') as f:
            tokens = f.read().splitlines()

        print(Fore.YELLOW + "[>] Starting send process with " + str(len(tokens)) + " tokens." + Style.RESET_ALL)

        def send(token, chid, message):
            url = f'https://discord.com/api/v9/channels/{chid}/messages'
            headers = {'Authorization': token}
            data = {'content': message}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code in [200, 204]:
                print(Fore.GREEN + f'Message Successful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Message Unsuccessful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
        
        threads = []

        # Start a thread for each token
        for token in tokens:
            thread = threading.Thread(target=send, args=(token, chid, msg))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

def listraider():
    # Read tokens early to know their count
    with open('assets/config/tokens.txt') as f:
        tokens = f.read().splitlines()

    os.system(f"title RAIDER w/ tokens: {len(tokens)}")  # Use len(tokens) to display the count
    print(Fore.YELLOW + "[>] You are about to start spamming a channel with messages from List." + Style.RESET_ALL)
    chid = input(Fore.MAGENTA + "[?] Enter a Channel ID (or 'b' to go back): " + Style.RESET_ALL)
    if chid.lower() == 'b':
        return  # Go back to main menu

    if not chid.isdigit():
        print(Fore.RED + "[-] Invalid Channel ID. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = input(Fore.MAGENTA + "[?] How many threads? (Per Token) (or 'b' to go back): " + Style.RESET_ALL)
    if threadnum.lower() == 'b':
        return  # Go back to main menu

    if not threadnum.isdigit():
        print(Fore.RED + "[-] Invalid Thread Number. Please enter a numeric value." + Style.RESET_ALL)
        time.sleep(1)
        return

    threadnum = int(threadnum)

    os.system("cls")

    # Messages are read after validating the inputs
    with open('assets/messages/tokens/list.txt') as f:
        messages = f.read().splitlines()

    print(Fore.YELLOW + "[>] Starting spam process with " + str(len(tokens)) + " tokens and " + str(len(messages)) + " messages." + Style.RESET_ALL)

    def spam(token, chid):
        for message in messages:
            url = f'https://discord.com/api/v9/channels/{chid}/messages'
            headers = {'Authorization': token}
            data = {'content': message}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code in [200, 204]:
                print(Fore.GREEN + f'Message Successful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Message Unsuccessful | {token[:12]} | {response.status_code}' + Style.RESET_ALL)

    # List to hold threads
    threads = []

    # Start threads for each token based on threadnum
    for token in tokens:
        for _ in range(threadnum):
            thread = threading.Thread(target=spam, args=(token, chid))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()



def join_server(user_token):
    parts = user_token.split('.')
    if len(parts) != 3:
        print(f"Invalid token format (expected 3 parts): {user_token}")
        return

    try:
        # Attempt to decode the first part of the token to get user ID (optional, but good for debugging)
        try:
            decoded_token_part = base64.b64decode(parts[0] + '==').decode('utf-8')
            # Assuming the first part is a user ID (common for Discord user tokens)
            user_id_from_token = decoded_token_part
        except Exception:
            user_id_from_token = "unknown" # Could not decode the first part

        session = tls_client.Session(client_identifier="chrome_124", random_tls_extension_order=True)

        headers = {
            "Authorization": user_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        query = {
            "client_id": BOT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": BOT_REDIRECT_URI,
            "scope": "identify guilds.join"
        }

        # Simulate OAuth2 authorize step
        response = session.post(
            "https://discord.com/api/v9/oauth2/authorize",
            headers=headers,
            params=query,
            json={"permissions": "0", "authorize": True}
        )

        if response.status_code == 401:
            print(f"[!] Authorization failed (401 Unauthorized) for token: {user_token}. Token is likely invalid or expired.")
            return
        elif response.status_code == 403:
            print(f"[!] Authorization failed (403 Forbidden) for token: {user_token}. Potential IP ban or permission issue.")
            return
        elif response.status_code != 200:
            print(f"[!] Unexpected status code {response.status_code} during authorization for token: {user_token}. Response: {response.text}")
            return

        if "location" not in response.text: # Check if 'location' is in the raw response text
            # If the response is JSON, use .json() to get location
            try:
                redirect_url = response.json().get("location")
            except json.JSONDecodeError:
                print(Fore.RED + f"[!] Authorization response did not contain a valid location for token: {user_token}. Raw response: {response.text}" + Style.RESET_ALL)
                return
            if not redirect_url: # Check if location was actually extracted
                print(Fore.RED + f"[!] Authorization response did not provide a redirect URL for token: {user_token}. Raw response: {response.text}" + Style.RESET_ALL)
                return
        else: # Fallback if 'location' is in text but not directly in json (less common)
            try:
                redirect_url = response.json().get("location")
            except json.JSONDecodeError:
                print(Fore.RED + f"[!] Authorization response JSON parsing failed for token: {user_token}. Raw response: {response.text}" + Style.RESET_ALL)
                return


        code = parse_qs(urlparse(redirect_url).query).get("code", [None])[0]
        if not code:
            print(f"[!] Could not extract code from redirect URL for token: {user_token}. Redirect URL: {redirect_url}")
            return

        # Exchange code for access token
        token_response = session.post(
            "https://discord.com/api/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": BOT_CLIENT_ID,
                "client_secret": BOT_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": BOT_REDIRECT_URI
            }
        )

        if token_response.status_code != 200:
            print(f"[!] Failed to get access token ({token_response.status_code}) for token: {user_token}. Response: {token_response.text}")
            return

        access_token = token_response.json().get("access_token")
        if not access_token:
            print(f"[!] Access token not found in response for token: {user_token}. Response: {token_response.text}")
            return

        # Use bot to add user to guild
        user_info = session.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info.status_code != 200:
            print(f"[!] Failed to fetch user info ({user_info.status_code}) for token: {user_token}. Response: {user_info.text}")
            return

        user_id = user_info.json().get("id")
        if not user_id:
            print(f"[!] User ID not found in user info for token: {user_token}. Response: {user_info.text}")
            return
        
        response = session.put(
            f"https://discord.com/api/guilds/{SERVER_ID}/members/{user_id}",
            headers={
                "Authorization": f"Bot {BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "access_token": access_token
            }
        )

        if response.status_code in (200, 201, 204):
            print(Fore.GREEN + f"[+] Successfully added user {user_id} to server." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[!] Failed to add user {user_id} to server ({response.status_code}): {response.text}" + Style.RESET_ALL)

    except tls_client.exceptions.TLSClientException as e:
        print(f"[!] TLS Client Exception for token {user_token}: {e}")
    except json.JSONDecodeError:
        print(f"[!] JSON Decode Error for token {user_token}. Response content was not valid JSON.")
    except Exception as e:
        print(f"[!] General Exception for token {user_token}: {e}")

def run_all_tokens():
    try:
        with open('assets/config/tokens.txt', "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: tokens.txt not found. Please create a tokens.txt file with one token per line.")
        return

    if not tokens:
        print("No tokens found in tokens.txt. Please add tokens to the file.")
        return

    threads = []
    for token in tokens:
        t = threading.Thread(target=join_server, args=(token,))
        threads.append(t)
        t.start()
        # Small delay to avoid immediate rate limits when starting many threads
        time.sleep(0.1)

    for t in threads:
        t.join()

def serverjoin():
    run_all_tokens()