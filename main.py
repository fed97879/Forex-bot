from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, timedelta

BOT_TOKEN = "8861278241:AAGlvZpkBLWZ6aFtfWoXSK0ZtsUZlkmDM9w"
ADMIN_ID = 7068062973
CHANNEL_ID = "@Forex_fm_pro_bot"
VISA_CARD = "4111 1111 1111 1111"
PRICE = 1000

subscribers = {}
pending = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("💎 Купить подписку", callback_data="buy")],
          [InlineKeyboardButton("📊 Мой статус", callback_data="status")]]
    await update.message.reply_text(
        "👋 Добро пожаловать в Forex Signal Pro!\n\n"
        "📈 Сигналы EUR/USD, GBP/USD, XAU/USD\n"
        f"💰 Цена: {PRICE} руб / 30 дней",
        reply_markup=InlineKeyboardMarkup(kb))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user = q.from_user
    if q.data == "buy":
        pending[user.id] = True
        kb = [[InlineKeyboardButton("✅ Я оплатил", callback_data="paid")]]
        await q.edit_message_text(
            f"💳 Переведите {PRICE} руб на карту:\n\n"
            f"🏦 {VISA_CARD}\n\n"
            f"📝 Комментарий: FS_{user.id}\n\n"
            "После оплаты нажмите кнопку:",
            reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "paid":
        kb = [[InlineKeyboardButton("✅ Подтвердить", callback_data=f"ok_{user.id}"),
               InlineKeyboardButton("❌ Отклонить", callback_data=f"no_{user.id}")]]
        await context.bot.send_message(ADMIN_ID,
            f"💳 Новый платёж!\n👤 {user.full_name}\n🆔 {user.id}",
            reply_markup=InlineKeyboardMarkup(kb))
        await q.edit_message_text("⏳ Ожидайте подтверждения (5-30 минут)")
    elif q.data == "status":
        if user.id in subscribers and subscribers[user.id] > datetime.now():
            await q.edit_message_text(f"✅ Подписка активна до {subscribers[user.id].strftime('%d.%m.%Y')}")
        else:
            await q.edit_message_text("❌ Подписка не активна")
    elif q.data.startswith("ok_") and user.id == ADMIN_ID:
        uid = int(q.data.split("_")[1])
        subscribers[uid] = datetime.now() + timedelta(days=30)
        await context.bot.send_message(uid, "🎉 Подписка активирована на 30 дней!")
        await q.edit_message_text("✅ Подтверждено!")
    elif q.data.startswith("no_") and user.id == ADMIN_ID:
        uid = int(q.data.split("_")[1])
        await context.bot.send_message(uid, "❌ Платёж не подтверждён. Свяжитесь с @Feruz_fx1")
        await q.edit_message_text("❌ Отклонено!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Формат: /signal EURUSD BUY 1.0850 TP:1.0920 SL:1.0800")
        return
    parts = " ".join(context.args).upper().split()
    pair, direction, entry = parts[0], parts[1], parts[2]
    tp = next((p.split(":")[1] for p in parts if p.startswith("TP:")), "?")
    sl = next((p.split(":")[1] for p in parts if p.startswith("SL:")), "?")
    emoji = "🟢" if direction == "BUY" else "🔴"
    msg = f"{emoji} {pair} — {direction}\n📥 Вход: {entry}\n🎯 TP: {tp}\n🛡 SL: {sl}\n🕐 {datetime.now().strftime('%d.%m %H:%M')}"
    await context.bot.send_message(CHANNEL_ID, msg)
    await update.message.reply_text("✅ Сигнал отправлен!")

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or len(context.args) < 2:
        return
    uid, days = int(context.args[0]), int(context.args[1])
    subscribers[uid] = datetime.now() + timedelta(days=days)
    await context.bot.send_message(uid, f"🎉 Подписка активирована на {days} дней!")
    await update.message.reply_text("✅ Готово!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("give", give))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
