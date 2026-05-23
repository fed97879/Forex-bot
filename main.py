from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, timedelta

BOT_TOKEN = "8861278241:AAGlvZpkBLWZ6aFtfWoXSK0ZtsUZlkmDM9w"
ADMIN_ID = 1704863382
CHANNEL_ID = "@Forex_fm_pro_bot"
VISA_CARD = "4165 8585 7947 7312"
PRICE = 99

subscribers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = [
        [InlineKeyboardButton("💎 Купить — $99/мес", callback_data="buy")],
        [InlineKeyboardButton("📊 Мой статус", callback_data="status")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")]
    ]
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"🚀 Forex Signal Pro\n\n"
        f"📈 EUR/USD, GBP/USD, XAU/USD\n"
        f"🎯 Точность: 75-85%\n"
        f"📊 5-10 сигналов в день\n\n"
        f"💰 Цена: ${PRICE} / 30 дней",
        reply_markup=InlineKeyboardMarkup(kb))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user = q.from_user
    if q.data == "buy":
        kb = [[InlineKeyboardButton("✅ Я оплатил", callback_data="paid")]]
        await q.edit_message_text(
            f"💳 Оплата\n\nПереведите ${PRICE} на карту:\n\n"
