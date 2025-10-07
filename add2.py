# import libraries
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest
import sys
import os
import pickle
import time
import random
from colorama import init, Fore

init()

# Color definitions
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = lg + '[' + w + 'i' + lg + ']' + rs
error = lg + '[' + r + '!' + lg + ']' + rs
success = w + '[' + lg + '*' + w + ']' + rs
INPUT = lg + '[' + cy + '~' + lg + ']' + rs
plus = w + '[' + lg + '+' + w + ']' + rs
minus = w + '[' + lg + '-' + w + ']' + rs

def banner():
    # fancy logo
    b = [
        ' _____     _            __   ___      __ _______    _____',
        '/ ____|   |  |          /\    \ \\   / / |  ____|  |   __ \\',
        '| (___ |  |  |         /  \    \ \\_/ /  | |__     |   |__) |',
        ' \\___ \\ |  |        / /\\ \   \   /    |  __|    |   _  /',
        ' ____) |  |  |____   / ____ \\   | |     | |____   | | \\ \\',
        '|_____/   |_______| /_/    \\_\\ |_|     |______|  |_|  \\_\\',
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{rs}')
    print(f'{lg}   Version: {w}1.2{lg} | Author: {w}Cryptonian{rs}\n')

# function to clear screen
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def repair_vars_file():
    """Repair corrupted vars.txt file"""
    print(f'{info}{lg} Checking vars.txt file integrity...{rs}')
    
    if not os.path.exists('vars.txt'):
        print(f'{error} {r}vars.txt file not found!{rs}')
        return []
    
    # Create backup of corrupted file
    try:
        if os.path.exists('vars.txt.backup'):
            os.remove('vars.txt.backup')
        os.rename('vars.txt', 'vars.txt.backup')
        print(f'{info} {lg}Created backup: vars.txt.backup{rs}')
    except Exception as e:
        print(f'{error} {r}Error creating backup: {e}{rs}')
        return []
    
    accounts = []
    recovered_count = 0
    
    # Try to recover data from backup
    try:
        with open('vars.txt.backup', 'rb') as f:
            content = f.read()
            
        # Try to load with different protocols
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            try:
                f = open('vars.txt.backup', 'rb')
                accounts = []
                while True:
                    try:
                        account = pickle.load(f)
                        if (isinstance(account, list) and len(account) >= 3 and 
                            isinstance(account[0], str) and account[0].startswith('+')):
                            accounts.append(account)
                            recovered_count += 1
                            print(f'{plus} {lg}Recovered account: {account[0]}{rs}')
                    except EOFError:
                        break
                    except Exception:
                        continue
                f.close()
                if accounts:
                    break
            except Exception:
                continue
                
    except Exception as e:
        print(f'{error} {r}Could not recover accounts from backup: {e}{rs}')
    
    # Save recovered accounts
    if accounts:
        try:
            with open('vars.txt', 'wb') as f:
                for account in accounts:
                    pickle.dump(account, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f'{success} {lg}Successfully recovered {len(accounts)} accounts{rs}')
        except Exception as e:
            print(f'{error} {r}Error saving recovered accounts: {e}{rs}')
    else:
        # Create empty file
        with open('vars.txt', 'wb') as f:
            pass
        print(f'{info} {lg}Created new empty vars.txt file{rs}')
    
    return accounts

def load_accounts_safe():
    """Safely load accounts with corruption recovery"""
    accounts = []
    
    if not os.path.exists('vars.txt'):
        print(f'{info} {lg}vars.txt not found. You need to add accounts first.{rs}')
        return accounts
    
    file_size = os.path.getsize('vars.txt')
    if file_size == 0:
        print(f'{info} {lg}vars.txt is empty. No accounts found.{rs}')
        return accounts
    
    try:
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    account = pickle.load(f)
                    if (isinstance(account, list) and len(account) >= 3 and 
                        isinstance(account[0], str)):
                        accounts.append(account)
                except EOFError:
                    break
                except Exception as e:
                    print(f'{error} {r}Corrupted entry found: {e}{rs}')
                    continue
                    
    except Exception as e:
        print(f'{error} {r}File appears corrupted. Attempting repair...{rs}')
        accounts = repair_vars_file()
    
    return accounts

def save_accounts(accounts):
    """Save accounts to file safely"""
    try:
        # Create backup before saving
        if os.path.exists('vars.txt'):
            os.rename('vars.txt', 'vars.txt.backup.tmp')
        
        with open('vars.txt', 'wb') as f:
            for account in accounts:
                if (isinstance(account, list) and len(account) >= 3 and 
                    isinstance(account[0], str)):
                    pickle.dump(account, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Remove temporary backup if save successful
        if os.path.exists('vars.txt.backup.tmp'):
            os.remove('vars.txt.backup.tmp')
            
        print(f'{success} {lg}Successfully saved {len(accounts)} accounts{rs}')
    except Exception as e:
        print(f'{error} {r}Error saving accounts: {e}{rs}')
        # Restore backup if save failed
        if os.path.exists('vars.txt.backup.tmp'):
            if os.path.exists('vars.txt'):
                os.remove('vars.txt')
            os.rename('vars.txt.backup.tmp', 'vars.txt')

def setup_new_account():
    """Setup a new Telegram account"""
    print(f'\n{info}{cy} Setting up new account...{rs}')
    
    try:
        api_id = input(f'{INPUT}{cy} Enter API ID: {rs}').strip()
        api_hash = input(f'{INPUT}{cy} Enter API Hash: {rs}').strip()
        phone = input(f'{INPUT}{cy} Enter phone number (with country code): {rs}').strip()
        
        if not api_id or not api_hash or not phone:
            print(f'{error} {r}All fields are required!{rs}')
            return None
        
        # Create sessions directory if it doesn't exist
        if not os.path.exists('sessions'):
            os.makedirs('sessions')
        
        # Test the account
        client = TelegramClient(f'sessions/{phone}', int(api_id), api_hash)
        client.connect()
        
        if not client.is_user_authorized():
            print(f'{info} {lg}Sending verification code...{rs}')
            client.send_code_request(phone)
            code = input(f'{INPUT}{cy} Enter verification code: {rs}').strip()
            client.sign_in(phone, code)
        
        # Verify login
        me = client.get_me()
        if me:
            print(f'{success} {lg}Success! Logged in as: {me.first_name}{rs}')
            account_data = [phone, api_id, api_hash]
            
            # Save to vars.txt
            current_accounts = load_accounts_safe()
            current_accounts.append(account_data)
            save_accounts(current_accounts)
            
            client.disconnect()
            return account_data
        else:
            print(f'{error} {r}Failed to verify login{rs}')
            client.disconnect()
            return None
            
    except Exception as e:
        print(f'{error} {r}Error setting up account: {e}{rs}')
        return None

def check_banned_accounts():
    """Check and remove banned accounts"""
    print(f'\n{info}{lg} Checking for banned accounts...{rs}')
    accounts = load_accounts_safe()
    
    if not accounts:
        print(f'{info} {lg}No accounts found. Would you like to add one?{rs}')
        add_new = input(f'{INPUT}{cy} Add new account? [y/n]: {rs}').lower().startswith('y')
        if add_new:
            new_acc = setup_new_account()
            if new_acc:
                accounts = [new_acc]
        else:
            return []
    
    banned = []
    valid_accounts = []
    
    for account in accounts:
        if not account or len(account) < 3:
            continue
            
        phone, api_id, api_hash = account[0], account[1], account[2]
        print(f'{plus}{grey} Checking {lg}{phone}')
        
        try:
            client = TelegramClient(f'sessions/{phone}', int(api_id), api_hash)
            client.connect()
            
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f'{plus} {lg}OK - Code sent{rs}')
                    valid_accounts.append(account)
                except PhoneNumberBannedError:
                    print(f'{error} {w}{phone} {r}is banned!{rs}')
                    banned.append(account)
                except Exception as e:
                    print(f'{error} {r}Error with {phone}: {e}{rs}')
                    # Keep account for now, might be temporary issue
                    valid_accounts.append(account)
            else:
                valid_accounts.append(account)
                me = client.get_me()
                if me:
                    print(f'{plus} {lg}Authorized as: {me.first_name}{rs}')
                else:
                    print(f'{plus} {lg}Authorized{rs}')
                    
        except PhoneNumberBannedError:
            print(f'{error} {w}{phone} {r}is banned!{rs}')
            banned.append(account)
        except Exception as e:
            print(f'{error} {r}Error checking {phone}: {e}{rs}')
            valid_accounts.append(account)  # Keep account on connection errors
        finally:
            try:
                client.disconnect()
            except:
                pass
    
    # Save valid accounts back to file
    if banned:
        save_accounts(valid_accounts)
        print(f'{info} {lg}Removed {len(banned)} banned account(s){rs}')
    
    return valid_accounts

def log_status(scraped, index):
    """Log scraping details"""
    try:
        with open('status.dat', 'wb') as f:
            pickle.dump([scraped, int(index)], f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f'{info}{lg} Progress saved to status.dat{lg}')
    except Exception as e:
        print(f'{error} {r}Error saving status: {e}{rs}')

def load_status():
    """Load scraping status"""
    try:
        if os.path.exists('status.dat'):
            with open('status.dat', 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        print(f'{error} {r}Error loading status: {e}{rs}')
        # Remove corrupted status file
        try:
            os.remove('status.dat')
        except:
            pass
    return None

def exit_window():
    input(f'\n{cy} Press enter to exit...{rs}')
    clr()
    banner()
    sys.exit()

def main():
    clr()
    banner()
    
    # Load and check accounts
    accounts = check_banned_accounts()
    if not accounts:
        print(f'{error} {r}No valid accounts found!{rs}')
        add_new = input(f'{INPUT}{cy} Would you like to add a new account? [y/n]: {rs}').lower().startswith('y')
        if add_new:
            setup_new_account()
            print(f'{info} {lg}Please run the script again to use the new account.{rs}')
        exit_window()
    
    print(f'{info}{lg} Total valid accounts: {w}{len(accounts)}{rs}')
    
    # Get scraping details
    status = load_status()
    if status:
        scraped_grp, index = status
        resume = input(f'{INPUT}{cy} Resume scraping members from {w}{scraped_grp}{lg}? [y/n]: {rs}')
        if resume.lower().startswith('y'):
            print(f'{info} {lg}Resuming from index: {w}{index}{rs}')
        else:
            try:
                os.remove('status.dat')
            except:
                pass
            scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {rs}').strip()
            index = 0
    else:
        scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {rs}').strip()
        index = 0
    
    if not scraped_grp:
        print(f'{error} {r}Group link is required!{rs}')
        exit_window()
    
    # Get number of accounts to use
    try:
        number_of_accs = min(int(input(f'{INPUT}{cy} Enter number of accounts to use: {rs}')), len(accounts))
    except ValueError:
        print(f'{error} {r}Invalid number! Using 1 account.{rs}')
        number_of_accs = 1
    
    print(f'{info}{cy} Choose an option{lg}')
    print(f'{cy}[0]{lg} Add to public group')
    print(f'{cy}[1]{lg} Add to private group')
    
    try:
        choice = int(input(f'{INPUT}{cy} Enter choice: {rs}'))
        if choice not in [0, 1]:
            choice = 0
    except ValueError:
        choice = 0
    
    target = input(f'{INPUT}{cy} Enter {"public" if choice == 0 else "private"} group link: {rs}').strip()
    
    if not target:
        print(f'{error} {r}Target group link is required!{rs}')
        exit_window()
    
    print(f'{grey}_'*50)
    
    # Select accounts to use
    to_use = accounts[:number_of_accs]
    remaining_accounts = accounts[number_of_accs:]
    
    # Save all accounts back (reordered)
    save_accounts(remaining_accounts + to_use)
    
    try:
        sleep_time = max(0, int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None{w}]: {rs}')))
    except ValueError:
        sleep_time = 1
    
    print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')
    
    total_members_added = 0
    
    for i, acc in enumerate(to_use):
        if not acc or len(acc) < 3:
            continue
            
        phone, api_id, api_hash = acc[0], acc[1], acc[2]
        stop = index + 60
        
        print(f'{plus}{grey} User {i+1}/{len(to_use)}: {cy}{phone}{lg} -- Starting session... ')
        
        client = TelegramClient(f'sessions/{phone}', int(api_id), api_hash)
        
        try:
            client.start(phone)
            me = client.get_me()
            acc_name = me.first_name if me else phone
            
            # Join source group to scrape members
            try:
                if '/joinchat/' in scraped_grp:
                    g_hash = scraped_grp.split('/joinchat/')[1]
                    client(ImportChatInviteRequest(g_hash))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
                else:
                    client(JoinChannelRequest(scraped_grp))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except UserAlreadyParticipantError:
                pass
            except Exception as e:
                print(f'{error} {r}Failed to join source group: {e}{rs}')
                continue
            
            # Get source group entity
            try:
                scraped_grp_entity = client.get_entity(scraped_grp)
            except Exception as e:
                print(f'{error} {r}Failed to get source group entity: {e}{rs}')
                continue
            
            # Join target group
            target_entity = None
            try:
                if choice == 0:  # Public group
                    client(JoinChannelRequest(target))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined target group')
                    target_entity = client.get_entity(target)
                else:  # Private group
                    if '/joinchat/' in target:
                        grp_hash = target.split('/joinchat/')[1]
                        client(ImportChatInviteRequest(grp_hash))
                        print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined target group')
                    target_entity = client.get_entity(target)
            except UserAlreadyParticipantError:
                pass
            except Exception as e:
                print(f'{error} {r}Failed to join target group: {e}{rs}')
                continue
            
            if not target_entity:
                print(f'{error} {r}Could not get target group entity{rs}')
                continue
            
            # Scrape members from source group
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Scraping members...')
            members = []
            offset = 0
            limit = 200
            
            while True:
                try:
                    participants = client(GetParticipantsRequest(
                        channel=scraped_grp_entity,
                        filter=ChannelParticipantsSearch(''),
                        offset=offset,
                        limit=limit,
                        hash=0
                    ))
                    
                    if not participants or not participants.users:
                        break
                        
                    members.extend(participants.users)
                    offset += len(participants.users)
                    
                    if len(participants.users) < limit:
                        break
                        
                except Exception as e:
                    print(f'{error} {r}Error scraping members: {e}{rs}')
                    break
            
            if not members:
                print(f'{error} {r}No members found in source group!{rs}')
                continue
            
            total_members = len(members)
            print(f'{info} {lg}Found {w}{total_members}{lg} members in source group')
            
            if index >= total_members:
                print(f'{info} {lg}No more members to add from this position{rs}')
                continue
            
            print(f'{info}{lg} Start index: {w}{index}')
            peer_flood_count = 0
            max_peer_flood_errors = 3
            
            # Add members to target group
            for j, user in enumerate(members[index:stop]):
                current_index = index + j
                
                if peer_flood_count >= max_peer_flood_errors:
                    print(f'{error} {r}Too many Peer Flood Errors! Switching to next account...{rs}')
                    break
                
                try:
                    if choice == 0:  # Public group
                        client(InviteToChannelRequest(target_entity, [user]))
                    else:  # Private group
                        client(AddChatUserRequest(target_entity.id, user, fwd_limit=42))
                    
                    user_name = user.first_name or "Unknown"
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_name} {lg}--> {cy}{target_entity.title}')
                    total_members_added += 1
                    
                    if sleep_time > 0:
                        print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time}{lg} second(s)')
                        time.sleep(sleep_time)
                        
                except UserPrivacyRestrictedError:
                    print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted{rs}')
                except PeerFloodError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error{rs}')
                    peer_flood_count += 1
                except ChatWriteForbiddenError:
                    print(f'{error} {r}Can\'t add to group. Contact group admin to enable members adding{rs}')
                    break
                except UserBannedInChannelError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups{rs}')
                    break
                except ChatAdminRequiredError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Admin rights needed to add{rs}')
                except UserAlreadyParticipantError:
                    print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User already in group{rs}')
                except FloodWaitError as e:
                    print(f'{error} {r}Flood wait: {e}{rs}')
                    break
                except Exception as e:
                    print(f'{error} {r}Error adding user: {e}{rs}')
                
                # Update index for resume capability
                index = current_index + 1
                
        except KeyboardInterrupt:
            print(f'\n{error} {r}Operation interrupted by user{rs}')
            if 'members' in locals() and index < len(members):
                log_status(scraped_grp, index)
            break
        except Exception as e:
            print(f'{error} {r}Error with account {phone}: {e}{rs}')
        finally:
            try:
                client.disconnect()
            except:
                pass
    
    # Final status
    print(f'\n{success} {lg}Adding session completed!{rs}')
    print(f'{info} {lg}Total members added: {w}{total_members_added}{rs}')
    
    if 'members' in locals() and index < len(members):
        log_status(scraped_grp, index)
        print(f'{info} {lg}Progress saved. You can resume later.{rs}')
    
    exit_window()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{error} {r}Program terminated by user{rs}')
        sys.exit(0)
    except Exception as e:
        print(f'{error} {r}Unexpected error: {e}{rs}')
        sys.exit(1)
