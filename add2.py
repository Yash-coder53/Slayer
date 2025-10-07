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

def load_accounts():
    """Load accounts from file with error handling"""
    accounts = []
    if not os.path.exists('vars.txt'):
        print(f'{error} {r}vars.txt file not found!{rs}')
        return accounts
        
    try:
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
    except Exception as e:
        print(f'{error} {r}Error loading accounts: {e}{rs}')
    return accounts

def save_accounts(accounts):
    """Save accounts to file"""
    try:
        with open('vars.txt', 'wb') as f:
            for account in accounts:
                pickle.dump(account, f)
    except Exception as e:
        print(f'{error} {r}Error saving accounts: {e}{rs}')

def check_banned_accounts():
    """Check and remove banned accounts"""
    print('\n' + info + lg + ' Checking for banned accounts...' + rs)
    accounts = load_accounts()
    if not accounts:
        return []
    
    banned = []
    valid_accounts = []
    
    for account in accounts:
        if not account or len(account) < 1:
            continue
            
        phone = account[0]
        print(f'{plus}{grey} Checking {lg}{phone}')
        
        client = TelegramClient(f'sessions/{phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
        try:
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f'{plus} {lg}OK{rs}')
                    valid_accounts.append(account)
                except PhoneNumberBannedError:
                    print(f'{error} {w}{phone} {r}is banned!{rs}')
                    banned.append(account)
            else:
                valid_accounts.append(account)
                print(f'{plus} {lg}Authorized{rs}')
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
            pickle.dump([scraped, int(index)], f)
        print(f'{info}{lg} Session stored in {w}status.dat{lg}')
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
    return None

def exit_window():
    input(f'\n{cy} Press enter to exit...')
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
        exit_window()
    
    print(f'{info}{lg} Total valid accounts: {w}{len(accounts)}')
    
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
            scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {rs}')
            index = 0
    else:
        scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {rs}')
        index = 0
    
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
    
    target = input(f'{INPUT}{cy} Enter {"public" if choice == 0 else "private"} group link: {rs}')
    
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
    
    adding_status = 0
    total_members_added = 0
    
    for i, acc in enumerate(to_use):
        if not acc or len(acc) < 1:
            continue
            
        phone = acc[0]
        stop = index + 60
        
        print(f'{plus}{grey} User {i+1}/{len(to_use)}: {cy}{phone}{lg} -- Starting session... ')
        
        client = TelegramClient(f'sessions/{phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
        
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
                    adding_status += 1
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
            if index < total_members:
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
    
    if index < total_members:
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
