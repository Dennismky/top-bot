import os
import telebot
from dotenv import load_dotenv
from gemini import get_gemini_response

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    chat_id = message.chat.id

    if not user_text.strip():
        return

    lower_text = user_text.lower()
    spam_keywords = ["scam", "scammer", "lying", "liar"]
    if any(word in lower_text for word in spam_keywords):
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception as e:
            print(f"Failed to delete spam message: {e}")
        return 

    try:
        gemini_reply = get_gemini_response(user_text)
    except Exception as e:
        gemini_reply = f"Error getting response: {str(e)}"

    bot.send_message(chat_id, gemini_reply)

print("Bot is polling...")
bot.infinity_polling()
