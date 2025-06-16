def start_bot():
    bot_token = get_bot_token()
    if bot_token:
        try:
            bot.run(bot_token)
        except discord.LoginFailure:
            print(Fore.RED + "[-] Invalid bot token. Please check 'assets/config/bottoken.txt'." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[-] An unexpected error occurred while starting the bot: {e}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[-] Bot token not found, cannot start bot." + Style.RESET_ALL)

start_bot()