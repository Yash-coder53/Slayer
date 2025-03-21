from Slayer.core.bot import Slayer
from Slayer.core.dir import dirr
from Slayer.core.git import git
from Slayer.core.userbot import Userbot
from Slayer.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Slayer()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
