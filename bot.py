import os
import sqlite3
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "SENINGBOTUSERNAME"  # <-- bot username ni yoz (masalan: valyuta_pro_bot)

# ===== DATABASE =====
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrer_id INTEGER,
    referrals INTEGER DEFAULT 0
)
""")
conn.commit()

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        referrer_id = None

        if args:
            referrer_id = int(args[0])
            if referrer_id != user_id:
                cursor.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id=?", (referrer_id,))
        
        cursor.execute(
            "INSERT INTO users (user_id, referrer_id) VALUES (?, ?)",
            (user_id, referrer_id)
        )
        conn.commit()

    cursor.execute("SELECT referrals FROM users WHERE user_id=?", (user_id,))
    referrals = cursor.fetchone()[0]

    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    await update.message.reply_text(
        f"👋 Salom!\n\n"
        f"👥 Sizning referallaringiz: {referrals}\n\n"
        f"🔗 Sizning link:\n{referral_link}\n\n"
        f"Do‘stlaringizni taklif qiling 🚀"
    )

# ===== ADMIN STATS =====
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_ID = 8598603565  # <-- o‘z telegram id ni yoz

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    await update.message.reply_text(f"📊 Jami foydalanuvchilar: {total}")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()

if __name__ == "__main__":
    main()
