import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

ISLETME_BILGI = """
🌟 Salam! Men Bestseller UC boýunça soraglara kömek edýän bot! 🤖

🔥 Bestseller UC — Türkmenistanda iň amatly bahadan UC satyn almak hyzmaty 🇹🇲

💰 UC — Pubg Mobile oýnundaky pul birligi 💎

📞 Habarlaşmak üçin: +993 61 615 471 ýa-da @dvrn_777
📢 Kanalymyz: @BESTSELLER_UC

📌 Başga dürli umumy soraglara-da kömek etmäge synanyşaryn, ýöne diňe ahlakdan, syýasatdan ýa-da din bilen baglanyşykly temalardan gaça duraryn.
"""

# Gadagan temalar üçin açar sözler
BLACKLIST = [
    "din", "allah", "jeset", "syýasy", "porn", "ýarag", "intihar", "öldür", "adam öldür", 
    "seni kim döretdi", "ýaradyjy", "pylan dini", "Ýahudy", "Hristian", "Musulman", "Ilon Mask"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Grupda diňe at bilen bellenende jogap ber
    if update.message.chat.type in ['group', 'supergroup']:
        if not context.bot.username.lower() in update.message.text.lower():
            return

    user_message = update.message.text.replace(f"@{context.bot.username}", "").strip()

    if any(term in user_message.lower() for term in BLACKLIST):
        await update.message.reply_text("Bagyşlaň, bu tema boýunça kömek edip bilemok.")
        return

    prompt = (
        f"{ISLETME_BILGI}\n\n"
        f"Sorag:\n{user_message}\n\n"
        f"⚠️ Edebe laýyk we umumy maglumatlara jogap ber, ýöne dini, syýasy ýa ahlakdan daş temalara geçme."
    )

    try:
        response = model.generate_content(prompt)
        bot_reply = response.text

    except Exception as e:
        bot_reply = "Bagyşlaň, näsazlyk ýüze çykdy."

    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    print("Bot işleýär... Synap görüň!")
    asyncio.run(app.run_polling())
