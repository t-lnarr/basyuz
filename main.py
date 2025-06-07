import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Gemini modelini sazlamak
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Isletme maglumatlary we ýörelgeler
ISLETME_BILGI = """
🌟 Salam! Men Bestseller UC barada islendik soraglaryňyza jogap berip bilýän kömekçi bot! 🤖

🔥 Bestseller UC — Türkmenistanda iň amatly bahadan UC satyn almakda #1 hyzmatdyr! 🇹🇲

💰 UC — Pubg Mobile oýnundaky esasy pul birligi 💎

Näme üçin Bestseller UC?
✅ Ynamdar
✅ Amatly
✅ Çalt
✅ 7/24 hyzmatda ⏰

📞 Habarlaşmak üçin: +993 61 615 471 ýa-da admin: @dvrn_777
📢 Telegram kanalymyz: @BESTSELLER_UC

🛑 Diňe şu hyzmat barada maglumat berýärin. Başga soraglara jogap beremok.
"""

# Gara sanaw — nädogry ýa-da baglanyşyksyz soraglar
BLACKLIST = [
    "seni kim döretdi", "seni kim ýasady", "sen kim", "allah", "dini", "syýasy", "ýaradyjy"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Grup söhbetde diňe bot ady bellenende jogap ber
    if update.message.chat.type in ['group', 'supergroup']:
        if not context.bot.username.lower() in update.message.text.lower():
            return

    user_message = update.message.text.replace(f"@{context.bot.username}", "").strip().lower()

    # Gara sanaw barlagy
    if any(blk in user_message for blk in BLACKLIST):
        await update.message.reply_text("Bu barada kömek edip bilemok.")
        return

    # Prompt
    full_prompt = (
        ISLETME_BILGI +
        "\n\nSiziň soragyňyz:\n" + user_message +
        "\n\n⚠️ Diňe ýokardaky hyzmat barada maglumat ber. Başga temalar boýunça jogap bermerin!"
    )

    try:
        response = model.generate_content(full_prompt)
        bot_reply = response.text

        # Uýgun däl söz barlagy
        if any(bad in bot_reply.lower() for bad in ["bagyşlaň", "bilmeýärin"]):
            bot_reply = "Bu barada kömek edip bilemok."

    except Exception as e:
        bot_reply = "Bagyşlaň, näsazlyk ýüze çykdy."

    await update.message.reply_text(bot_reply)

# Boty işe girizmek
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    print("Bot işleýär... Telegram arkaly synap görüň.")
    asyncio.run(app.run_polling())
