import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "BU YERGA TOKENINGNI QO'Y"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Bu — zamonaviy va tez ishlaydigan Telegram bot 🚀\n"
        "Pastdagi buyruqlardan foydalaning:\n\n"
        "🔹 /start — Boshlash\n"
        "🔹 /help — Yordam\n"
        "🔹 /about — Bot haqida"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Botdan foydalanish:\n\n"
        "➡️ /start — Botni ishga tushirish\n"
        "➡️ /about — Bot haqida ma'lumot\n\n"
        "Agar savollaringiz bo‘lsa, yozing 🙂"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bu bot Python va python-telegram-bot kutubxonasi yordamida yozilgan.\n"
        "⚡️ Tez, ishonchli va serverga mos!\n\n"
        "📈 Kelajakda premium funksiyalar, statistikalar va AI qo‘shiladi."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
