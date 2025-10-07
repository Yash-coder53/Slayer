# corrected_script.py
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, ChannelParticipantsSearch, User
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
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
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = lg + '[' + w + 'i' + lg + ']' + rs
error = lg + '[' + r + '!' + lg + ']' + rs
success = w + '[' + lg + '*' + w + ']' + rs
INPUT = lg + '[' + cy + '~' + lg + ']' + rs
plus = w + '[' + lg + '+' + w + ']' + rs
minus = w + '[' + lg + '-' + w + ']' + rs

API_ID = 3910389
API_HASH = '86f861352f0ab76a251866059a6adbd6'
SESSIONS_DIR = 'sessions'

if not os.path.isdir(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR, exist_ok=True)

def banner():
    b = [
        ' _____     _            __   ___      __ _______    _____',
        '/ ____|   |  |          /\\    \\ \\   / / |  ____|  |   __ \\',
        '| (___ |  |  |         /  \\    \\ \\_/ /  | |__     |   |__) |',
        ' \\___ \\ |  |        / /\\ \\   \\   /    |  __|    |   _  /',
        ' ____) |  |  |____   / ____ \\   | |     | |____   | | \\ \\',
        '|_____/   |_______| /_/    \\_\\ |_|     |______|  |_|  \\_\\',
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{rs}')
    print(f'{lg}   Version: {w}1.2{lg} | Author: {w}Cryptonian{rs}\n')

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

# Load accounts from vars.txt (pickled list of tuples like (phone, ...))
def load_accounts(path='vars.txt'):
    accounts = []
    if not os.path.exists(path):
        print(f'{error} {w}{path} not found. Create vars.txt with pickled account tuples first.{rs}')
        return accounts
    with open(path, 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

accounts = load_accounts()
if not accounts:
    print(f'{error} No accounts loaded. Exiting.{rs}')
    sys.exit(1)

# Check for banned accounts
print('\n' + info + lg + ' Checking for banned accounts...' + rs)
banned = []
for a in accounts:
    phn = a[0]
    print(f'{plus}{phn}')
    client = TelegramClient(os.path.join(SESSIONS_DIR, phn), API_ID, API_HASH)
    try:
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phn)
                print('OK')
            except PhoneNumberBannedError:
                print(f'{error} {w}{phn} {r}is banned!{rs}')
                banned.append(a)
    except Exception as e:
        print(f'{error} Error connecting {phn}: {e}')
    finally:
        try:
            client.disconnect()
        except:
            pass

for z in banned:
    accounts.remove(z)
    print(info + lg + ' Banned account removed (remove permanently using manager.py)' + rs)

print(info + ' Sessions checked!')
time.sleep(1)
clr()
banner()

def log_status(scraped, index):
    with open('status.dat', 'wb') as f:
        pickle.dump([scraped, int(index)], f)
    print(f'{info}{lg} Session stored in {w}status.dat{lg}')

def exit_window():
    input(f'\n{cy} Press enter to exit...')
    clr()
    banner()
    sys.exit()

# Resume or new
try:
    with open('status.dat', 'rb') as f:
        status = pickle.load(f)
        resume = input(f'{INPUT}{cy} Resume scraping members from {w}{status[0]}{lg}? [y/n]: {r}')
        if 'y' in resume.lower():
            scraped_grp = status[0]
            index = int(status[1])
        else:
            try:
                os.remove('status.dat')
            except:
                pass
            scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
            index = 0
except (FileNotFoundError, EOFError):
    scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
    index = 0

# Reload accounts (so we can split them to use vs rest)
accounts = load_accounts()
if not accounts:
    print(f'{error} No accounts available. Exiting.{rs}')
    sys.exit(1)

print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
number_of_accs = int(input(f'{INPUT}{cy} Enter number of accounts to use: {r}'))
if number_of_accs < 1:
    print(f'{error} Invalid number of accounts.{rs}')
    sys.exit(1)

print(f'{info}{cy} Choose an option{lg}')
print(f'{cy}[0]{lg} Add to public group')
print(f'{cy}[1]{lg} Add to private group')
choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
target = input(f'{INPUT}{cy} Enter {"public" if choice == 0 else "private"} group link: {r}')

print(f'{grey}_'*50)

to_use = [x for x in accounts[:number_of_accs]]
# keep the remaining accounts back into vars.txt
with open('vars.txt', 'wb') as f:
    for a in accounts[number_of_accs:]:
        pickle.dump(a, f)

sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None{w}]: {r}'))

print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')
adding_status = 0
approx_members_count = 0

