import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("14125888"))
API_HASH = getenv("ba80aeb31471c5762fe6736112029576")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("8118009991:AAEDlne-l_v8aMkdsB5KDOT8PF9rASBhqjY")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("mongodb+srv://rohillayash281:rohillayash281@cluster0.35b8c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("-1002325306088", True))

# Get this value from @LeafRobot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 6748827895))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Yash-coder53/Slayer",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "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", True
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/slayer_logs")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/WE_ARE_LEGIONS")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

#Dont edit this line !!
MITWA = [ "<b>нєу</b> {0}, 💗\n\n๏ ᴛʜɪs ɪs {1} !\n\n➻ {1} ʏᴏᴜʀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜsɪᴄ ʙᴏᴛ! EɴJᴏʏ sᴇᴀᴍʟᴇss 💓 ᴀᴄᴄᴇss ᴛᴏ ᴀɴʏ sᴏɴɢ ᴡɪᴛʜ ʟᴀɢ-ғʀᴇᴇ ᴘᴇʀғᴏʀᴍᴀɴᴄᴇ ᴀɴᴅ ᴛʜᴇ ʙᴇsᴛ ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ. sʟᴀʏᴇʀ ᴄᴜʀᴀᴛᴇs ᴘᴇʀsᴏɴᴀʟɪᴢᴇᴅ ᴘʟᴀʏʟɪsᴛs, ᴅɪsᴄᴏᴠᴇʀs ɴᴇᴡ ᴀʀᴛɪsᴛs, ᴀɴᴅ ᴇɴʜᴀɴᴄᴇs ʏᴏᴜʀ ʟɪsᴛᴇɴɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ, ᴍᴀᴋɪɴɢ ɪᴛ ᴛʜᴇ ᴘᴇʀғᴇᴄᴛ ᴄᴏᴍᴘᴀɴɪᴏɴ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ ᴍᴜsɪᴄᴀʟ ᴍᴏᴍᴇɴᴛs 🦋. ᴛᴜɴᴇ ɪɴ ɴᴏᴡ!.\n\n<b><u>Sᴜᴘᴘᴏʀᴛᴇᴅ Pʟᴀᴛғᴏʀᴍs :</b></u> ʏᴏᴜᴛᴜʙᴇ, sᴘᴏᴛɪғʏ, ʀᴇssᴏ, ᴀᴘᴘʟᴇ ᴍᴜsɪᴄ ᴀɴᴅ sᴏᴜɴᴅᴄʟᴏᴜᴅ.\n──────────────────\n<b>๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs🦋.</b> "  ,
        ]


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("BQDXi0AAOV37fTYLR_uW_vf16XKs3_UhBIzX9Q2hyaREV8JXl0w3pFcJavToy2VpwdG3C3RbHJwT0L-xmmt9S1lJUGKVQLsqJ3W80I0ZB_l_OACmqh_Eruix07I3zE-ewIe8URSRa_wrhxDE7jPj_fUHX6grimNhWQM2W2eqS4s1dSLSR4-5jN8P3GhPzEZS2wkFMtKXzHw8vbeN-0CZ6QsTDydclc1IFHEDWFdHQh-IrZ5A1LvQ8iJOE6kDXAYbV6jEmkjemUeUGG9nv3Hv0mFOB_-JHXjoN-fz2pWYQKRYYf3vlzk2STzG6lyVtdW3fVsNI7-hUE-WhrAiK88qZa2lwcI1VgAAAAHNN4qaAA", True)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://te.legra.ph/file/25efe6aa029c6baea73ea.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://te.legra.ph/file/b8a0c1a00db3e57522b53.jpg"
)
PLAYLIST_IMG_URL = "https://te.legra.ph/file/4ec5ae4381dffb039b4ef.jpg"
STATS_IMG_URL = "https://envs.sh/Gbw.jpg"
TELEGRAM_AUDIO_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
TELEGRAM_VIDEO_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 2300**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
