import os
import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= TOKEN =================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN topilmadi. Server env ga token qo‘ying!")

# ================= API =================
CBU_API = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"

def get_rate(code):
    try:
        data = requests.get(CBU_API, timeout=10).json()
        for item in data:
            if item["Ccy"] == code:
                return item
    except Exception as e:
        logging.error(f"API xatolik: {e}")
    return None

# ================= MENYU =================
def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["💵 USD", "💶 EUR", "💷 RUB"],
            ["🧮 Kalkulyator", "📊 Grafik"],
            ["🎯 Maqsad", "📰 Yangiliklar"],
            ["ℹ️ Yordam"]
        ],
        resize_keyboard=True
    )

# ================= HANDLERLAR =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Bu bot orqali valyuta kurslari, kalkulyator va boshqa foydali xizmatlardan foydalanishingiz mumkin.\n\n"
        "Pastdagi menyudan tanlang 👇",
        reply_markup=main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Yordam:\n\n"
        "💵 USD/EUR/RUB — joriy kurslar\n"
        "🧮 Kalkulyator — valyuta hisoblash\n"
        "📊 Grafik — kurslar grafigi\n"
        "🎯 Maqsad — shaxsiy maqsad yozish\n\n"
        "Bot 24/7 ishlaydi 🤖",
        reply_markup=main_menu()
    )

async def usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_rate("USD")
    if rate:
        await update.message.reply_text(
            f"💵 USD kursi:\n\n"
            f"💰 {rate['Rate']} so‘m\n"
            f"📅 {rate['Date']}",
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text("❌ USD kursini olishda xatolik.")

async def eur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_rate("EUR")
    if rate:
        await update.message.reply_text(
            f"💶 EUR kursi:\n\n"
            f"💰 {rate['Rate']} so‘m\n"
            f"📅 {rate['Date']}",
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text("❌ EUR kursini olishda xatolik.")

async def rub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_rate("RUB")
    if rate:
        await update.message.reply_text(
            f"💷 RUB kursi:\n\n"
            f"💰 {rate['Rate']} so‘m\n"
            f"📅 {rate['Date']}",
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text("❌ RUB kursini olishda xatolik.")

async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["calc"] = True
    await update.message.reply_text(
        "🧮 Kalkulyator\n\n"
        "Format:\n"
        "100 USD\n"
        "250 EUR\n\n"
        "Shu tarzda yozing 👇"
      )

async def graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Grafik hozircha demo rejimda.\n\n"
        "Tez orada real grafik qo‘shiladi 📈",
        reply_markup=main_menu()
    )

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = True
    await update.message.reply_text(
        "🎯 Maqsadingizni yozing:\n\nMasalan: 1 000 000 so‘m yig‘ish"
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 Yangiliklar bo‘limi tez orada qo‘shiladi.\n\n"
        "Hozircha asosiy funksiyalardan foydalaning 😊",
        reply_markup=main_menu()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get("calc"):
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text("❌ Noto‘g‘ri format. Masalan: 100 USD")
            return

        amount, code = parts
        if not amount.replace(".", "").isdigit():
            await update.message.reply_text("❌ Miqdorni raqam bilan yozing.")
            return

        rate = get_rate(code.upper())
        if not rate:
            await update.message.reply_text("❌ Bunday valyuta topilmadi.")
            return

        result = float(amount) * float(rate["Rate"])
        await update.message.reply_text(
            f"📊 Natija:\n\n"
            f"{amount} {code.upper()} = {result:,.2f} so‘m",
            reply_markup=main_menu()
        )
        context.user_data["calc"] = False
        return

    if context.user_data.get("goal"):
        await update.message.reply_text(
            f"🎯 Maqsad saqlandi:\n{text}",
            reply_markup=main_menu()
        )
        context.user_data["goal"] = False
        return

    await update.message.reply_text("❗️ Iltimos, menyudan foydalaning 👇", reply_markup=main_menu())

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.Regex("^💵 USD$"), usd))
    app.add_handler(MessageHandler(filters.Regex("^💶 EUR$"), eur))
    app.add_handler(MessageHandler(filters.Regex("^💷 RUB$"), rub))
    app.add_handler(MessageHandler(filters.Regex("^🧮 Kalkulyator$"), calculator))
    app.add_handler(MessageHandler(filters.Regex("^📊 Grafik$"), graph))
    app.add_handler(MessageHandler(filters.Regex("^🎯 Maqsad$"), goal))
    app.add_handler(MessageHandler(filters.Regex("^📰 Yangiliklar$"), news))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Yordam$"), help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