for acc in to_use:
    stop = index + 60
    session_path = os.path.join(SESSIONS_DIR, acc[0])
    c = TelegramClient(session_path, API_ID, API_HASH)
    print(f'{plus}{grey} User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
    try:
        c.start(acc[0])
    except Exception as e:
        print(f'{error} Failed to start session for {acc[0]}: {e}')
        continue

    try:
        acc_name = c.get_me().first_name
    except:
        acc_name = acc[0]

    try:
        # Join the scraping group if needed
        if '/joinchat/' in scraped_grp:
            g_hash = scraped_grp.split('/joinchat/')[1]
            try:
                c(ImportChatInviteRequest(g_hash))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except UserAlreadyParticipantError:
                print(f'{plus} Already participant in scrape group')
            except Exception as e:
                print(f'{error} Could not import scrape invite: {e}')
        else:
            try:
                c(JoinChannelRequest(scraped_grp))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except Exception as e:
                # it might already be joined or invalid link
                print(f'{error} Join scrape group failed: {e}')

        scraped_grp_entity = c.get_entity(scraped_grp)

        # Prepare target
        if choice == 0:
            # public group/channel (use JoinChannelRequest)
            try:
                c(JoinChannelRequest(target))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined target group to add')
            except UserAlreadyParticipantError:
                pass
            except Exception as e:
                print(f'{error} Could not join target public group: {e}')
            target_entity = c.get_entity(target)
            # For InviteToChannelRequest we may need InputPeerChannel for some Telethon versions:
            try:
                target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
            except Exception:
                target_details = target_entity
        else:
            # private (join via invite hash)
            try:
                grp_hash = target.split('/joinchat/')[1]
                try:
                    c(ImportChatInviteRequest(grp_hash))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined private target group')
                except UserAlreadyParticipantError:
                    pass
            except IndexError:
                print(f'{error} Provided private link does not contain /joinchat/ hash.')
            target_entity = c.get_entity(target)
            target_details = target_entity

    except Exception as e:
        print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to prepare groups: {e}')
        c.disconnect()
        continue

    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
    try:
        members = []
        my_filter = ChannelParticipantsSearch('')
        offset = 0
        limit = 200
        while True:
            participants = c(GetParticipantsRequest(channel=scraped_grp_entity, filter=my_filter, offset=offset, limit=limit, hash=0))
            if not participants.users:
                break
            members.extend(participants.users)
            offset += len(participants.users)
            # if fewer than limit, probably last page
            if len(participants.users) < limit:
                break
    except Exception as e:
        print(f'{error}{r} Couldn\'t scrape members: {e}')
        c.disconnect()
        continue

    approx_members_count = len(members)
    if approx_members_count == 0:
        print(f'{error}{lg} No members found to add! Skipping this account.')
        c.disconnect()
        continue

    if index >= approx_members_count:
        print(f'{error}{lg} Index >= members count, nothing to add from this account.')
        c.disconnect()
        continue

    print(f'{info}{lg} Start index: {w}{index}')
    peer_flood_status = 0

    for user in members[index:stop]:
        index += 1
        if peer_flood_status >= 10:
            print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
            break
        try:
            # If user is a User object, pass the id or the User object depending on API
            if choice == 0:
                # Invite to channel (public)
                try:
                    c(InviteToChannelRequest(target_details, [user]))
                except TypeError:
                    # Try passing user.id if passing user object fails
                    c(InviteToChannelRequest(target_details, [user.id if isinstance(user, User) else user]))
            else:
                # Add to chat (private). AddChatUserRequest(chat_id, user_id, fwd_limit)
                user_id = user.id if isinstance(user, User) else user
                try:
                    c(AddChatUserRequest(target_entity.id, user_id, 42))
                except TypeError:
                    # older/newer versions might expect peer object
                    c(AddChatUserRequest(target_entity, user_id, 42))

            user_name = getattr(user, 'first_name', str(getattr(user, 'id', 'unknown')))
            target_title = getattr(target_entity, 'title', str(getattr(target_entity, 'id', 'target')))
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_name} {lg}--> {cy}{target_title}')
            adding_status += 1
            print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
            time.sleep(sleep_time)
        except UserPrivacyRestrictedError:
            print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted Error')
            continue
        except PeerFloodError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
            peer_flood_status += 1
            continue
        except ChatWriteForbiddenError:
            print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
            if index < approx_members_count:
                log_status(scraped_grp, index)
            c.disconnect()
            exit_window()
        except UserBannedInChannelError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
            break
        except ChatAdminRequiredError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
            continue
        except UserAlreadyParticipantError:
            print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User is already a participant')
            continue
        except FloodWaitError as e:
            print(f'{error}{r} Flood wait: {e}')
            break
        except ValueError:
            print(f'{error}{r} Error in Entity')
            continue
        except KeyboardInterrupt:
            print(f'{error}{r} ---- Adding Terminated ----')
            if index < len(members):
                log_status(scraped_grp, index)
            c.disconnect()
            exit_window()
        except Exception as e:
            print(f'{error} Unexpected error: {e}')
            continue

    try:
        if index < approx_members_count:
            log_status(scraped_grp, index)
            c.disconnect()
            exit_window()
    except Exception:
        c.disconnect()
        exit_window()

if adding_status != 0:
    print(f"\n{info}{lg} Adding session ended. Total added: {w}{adding_status}")
else:
    print(f"\n{info}{lg} No members were added in this run.")
