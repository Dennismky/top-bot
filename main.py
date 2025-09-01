import os
import requests
import json
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_input = message.text

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))

        print("Status Code:", response.status_code) 
        print("Raw Response:", response.text)      
        print("Gemini API Key:", GEMINI_API_KEY)

        response.raise_for_status()  

        response_json = response.json()
        print("Gemini Response JSON:", json.dumps(response_json, indent=2))

        candidates = response_json.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                reply_text = parts[0].get("text", " Gemini gave no text.")
            else:
                reply_text = "Gemini returned no parts."
        else:
            reply_text = " Gemini returned no candidates."

    except Exception as e:
        reply_text = f"Error: {e}"

    bot.reply_to(message, reply_text)

bot.infinity_polling()
