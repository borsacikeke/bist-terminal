import json
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "")
WEBAPP_URL = "https://borsacikeke.github.io/bist-terminal"
BOT_USERNAME = "BistTerminalBot"
KANAL = "@ekonomiveborsa"
KANAL_LINK = "https://t.me/ekonomiveborsa"
SONUCLAR_URL = "https://borsacikeke.github.io/bist-terminal/sonuclar.json"
DAVET_DOSYA = "/tmp/davetler.json"
OZEL_KILIT = 10

YASAL_UYARI = (
    "⚠️ *YASAL UYARI*\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Bu platform yalnızca algoritmik teknik analiz sinyalleri sunar. "
    "Buradaki veriler *yatırım tavsiyesi değildir*. "
    "Göstergeler otomatik hesaplanmakta olup hatalar içerebilir. "
    "Kendi grafik analizinizi yapmanız ve bir yatırım danışmanına başvurmanız önerilir. "
    "Sermaye piyasası işlemleri *risk içerir*.\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

def davet_yukle():
    try:
        with open(DAVET_DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def davet_kaydet(data):
    with open(DAVET_DOSYA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def davet_sayisi(user_id, data):
    return len(data.get(str(user_id), {}).get("davet_edilenler", []))

def kilitli_mi(user_id, data, gereken=5):
    return davet_sayisi(user_id, data) < gereken

def ozel_kilitli_mi(user_id, data):
    return davet_sayisi(user_id, data) < OZEL_KILIT

def veri_yukle():
    try:
        r = requests.get(SONUCLAR_URL, timeout=10)
        return r.json()
    except:
        return None

async def kanal_uye_mi(context, user_id):
    try:
        uye = await context.bot.get_chat_member(chat_id=KANAL, user_id=user_id)
        return uye.status not in ["left", "kicked", "banned"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = str(user.id)
    isim    = user.first_name
    data    = davet_yukle()

    if context.args:
        davet_eden_id = context.args[0]
        if davet_eden_id != user_id and davet_eden_id in data:
            davet_edilenler = data[davet_eden_id].get("davet_edilenler", [])
            if user_id not in davet_edilenler:
                davet_edilenler.append(user_id)
                data[davet_eden_id]["davet_edilenler"] = davet_edilenler
                davet_kaydet(data)
                try:
                    yeni_sayi = len(davet_edilenler)
                    mesaj = (
                        f"🎉 Yeni davet! *{isim}* bota katıldı.\n"
                        f"Toplam davetiniz: *{yeni_sayi}*\n"
                    )
                    if yeni_sayi >= OZEL_KILIT:
                        mesaj += "🏅 Özel Tarama Bölümü açıldı!"
                    elif yeni_sayi >= 5:
                        mesaj += "🔓 Altın grafikleri açıldı!"
                    await context.bot.send_message(
                        chat_id=int(davet_eden_id),
                        text=mesaj,
                        parse_mode="Markdown"
                    )
                except:
                    pass

    uye = await kanal_uye_mi(context, int(user_id))
    if not uye:
        keyboard = [
            [InlineKeyboardButton("📢 Kanala Katıl", url=KANAL_LINK)],
            [InlineKeyboardButton("✅ Katıldım, Devam Et", callback_data="kanal_kontrol")],
        ]
        await update.message.reply_text(
            f"👋 Merhaba *{isim}*!\n\n"
            f"Botu kullanmak için önce kanalımıza katılman gerekiyor 👇\n\n"
            f"📢 *Ekonomi ve Borsa Kanalı*\n`{KANAL_LINK}`\n\n"
            f"Kanala katıldıktan sonra aşağıdaki butona bas ✅",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    if user_id not in data:
        data[user_id] = {"isim": isim, "davet_edilenler": []}
        davet_kaydet(data)

    await ana_menu_gonder(update.message, user_id, isim, data)

async def ana_menu_gonder(message, user_id, isim, data):
    veri  = veri_yukle()
    tarih = veri["tarih"] if veri else "—"
    altin = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Altin"] if veri else []
    gumus = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Gumus"] if veri else []
    bronz = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Bronz"] if veri else []
    ozel  = [k for k, v in veri["hisseler"].items() if v.get("ozel_tarama")]       if veri else []

    sayi          = davet_sayisi(user_id, data)
    altin_kilitli = kilitli_mi(user_id, data)
    ozel_kilitli  = ozel_kilitli_mi(user_id, data)

    if sayi >= OZEL_KILIT:
        durum = f"🏅 *{sayi}* davet — tüm özellikler açık"
    elif sayi >= 5:
        durum = f"🔓 *{sayi}* davet — altın açık · özel {sayi}/{OZEL_KILIT}"
    else:
        durum = f"🔒 *{sayi}/5* davet — özellikler kilitli"

    ozel_param  = "1" if not ozel_kilitli  else "0"
    altin_param = "1" if not altin_kilitli else "0"
    webapp_full = f"{WEBAPP_URL}?ozel={ozel_param}&altin={altin_param}"

    keyboard = [
        [InlineKeyboardButton(
            "🏅 Özel Tarama" + (f" ({len(ozel)})" if not ozel_kilitli else " 🔒"),
            callback_data="ozel_tarama"
        )],
        [InlineKeyboardButton("📊 Terminali Aç", web_app=WebAppInfo(url=webapp_full))],
        [InlineKeyboardButton("🏆 Altın Grafikleri" + (" 🔒" if altin_kilitli else ""), callback_data="altin_grafik")],
        [InlineKeyboardButton("👥 Davet Linkim", callback_data="davet_link")],
        [InlineKeyboardButton("⚠️ Yasal Uyarı", callback_data="yasal_uyari")],
    ]

    await message.reply_text(
        f"📊 *BIST TEKNİK ANALİZ TERMİNALİ*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 Hoş geldin, *{isim}*!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 Son güncelleme: `{tarih}`\n\n"
        f"🏆 Altın: *{len(altin)}* · 🥈 Gümüş: *{len(gumus)}* · 🥉 Bronz: *{len(bronz)}*\n"
        f"🏅 Özel: *{len(ozel)}* hisse\n\n"
        f"{durum}\n\n"
        f"_Bu platform yatırım tavsiyesi vermez. Risk içerir._",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def buton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = str(query.from_user.id)
    isim    = query.from_user.first_name
    await query.answer()
    data = davet_yukle()

    if query.data == "kanal_kontrol":
        uye = await kanal_uye_mi(context, int(user_id))
        if uye:
            await query.message.delete()
            if user_id not in data:
                data[user_id] = {"isim": isim, "davet_edilenler": []}
                davet_kaydet(data)
            await ana_menu_gonder(query.message, user_id, isim, data)
        else:
            await query.answer("❌ Henüz kanala katılmadın!", show_alert=True)
        return

    uye = await kanal_uye_mi(context, int(user_id))
    if not uye:
        keyboard = [
            [InlineKeyboardButton("📢 Kanala Katıl", url=KANAL_LINK)],
            [InlineKeyboardButton("✅ Katıldım, Devam Et", callback_data="kanal_kontrol")],
        ]
        await query.message.reply_text(
            "⚠️ Kanaldan ayrılmışsın! Devam etmek için kanala katılman gerekiyor.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if query.data == "yasal_uyari":
        await query.message.reply_text(YASAL_UYARI, parse_mode="Markdown")

    elif query.data == "davet_link":
        sayi       = davet_sayisi(user_id, data)
        davet_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        await query.message.reply_text(
            f"👥 *Davet Linkin*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"`{davet_link}`\n\n"
            f"📊 Davet durumun: *{sayi}*\n\n"
            f"• 5 davet → 🏆 Altın hisse grafikleri\n"
            f"• 10 davet → 🏅 Özel Tarama Bölümü\n\n"
            f"_Her davet farklı bir kullanıcı olmalıdır._",
            parse_mode="Markdown"
        )

    elif query.data == "altin_grafik":
        if kilitli_mi(user_id, data):
            sayi       = davet_sayisi(user_id, data)
            davet_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Bu özellik kilitli!*\n\n"
                f"Altın grafikleri için *5 kişi davet* gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/5*\n\n"
                f"Davet linkin:\n`{davet_link}`",
                parse_mode="Markdown"
            )
            return

        veri = veri_yukle()
        if not veri:
            await query.message.reply_text("Veri bulunamadı.")
            return

        altin_hisseler = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Altin"]
        if not altin_hisseler:
            await query.message.reply_text("Bugün altın sinyal veren hisse bulunamadı.")
            return

        await query.message.reply_text(
            f"🏆 *{len(altin_hisseler)} Altın Sinyal*\n_Yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )
        for ad in altin_hisseler:
            h = veri["hisseler"][ad]
            sinyaller = h["sinyaller"][:4]
            await query.message.reply_text(
                f"🏆 *{ad}* — {h['kapanis']} TL\n"
                f"RSI: {h['rsi']}\n"
                f"_{', '.join(sinyaller)}_\n\n"
                f"⚠️ _Yatırım tavsiyesi değildir._",
                parse_mode="Markdown"
            )

    elif query.data == "ozel_tarama":
        if ozel_kilitli_mi(user_id, data):
            sayi       = davet_sayisi(user_id, data)
            davet_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Özel Tarama Bölümü Kilitli!*\n\n"
                f"Bu özel bölüme erişmek için *{OZEL_KILIT} farklı kişiyi* davet etmen gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/{OZEL_KILIT}*\n\n"
                f"Davet linkin:\n`{davet_link}`\n\n"
                f"_Her davet farklı bir kullanıcı olmalıdır._",
                parse_mode="Markdown"
            )
            return

        veri = veri_yukle()
        if not veri:
            await query.message.reply_text("Veri bulunamadı.")
            return

        ozel_hisseler = [k for k, v in veri["hisseler"].items() if v.get("ozel_tarama")]
        if not ozel_hisseler:
            await query.message.reply_text(
                "🏅 *Özel Tarama*\n\nBugün koşulları sağlayan hisse bulunamadı.",
                parse_mode="Markdown"
            )
            return

        await query.message.reply_text(
            f"🏅 *ÖZEL TARAMA — {len(ozel_hisseler)} Hisse*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"_Yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )
        for ad in ozel_hisseler:
            h = veri["hisseler"][ad]
            await query.message.reply_text(
                f"🏅 *{ad}* — {h['kapanis']} TL\n"
                f"RSI: {h['rsi']}\n\n"
                f"⚠️ _Yatırım tavsiyesi değildir._",
                parse_mode="Markdown"
            )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buton))
    print("✅ Bot çalışıyor...")
    app.run_polling()
