import logging
from Slayer.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from Slayer import InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl

logging.basicConfig(level=logging.INFO)

TOKEN = '8118009991:AAEDlne-l_v8aMkdsB5KDOT8PF9rASBhqjY'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Slayer Music Bot!")

def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Use /play to play a song or /stop to stop the music.")

def play(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a song name or URL.")
        return

    song_name = ' '.join(context.args)
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(song_name, download=False)
            url = info['formats'][0]['url']
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=url)
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error playing song: {e}")

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Music stopped.")

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("/start", start))
    dp.add_handler(CommandHandler("/help", help_command))
    dp.add_handler(CommandHandler("/play", play))
    dp.add_handler(CommandHandler("/stop", stop))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
