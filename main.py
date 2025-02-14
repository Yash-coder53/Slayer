from Slayer.ext import Updater, CommandHandler, MessageHandler
from Slayer import Update, ForceReply
from Slayer.ext import ContextTypes
import logging
from music import MusicHandler
from chatgpt import ChatGPTHandler
from banall import BanAllHandler

Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

TOKEN = "8118009991:AAFiOhf0RcBOzzGmLaL8lhu9aBQjHcnKMHE"

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands - answer in Telegram
    dp.add_handler(CommandHandler("/start", start))
    dp.add_handler(CommandHandler("/help", help_command))
    dp.add_handler(CommandHandler("/music", MusicHandler))
    dp.add_handler(CommandHandler("/gpt", ChatGPTHandler))
    dp.add_handler(CommandHandler("banall", BanAllHandler))

    # Start the Bot
    updater.start_polling()
    updater.idle()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

if name == "main":
    main()
