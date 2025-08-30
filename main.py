import os
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8464474423:AAFCBOKq-LS5PQUsE8WA-q4qc3u_nFf7eCc"
BOT_USERNAME: Final = "top-bot"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We help Instagram accounts grow their following.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We pay 5 euros for every account you provide.")

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed or "hey" in processed:
        return "Hello there, welcome."
    if "hi" in processed:
        return "Hi, welcome"
    if "how are you" in processed or "i'm good" in processed or "im good" in processed or "am good" in processed:
        return "Glad to hear that. How can I assist you today?"

    if "just got here" in processed or "i just got here" in processed:
        return "Welcome, feel free to ask me anything you want to know."

    if "explain" in processed or "explain to me" in processed:
        return "We support Instagram accounts to grow their following. We pay 5 euros per account after tasks are done."

    if "how much" in processed or "amount" in processed or "payment" in processed:
        return "We pay 5 euros per account that you help us with."

    if "register" in processed or "sign up" in processed:
        return "Yes, if you don't have an Instagram account, you need to download it from the Play Store (Android) or App Store (iOS) and register."

    if "bye" in processed or "goodbye" in processed:
        return "Goodbye, talk to you later."

    if any(word in processed for word in ["scam", "scammer", "lying", "liar"]):
        return "BLOCK_USER"

    if "stupid" in processed or "dumb" in processed or "idiot" in processed:
        return "I'm doing my best to assist you. Let's keep our conversation respectful."

    if "?" in processed:
        return "let me get back to you in a minute."
    
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    print(f'User ({user_id}) in {message_type} sent: {text}')

    response: str = handle_response(text)

    if response == "BLOCK_USER":
        try:
            # Delete their message
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            
            # Try banning (works in groups/channels only)
            if message_type != "private":
                await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            
            print(f"User {user_id} flagged as spam and blocked.")
        except Exception as e:
            print(f"Error blocking user {user_id}: {e}")
        return

    if response:  
        print('Bot:', response)
        await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print("polling...")
    app.run_polling(poll_interval=3)
