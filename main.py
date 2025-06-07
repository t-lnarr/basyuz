import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Gemini sazlamak
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Doly maglumat
ISLETME_BILGI = """
🌟 Salam! Men Bestseller UC barada islendik soraglaryňyza kömek edip bilýän bot! 🤖

🔥 Bestseller UC — Türkmenistanda iň amatly bahadan UC hyzmatydyr! 🇹🇲

💰 UC — Pubg Mobile oýnundaky esasy pul birligi 💎

Näme üçin Bestseller UC?
✅ Ynamdar
✅ Amatly
✅ Tiz
✅ 7/24 elýeterli ⏰

📞 Habarlaşmak üçin: +993 61 615 471 ýa-da admin @dvrn_777
📢 Kanalymyz: @BESTSELLER_UC
"""

# Ahlak we hyzmatdan daşarky temalar (has anyk)
SENSITIVELIST = [
    "din", "allah", "jeset", "syýasy", "porno", "ýaragy", "seni kim döretdi", "seni kim ýasady", "ýaradyjy", "intihar", "terror"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Grupda diňe bot bellenende jogap ber
    if update.message.chat.type in ['group', 'supergroup']:
        if not context.bot.username.lower() in update.message.text.lower():
            return

    user_message = update.message.text.replace(f"@{context.bot.username}", "").strip()

    # Temany göz öňünde tutup filtrle
    if any(term in user_message.lower() for term in SENSITIVELIST):
        await update.message.reply_text("Bagyşlaň, bu tema boýunça kömek edip bilemok.")
        return

    # AI prompty
    prompt = (
        f"{ISLETME_BILGI}\n\n"
        f"Sorag:\n{user_message}\n\n"
        f"⚠️ Diňe UC hyzmatlary we PUBG bilen baglanyşykly soraglara kömek et. "
        f"Edebe degişli bolmadyk ýa-da başga temalara geçme."
    )

    try:
        response = model.generate_content(prompt)
        bot_reply = response.text

    except Exception as e:
        bot_reply = "Bagyşlaň, näsazlyk ýüze çykdy."

    await update.message.reply_text(bot_reply)

# Boty işledýäris
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    print("Bot işleýär... Synap görüň!")
    asyncio.run(app.run_polling())
