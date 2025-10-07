from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, os
from colorama import init, Fore
from time import sleep

# Initialize colorama
init(autoreset=True)

# Colors
n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

# Ensure sessions folder exists
os.makedirs("sessions", exist_ok=True)

# Install requests if not available
try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')
    import requests

def banner():
    import random
    b = [
        ' __  __ _____     _____ _____ _  __          _   _ _____  ______ _____ ',
        ' |  \/  |  __ \\   / ____|_   _| |/ /    /\\   | \\ | |  __ \\|  ____|  __ \\ ',
        ' | \\  / | |__) | | (___   | | |  /    /  \\  |  \\| | |  | | |__  | |__) | ',
        ' | |\\/| |  _  /   \\___ \\  | | |  <    / /\\ \\ | . ` | |  | |  __| |  _  / ',
        ' | |  | | | \\ \\   ____) |_| |_| . \\  / ____ \\| |\\  | |__| | |____| | \\ \\ ',
        ' |_|  |_|_|  \\_\\ |_____/|_____|_|\\_\\/_/    \\_\\_| \\_|_____/|______|_|  \\_\\ ',
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print(f'   Version: 1.3 | Author: @SLAYER{n}\n')

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_accounts():
    """Safely load accounts from vars.txt"""
    accounts = []
    if os.path.exists('vars.txt') and os.path.getsize('vars.txt') > 0:
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
    return accounts

def save_accounts(accounts):
    """Save accounts safely to vars.txt"""
    with open('vars.txt', 'wb') as f:
        for acc in accounts:
            pickle.dump(acc, f)

# Main menu loop
while True:
    clr()
    banner()
    print(lg + '[1] Add new accounts' + n)
    print(lg + '[2] Filter all banned accounts' + n)
    print(lg + '[3] Delete specific accounts' + n)
    print(lg + '[4] Update your venomadder' + n)
    print(lg + '[5] Quit' + n)

    choice = input('\nEnter your choice: ')
    if not choice.isdigit():
        print(r + '[!] Invalid input. Please enter a number.' + n)
        sleep(2)
        continue

    a = int(choice)

    # ---------------------- ADD ACCOUNTS ----------------------
    if a == 1:
        new_accs = []
        try:
            number_to_add = int(input(f'\n{lg} [~] Enter number of accounts to add: {r}'))
        except ValueError:
            print(r + '[!] Invalid number.' + n)
            sleep(2)
            continue

        with open('vars.txt', 'ab') as g:
            for i in range(number_to_add):
                phone_number = input(f'\n{lg} [~] Enter Phone Number: {r}').strip()
                parsed_number = ''.join(phone_number.split())
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)

        print(f'\n{lg} [i] Saved all accounts in vars.txt')
        clr()
        print(f'\n{lg} [*] Logging in from new accounts\n')

        for number in new_accs:
            try:
                c = TelegramClient(f'sessions/{number}', 3910389, '86f861352f0ab76a251866059a6adbd6')
                c.start(number)
                print(f'{lg}[+] Login successful: {number}{n}')
                c.disconnect()
            except Exception as e:
                print(r + f'[!] Login failed for {number}: {e}' + n)

        input(f'\nPress enter to go to main menu...')

    # ---------------------- FILTER BANNED ACCOUNTS ----------------------
    elif a == 2:
        accounts = load_accounts()
        banned_accs = []

        if not accounts:
            print(r + '[!] There are no accounts! Please add some and retry.')
            sleep(3)
            continue

        for account in accounts:
            phone = str(account[0])
            client = TelegramClient(f'sessions/{phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f'{lg}[+] {phone} is not banned{n}')
                except PhoneNumberBannedError:
                    print(r + f'{phone} is banned!' + n)
                    banned_accs.append(account)
                except Exception as e:
                    print(r + f'[!] Could not check {phone}: {e}' + n)

        if not banned_accs:
            print(lg + 'Congrats! No banned accounts.' + n)
        else:
            for b in banned_accs:
                accounts.remove(b)
            save_accounts(accounts)
            print(lg + '[i] All banned accounts removed.' + n)

        input('\nPress enter to go to main menu...')

    # ---------------------- DELETE ACCOUNT ----------------------
    elif a == 3:
        accs = load_accounts()
        if not accs:
            print(r + '[!] No accounts found.' + n)
            sleep(2)
            continue

        print(f'{lg}[i] Choose an account to delete\n')
        for i, acc in enumerate(accs):
            print(f'{lg}[{i}] {acc[0]}{n}')

        idx = input(f'\n{lg}[+] Enter a choice: {n}')
        if not idx.isdigit() or int(idx) >= len(accs):
            print(r + '[!] Invalid choice.' + n)
            sleep(2)
            continue

        index = int(idx)
        phone = accs[index][0]
        session_file = f'sessions/{phone}.session'

        if os.path.exists(session_file):
            os.remove(session_file)

        del accs[index]
        save_accounts(accs)

        print(f'\n{lg}[+] Account Deleted: {phone}{n}')
        input(f'\nPress enter to go to main menu...')

    # ---------------------- UPDATE SCRIPT ----------------------
    elif a == 4:
        print(f'\n{lg}[i] Checking for updates...')
        try:
            version = requests.get('https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt')
        except:
            print(f'{r}You are not connected to the internet. Please retry.{n}')
            sleep(2)
            continue

        try:
            remote_version = float(version.text.strip())
        except ValueError:
            print(r + '[!] Could not check version info.' + n)
            sleep(2)
            continue

        if remote_version > 1.3:
            prompt = input(f'{lg}[~] Update available [v{remote_version}]. Download? [y/n]: {r}').lower()
            if prompt in ['y', 'yes']:
                print(f'{lg}[i] Downloading updates...')
                os.system('rm -f add.py manager.py')
                os.system('curl -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/add.py')
                os.system('curl -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/manager.py')
                print(f'{lg}[*] Updated to version: {remote_version}')
                input('Press enter to exit...')
                exit()
            else:
                print(f'{lg}[!] Update aborted.' + n)
        else:
            print(f'{lg}[i] Your venomadder is already up to date.' + n)
        input('Press enter to go to main menu...')

    # ---------------------- QUIT ----------------------
    elif a == 5:
        clr()
        banner()
        exit()

    else:
        print(r + '[!] Invalid option. Try again.' + n)
        sleep(2)
