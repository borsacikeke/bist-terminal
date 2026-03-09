import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8739320823:AAFHMgR7xSRO3J3ZPzmCOhT1MeQFXc6zPmM"
WEBAPP_URL = "https://borsacikeke.github.io/bist-terminal"

YASAL_UYARI = (
    "⚠️ *YASAL UYARI*\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Bu platform yalnızca algoritma tabanlı teknik analiz sinyalleri sunar. "
    "Buradaki veriler *yatırım tavsiyesi değildir*. Göstergeler otomatik olarak hesaplanmakta olup hatalar içerebilir. "
    "Her yatırımcının kendi grafik analizini yapması ve bir yatırım danışmanına başvurması önerilir. "
    "Sermaye piyasalarında işlemler *risk içerir*, geçmiş performans gelecek getiriyi garanti etmez.\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

def veri_yukle():
    try:
        with open("C:/bist_terminal/sonuclar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    isim = update.effective_user.first_name
    veri = veri_yukle()
    tarih = veri["tarih"] if veri else "—"

    altin = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Altin"] if veri else []
    gumus = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Gumus"] if veri else []
    bronz = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Bronz"] if veri else []

    keyboard = [
        [InlineKeyboardButton("📊 Terminali Aç", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🏆 Altın Grafikleri", callback_data="altin_grafik")],
        [InlineKeyboardButton("⚠️ Yasal Uyarı", callback_data="yasal_uyari")],
    ]

    await update.message.reply_text(
        f"📊 *BIST TEKNİK ANALİZ TERMİNALİ*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 Hoş geldin, *{isim}*!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 Son güncelleme: `{tarih}`\n\n"
        f"🏆 Altın: *{len(altin)}* hisse\n"
        f"🥈 Gümüş: *{len(gumus)}* hisse\n"
        f"🥉 Bronz: *{len(bronz)}* hisse\n\n"
        f"_Bu platform yatırım tavsiyesi vermez. Tüm sinyaller algoritmik olup risk içerir._",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def buton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "yasal_uyari":
        await query.message.reply_text(YASAL_UYARI, parse_mode="Markdown")

    elif query.data == "altin_grafik":
        veri = veri_yukle()
        if not veri:
            await query.edit_message_text("Veri bulunamadı.")
            return

        altin_hisseler = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Altin"]

        if not altin_hisseler:
            await query.edit_message_text("Bugün altın sinyal veren hisse bulunamadı.")
            return

        await query.edit_message_text(
            f"🏆 *{len(altin_hisseler)} Altın Sinyal* grafiği gönderiliyor...\n"
            f"_Grafikler algoritmik analiz içerir, yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )

        for ad in altin_hisseler:
            grafik_yolu = f"C:/bist_terminal/grafikler/{ad}.png"
            if os.path.exists(grafik_yolu):
                sinyaller = [s for s in veri["hisseler"][ad]["sinyaller"][:4]]
                caption = f"🏆 *{ad}* — {veri['hisseler'][ad]['kapanis']} TL\n_{', '.join(sinyaller)}_\n\n⚠️ _Yatırım tavsiyesi değildir._"
                with open(grafik_yolu, "rb") as f:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=f,
                        caption=caption,
                        parse_mode="Markdown"
                    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buton))
    print("✅ Bot çalışıyor...")
    app.run_polling()