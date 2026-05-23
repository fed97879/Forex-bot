import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8861278241:AAGlvZpkBLWZ6aFtfWoXSK0ZtsUZlkmDM9w"
ADMIN_ID = 5861278241

async def start(update, context):
    await update.message.reply_text("Привет! Я Forex Signal Bot 📊")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
