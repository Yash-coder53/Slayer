# group_adder.py
import os
import sys
import time
import pickle
import random
from colorama import init, Fore
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, ChannelParticipantsSearch, User
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest

# ======= CONFIG =======
API_ID = 3910389
API_HASH = "86f861352f0ab76a251866059a6adbd6"
SESSIONS_DIR = "sessions"
ACCOUNTS_FILE = "vars.txt"
STATUS_FILE = "status.dat"

init()
r, g, y, c, w, rs = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.WHITE, Fore.RESET
info = g + "[i]" + rs
error = r + "[!]" + rs
success = g + "[*]" + rs

# -----------------------------
# Utility
# -----------------------------
def clr():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"{g}Telegram Group Scraper & Adder v1.0{rs}\n")

def load_accounts():
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"{error} vars.txt not found.")
        sys.exit(1)
    with open(ACCOUNTS_FILE, "rb") as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

def log_status(scraped_group, index):
    with open(STATUS_FILE, "wb") as f:
        pickle.dump([scraped_group, int(index)], f)
    print(f"{info} Progress saved. Resume from {index} next time.")

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    clr()
    banner()

    accounts = load_accounts()
    print(f"{info} Loaded {len(accounts)} accounts.")

    # Check banned accounts
    active_accounts = []
    for phone, *_ in accounts:
        client = TelegramClient(f"{SESSIONS_DIR}/{phone}", API_ID, API_HASH)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                print(f"{success} {phone} ✅ OK")
                active_accounts.append((phone,))
            except PhoneNumberBannedError:
                print(f"{error} {phone} ❌ BANNED")
        else:
            active_accounts.append((phone,))
        client.disconnect()

    if not active_accounts:
        print(f"{error} No active accounts left.")
        sys.exit(1)

    # Resume or new scraping
    if os.path.exists(STATUS_FILE):
        scraped_grp, index = pickle.load(open(STATUS_FILE, "rb"))
        resume = input(f"{info} Resume scraping from {scraped_grp}? (y/n): ").lower()
        if resume != "y":
            os.remove(STATUS_FILE)
            scraped_grp = input("Enter group link to scrape from: ")
            index = 0
    else:
        scraped_grp = input("Enter group link to scrape from: ")
        index = 0

    target_grp = input("Enter target group link to add members: ")
    num_accounts = int(input("Number of accounts to use: "))
    delay = int(input("Delay between adds (seconds): "))

    accounts_to_use = active_accounts[:num_accounts]
    print(f"{info} Using {len(accounts_to_use)} accounts for adding.")

    adding_status = 0

    for acc in accounts_to_use:
        phone = acc[0]
        client = TelegramClient(f"{SESSIONS_DIR}/{phone}", API_ID, API_HASH)
        print(f"{info} Starting session for {phone}")
        try:
            client.start(phone)
        except Exception as e:
            print(f"{error} Cannot start session: {e}")
            continue

        # Join source group
        try:
            if "/joinchat/" in scraped_grp:
                invite_hash = scraped_grp.split("/joinchat/")[1]
                try:
                    client(ImportChatInviteRequest(invite_hash))
                except UserAlreadyParticipantError:
                    pass
            else:
                client(JoinChannelRequest(scraped_grp))
            source_entity = client.get_entity(scraped_grp)
            print(f"{success} Joined source group")
        except Exception as e:
            print(f"{error} Failed to join source group: {e}")
            continue

        # Join target group
        try:
            if "/joinchat/" in target_grp:
                target_hash = target_grp.split("/joinchat/")[1]
                try:
                    client(ImportChatInviteRequest(target_hash))
                except UserAlreadyParticipantError:
                    pass
            else:
                client(JoinChannelRequest(target_grp))
            target_entity = client.get_entity(target_grp)
            target_peer = InputPeerChannel(target_entity.id, target_entity.access_hash)
            print(f"{success} Joined target group")
        except Exception as e:
            print(f"{error} Failed to join target group: {e}")
            continue

        # Scrape members
        print(f"{info} Scraping members...")
        members = []
        offset = 0
        while True:
            participants = client(GetParticipantsRequest(
                channel=source_entity,
                filter=ChannelParticipantsSearch(""),
                offset=offset,
                limit=200,
                hash=0
            ))
            if not participants.users:
                break
            members.extend(participants.users)
            offset += len(participants.users)
        print(f"{success} Total members scraped: {len(members)}")

        if index >= len(members):
            print(f"{error} All members already added.")
            continue

        # Add members
        print(f"{info} Starting adding from index {index}")
        peer_flood_errors = 0

        for user in members[index:index + 60]:
            if peer_flood_errors >= 10:
                print(f"{error} Too many PeerFlood errors. Stopping.")
                break

            try:
                if isinstance(user, User):
                    client(InviteToChannelRequest(target_peer, [user.id]))
                else:
                    client(InviteToChannelRequest(target_peer, [user]))

                print(f"{success} Added: {user.first_name}")
                adding_status += 1
                time.sleep(delay)

            except UserPrivacyRestrictedError:
                print(f"{error} Privacy restricted.")
                continue
            except PeerFloodError:
                print(f"{error} PeerFloodError! Skipping...")
                peer_flood_errors += 1
                continue
            except ChatWriteForbiddenError:
                print(f"{error} Cannot write to group. Need admin rights.")
                log_status(scraped_grp, index)
                sys.exit(1)
            except UserAlreadyParticipantError:
                print(f"{info} Already in group.")
                continue
            except FloodWaitError as e:
                print(f"{error} FloodWaitError: Wait {e.seconds}s.")
                time.sleep(e.seconds)
                continue
            except Exception as e:
                print(f"{error} Unexpected: {e}")
                continue

            index += 1

        log_status(scraped_grp, index)
        client.disconnect()

    print(f"\n{success} DONE. Total added: {adding_status}")


if __name__ == "__main__":
    main()
