from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle
import os
from colorama import init, Fore
from time import sleep

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

def banner():
    import random
    # fancy logo
    b = [
        ' __  __ _____     _____ _____ _  __          _   _ _____  ______ _____ ',
        ' |  \/  |  __ \   / ____|_   _| |/ /    /\   | \ | |  __ \|  ____|  __ \ ',
        ' | \  / | |__) | | (___   | | |  /    /  \  |  \| | |  | | |__  | |__) | ',
        ' | |\/| |  _  /   \___ \  | | |  <    / /\ \ | . ` | |  | |  __| |  _  / ',
        ' | |  | | | \ \   ____) |_| |_| . \  / ____ \| |\  | |__| | |____| | \ \ ',
        ' |_|  |_|_|  \_\ |_____/|_____|_|\_\/_/    \_\_| \_|_____/|______|_|  \_\ ',
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print(f'   Version: 1.3 | Author: @SLAYER{n}\n')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def ensure_sessions_dir():
    """Ensure sessions directory exists"""
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

def load_accounts():
    """Load accounts from vars.txt file"""
    accounts = []
    if not os.path.exists('vars.txt'):
        return accounts
        
    with open('vars.txt', 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

def save_accounts(accounts):
    """Save accounts to vars.txt file"""
    with open('vars.txt', 'wb') as f:
        for account in accounts:
            pickle.dump(account, f)

def add_accounts():
    """Add new accounts"""
    new_accs = []
    number_to_add = int(input(f'\n{lg}[~] Enter number of accounts to add: {r}'))
    
    for i in range(number_to_add):
        phone_number = input(f'\n{lg}[~] Enter Phone Number: {r}')
        parsed_number = ''.join(phone_number.split())
        new_accs.append(parsed_number)
    
    # Save all new accounts
    with open('vars.txt', 'ab') as g:
        for number in new_accs:
            pickle.dump([number], g)
    
    print(f'\n{lg}[i] Saved all accounts in vars.txt')
    clr()
    print(f'\n{lg}[*] Logging in from new accounts\n')
    
    # Login to new accounts
    for number in new_accs:
        try:
            c = TelegramClient(f'sessions/{number}', 3910389, '86f861352f0ab76a251866059a6adbd6')
            c.start(number)
            print(f'{lg}[+] Login successful for {number}')
            c.disconnect()
        except Exception as e:
            print(f'{r}[!] Failed to login for {number}: {e}')
    
    input(f'\nPress enter to goto main menu...')

def filter_banned_accounts():
    """Filter and remove banned accounts"""
    accounts = load_accounts()
    
    if len(accounts) == 0:
        print(r + '[!] There are no accounts! Please add some and retry')
        sleep(3)
        return

    banned_accs = []
    valid_accs = []
    
    for account in accounts:
        phone = str(account[0])
        client = TelegramClient(f'sessions/{phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
        
        try:
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f'{lg}[+] {phone} is not banned{n}')
                    valid_accs.append(account)
                except PhoneNumberBannedError:
                    print(r + str(phone) + ' is banned!' + n)
                    banned_accs.append(account)
            else:
                print(f'{lg}[+] {phone} is authorized and not banned{n}')
                valid_accs.append(account)
        except Exception as e:
            print(f'{r}[!] Error checking {phone}: {e}')
            valid_accs.append(account)  # Keep account if we can't determine status
        finally:
            client.disconnect()

    if len(banned_accs) == 0:
        print(lg + 'Congrats! No banned accounts')
    else:
        save_accounts(valid_accs)
        print(lg + f'[i] Removed {len(banned_accs)} banned accounts' + n)
    
    input('\nPress enter to goto main menu...')

def delete_account():
    """Delete specific account"""
    accs = load_accounts()
    
    if len(accs) == 0:
        print(r + '[!] No accounts found!')
        input('\nPress enter to goto main menu...')
        return

    print(f'{lg}[i] Choose an account to delete\n')
    for i, acc in enumerate(accs):
        print(f'{lg}[{i}] {acc[0]}{n}')
    
    try:
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        if index < 0 or index >= len(accs):
            print(r + '[!] Invalid choice!')
            input('\nPress enter to goto main menu...')
            return
            
        phone = str(accs[index][0])
        session_file = f'sessions/{phone}.session'
        
        # Delete session file
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f'{lg}[+] Session file deleted: {session_file}')
        
        # Remove from accounts list
        del accs[index]
        save_accounts(accs)
        
        print(f'\n{lg}[+] Account {phone} deleted successfully{n}')
    except (ValueError, IndexError):
        print(r + '[!] Invalid input!')
    except Exception as e:
        print(r + f'[!] Error deleting account: {e}')
    
    input('\nPress enter to goto main menu...')

def update_venomadder():
    """Update the application"""
    print(f'\n{lg}[i] Checking for updates...')
    try:
        version = requests.get('https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt', timeout=10)
        version.raise_for_status()
        latest_version = float(version.text.strip())
    except Exception as e:
        print(f'{r}[!] Failed to check for updates: {e}')
        print(f'{r}[!] Please check your internet connection and try again')
        input('\nPress enter to goto main menu...')
        return

    current_version = 1.3
    
    if latest_version > current_version:
        prompt = input(f'{lg}[~] Update available [Version {latest_version}]. Download? [y/n]: {r}').lower()
        if prompt in ['y', 'yes']:
            print(f'{lg}[i] Downloading updates...')
            try:
                # Download updated files
                files_to_update = {
                    'add.py': 'https://raw.githubusercontent.com/Cryptonian007/Astra/main/add.py',
                    'manager.py': 'https://raw.githubusercontent.com/Cryptonian007/Astra/main/manager.py'
                }
                
                for filename, url in files_to_update.items():
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f'{lg}[+] Updated {filename}')
                
                print(f'{lg}[*] Successfully updated to version: {latest_version}')
            except Exception as e:
                print(f'{r}[!] Failed to download updates: {e}')
        else:
            print(f'{lg}[!] Update cancelled.')
    else:
        print(f'{lg}[i] Your venomadder is already up to date')
    
    input('\nPress enter to goto main menu...')

def main():
    ensure_sessions_dir()
    
    while True:
        clr()
        banner()
        print(lg + '[1] Add new accounts' + n)
        print(lg + '[2] Filter all banned accounts' + n)
        print(lg + '[3] Delete specific accounts' + n)
        print(lg + '[4] Update your venomadder' + n)
        print(lg + '[5] Quit' + n)
        
        try:
            choice = int(input('\nEnter your choice: '))
            
            if choice == 1:
                add_accounts()
            elif choice == 2:
                filter_banned_accounts()
            elif choice == 3:
                delete_account()
            elif choice == 4:
                update_venomadder()
            elif choice == 5:
                clr()
                banner()
                print(f'{lg}[i] Thank you for using Venomadder!{n}')
                break
            else:
                print(r + '[!] Invalid choice! Please try again.')
                sleep(2)
        except ValueError:
            print(r + '[!] Please enter a valid number!')
            sleep(2)
        except KeyboardInterrupt:
            print(f'\n{lg}[i] Program interrupted by user.{n}')
            break
        except Exception as e:
            print(r + f'[!] An error occurred: {e}')
            sleep(2)

if __name__ == "__main__":
    main()
