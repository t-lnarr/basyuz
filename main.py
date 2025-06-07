import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Gemini modelini yapılandır
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

ISLETME_BILGI = """
Salam men Bestseller UC barada islendik soraglaryňyza jogap berip bilýän kömekçi bot.

Bestseller UC - Türkmenistanda iň amatly bahadan UC almakda No1 hyzmatdyr.

UC - Pubg Mobile oýunyndaky pul birligi

Näme üçin Bestseller UC ? Sebäbi ynamly, amatly, tiz we 7/24 online.

Habarlaşmak üçin nomerimiz: +99361615471 ýa-da admin @dvrn_777

Telegram kanalymyz: @BESTSELLER_UC
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        full_prompt = ISLETME_BILGI + "\n\nMüşteri sorusu:\n" + user_message
        response = model.generate_content(full_prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Hata oluştu: {e}"

    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    print("Bot çalışıyor... Telegram'da mesaj gönder.")
    asyncio.run(app.run_polling())
