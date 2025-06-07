import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

GEMINI_API_KEY = "AIzaSyB0PNcZ436meXYtVhR3fMDLxvo2FWpaD9g"
TELEGRAM_TOKEN = "7895951762:AAEiXgCZMER31DfZD7ET3-s0YezMl8KAATE"

# Gemini modelini yapılandır
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Sabit işletme bilgisi
ISLETME_BILGI = """
Sen bir pastanenin AI asistanısın. İşletme bilgileri:

Adı: Güneş Pastanesi
Adres: Türkmenbaşy cad. 12/A, Aşkabat
Telefon: +993 65 12 34 56
Çalışma saatleri: 09:00 - 21:00
Instagram: @gunespastanesi

Ürünler:
- Napolyon (25 TMT)
- Ballı tort (30 TMT)
- Çilekli pasta (35 TMT)

Sipariş alınmaz ama bilgi verilir.
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
print("Bot çalışıyor...")
app.run_polling()
