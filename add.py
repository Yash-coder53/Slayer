# import libraries
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUser Request
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

# Load accounts from file
accounts = []
with open('vars.txt', 'rb') as f:
    while True:
        try:
            accounts.append(pickle.load(f))
        except EOFError:
            break

# Check for banned accounts
print('\n' + info + lg + ' Checking for banned accounts...' + rs)
banned = []
for a in accounts:
    phn = a[0]
    print(f'{plus}{grey} Checking {lg}{phn}')
    clnt = TelegramClient(f'sessions/{phn}', 3910389, '86f861352f0ab76a251866059a6adbd6')
    clnt.connect()
    if not clnt.is_user_authorized():
        try:
            clnt.send_code_request(phn)
            print('OK')
        except PhoneNumberBannedError:
            print(f'{error} {w}{phn} {r}is banned!{rs}')
            banned.append(a)
    clnt.disconnect()

for z in banned:
    accounts.remove(z)
    print(info + lg + ' Banned account removed[Remove permanently using manager.py]' + rs)

print(info + ' Sessions created!')
clr()
banner()

# Function to log scraping details
def log_status(scraped, index):
    with open('status.dat', 'wb') as f:
        pickle.dump([scraped, int(index)], f)
    print(f'{info}{lg} Session stored in {w}status.dat{lg}')

def exit_window():
    input(f'\n{cy} Press enter to exit...')
    clr()
    banner()
    sys.exit()

# Read user details
try:
    with open('status.dat', 'rb') as f:
        status = pickle.load(f)
        resume = input(f'{INPUT}{cy} Resume scraping members from {w}{status[0]}{lg}? [y/n]: {r}')
        if 'y' in resume:
            scraped_grp = status[0]
            index = int(status[1])
        else:
            os.remove('status.dat') if os.name == 'nt' else os.remove('status.dat')
            scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
            index = 0
except (FileNotFoundError, EOFError):
    scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
    index = 0

# Load all the accounts
accounts = []
with open('vars.txt', 'rb') as f:
    while True:
        try:
            accounts.append(pickle.load(f))
        except EOFError:
            break

print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
number_of_accs = int(input(f'{INPUT}{cy} Enter number of accounts to use: {r}'))
print(f'{info}{cy} Choose an option{lg}')
print(f'{cy}[0]{lg} Add to public group')
print(f'{cy}[1]{lg} Add to private group')
choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
target = input(f'{INPUT}{cy} Enter {"public" if choice == 0 else "private"} group link: {r}')

print(f'{grey}_'*50)

to_use = [x for x in accounts[:number_of_accs]]
for l in to_use: accounts.remove(l)

with open('vars.txt', 'wb') as f:
    for a in accounts:
        pickle.dump(a, f)
    for ab in to_use:
        pickle.dump(ab, f)

sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None{w}]: {r}'))

print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')
adding_status = 0
approx_members_count = 0

for acc in to_use:
    stop = index + 60
    c = TelegramClient(f'sessions/{acc[0]}', 3910389, '86f861352f0ab76a251866059a6adbd6')
    print(f'{plus}{grey} User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
    c.start(acc[0])
    acc_name = c.get_me().first_name
    try:
        if '/joinchat/' in scraped_grp:
            g_hash = scraped_grp.split('/joinchat/')[1]
            try:
                c(ImportChatInviteRequest(g_hash))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except UserAlreadyParticipantError:
                pass 
        else:
            c(JoinChannelRequest(scraped_grp))
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
        
        scraped_grp_entity = c.get_entity(scraped_grp)
        
        if choice == 0:
            c(JoinChannelRequest(target))
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
            target_entity = c.get_entity(target)
            target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
        else:
            try:
                grp_hash = target.split('/joinchat/')[1]
                c(ImportChatInviteRequest(grp_hash))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
            except UserAlreadyParticipantError:
                pass
            target_entity = c.get_entity(target)
            target_details = target_entity
    except Exception as e:
        print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group')
        print(f'{error} {r}{e}')
        continue

    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
    try:
        members = []
        while_condition = True
        my_filter = ChannelParticipantsSearch('')
        offset = 0
        while while_condition:
            participants = c(GetParticipantsRequest(channel=scraped_grp, offset=offset, filter=my_filter, limit=200, hash=0))
            members.extend(participants.users)
            offset += len(participants.users)
            if len(participants.users) < 1:
                while_condition = False
    except Exception as e:
        print(f'{error}{r} Couldn\'t scrape members')
        print(f'{error}{r} {e}')
        continue

    approx_members_count = len(members)
    assert approx_members_count != 0
    if index >= approx_members_count:
        print(f'{error}{lg} No members to add!')
        continue

    print(f'{info}{lg} Start: {w}{index}')
    peer_flood_status = 0

    for user in members[index:stop]:
        index += 1
        if peer_flood_status == 10:
            print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
            break
        try:
            if choice == 0:
                c(InviteToChannelRequest(target_details, [user]))
            else:
                c(AddChatUser Request(target_details.id, user, 42))
            user_id = user.first_name
            target_title = target_entity.title
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
            adding_status += 1
            print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
            time.sleep(sleep_time)
        except UserPrivacyRestrictedError:
            print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User  Privacy Restricted Error')
            continue
        except PeerFloodError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
            peer_flood_status += 1
            continue
        except ChatWriteForbiddenError:
            print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
            if index < approx_members_count:
                log_status(scraped_grp, index)
            exit_window()
        except UserBannedInChannelError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
            break
        except ChatAdminRequiredError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
            continue
        except UserAlreadyParticipantError:
            print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User  is already a participant')
            continue
        except FloodWaitError as e:
            print(f'{error}{r} {e}')
            break
        except ValueError:
            print(f'{error}{r} Error in Entity')
            continue
        except KeyboardInterrupt:
            print(f'{error}{r} ---- Adding Terminated ----')
            if index < len(members):
                log_status(scraped_grp, index)
            exit_window()
        except Exception as e:
            print(f'{error} {e}')
            continue

if adding_status != 0:
    print(f"\n{info}{lg} Adding session ended")
try:
    if index < approx_members_count:
        log_status(scraped_grp, index)
        exit_window()
except:
    exit_window()
