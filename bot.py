import json
import os
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN        = os.environ.get("TOKEN", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPO", "borsacikeke/bist-terminal")

WEBAPP_URL   = "https://borsacikeke.github.io/bist-terminal"
BOT_USERNAME = "BistTerminalBot"
KANAL        = "@ekonomiveborsa"
KANAL_LINK   = "https://t.me/ekonomiveborsa"
SONUCLAR_URL = "https://borsacikeke.github.io/bist-terminal/sonuclar.json"
OZEL_KILIT   = 10

YASAL_UYARI = (
    "⚠️ *YASAL UYARI*\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Bu platform yalnızca algoritmik teknik analiz sinyalleri sunar. "
    "Buradaki veriler *yatırım tavsiyesi değildir*. "
    "Göstergeler otomatik hesaplanmakta olup hatalar içerebilir. "
    "Sermaye piyasası işlemleri *risk içerir*.\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

# ── GitHub okuma / yazma ──────────────────────────────────────────────────────

def github_oku(dosya_adi):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{dosya_adi}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 404:
            return {}, None
        r.raise_for_status()
        data = r.json()
        sha  = data["sha"]
        icerik = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(icerik), sha
    except Exception as e:
        print(f"GitHub okuma hatası ({dosya_adi}): {e}")
        return {}, None

def github_yaz(dosya_adi, data, sha=None):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{dosya_adi}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        icerik  = base64.b64encode(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
        payload = {"message": f"{dosya_adi} guncelleme", "content": icerik}
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["content"]["sha"]
    except Exception as e:
        print(f"GitHub yazma hatası ({dosya_adi}): {e}")
        return sha

def davet_yukle():
    return github_oku("davetler.json")

def davet_kaydet(data, sha=None):
    return github_yaz("davetler.json", data, sha)

def favori_yukle():
    return github_oku("favoriler.json")

def favori_kaydet(data, sha=None):
    return github_yaz("favoriler.json", data, sha)

# ── Yardımcı fonksiyonlar ─────────────────────────────────────────────────────

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

def macd_yorum(h):
    if h.get("macd") is not None and h.get("macd_sinyal") is not None:
        if h["macd"] > h["macd_sinyal"]:
            return "📈 Pozitif"
        else:
            return "📉 Negatif"
    return "—"

def hacim_yorum(h):
    oran = h.get("hacim_oran")
    if oran is None:
        return "—"
    if oran >= 2.5:
        return f"🔥 Çok Yüksek ({oran}x)"
    elif oran >= 1.5:
        return f"📊 Yüksek ({oran}x)"
    else:
        return f"Normal ({oran}x)"

def rsi_yorum(rsi):
    if rsi is None:
        return "—"
    if rsi < 30:
        return "🟢 Aşırı Satım"
    elif rsi < 45:
        return "🟡 Satım Bölgesi"
    elif rsi < 55:
        return "⚪ Nötr"
    elif rsi < 70:
        return "🟡 Alım Bölgesi"
    else:
        return "🔴 Aşırı Alım"

# ── /start ────────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = str(user.id)
    isim    = user.first_name
    data, sha = davet_yukle()

    if context.args:
        davet_eden_id = context.args[0]
        if davet_eden_id != user_id and davet_eden_id in data:
            davet_edilenler = data[davet_eden_id].get("davet_edilenler", [])
            if user_id not in davet_edilenler:
                davet_edilenler.append(user_id)
                data[davet_eden_id]["davet_edilenler"] = davet_edilenler
                sha = davet_kaydet(data, sha)
                try:
                    yeni_sayi = len(davet_edilenler)
                    mesaj = f"🎉 Yeni davet! *{isim}* bota katıldı.\nToplam davetiniz: *{yeni_sayi}*\n"
                    if yeni_sayi >= OZEL_KILIT:
                        mesaj += "🏅 Özel Tarama Bölümü açıldı!"
                    elif yeni_sayi >= 5:
                        mesaj += "🔓 Altın grafikleri açıldı!"
                    await context.bot.send_message(chat_id=int(davet_eden_id), text=mesaj, parse_mode="Markdown")
                except:
                    pass

    uye = await kanal_uye_mi(context, int(user_id))
    if not uye:
        keyboard = [
            [InlineKeyboardButton("📢 Kanala Katıl", url=KANAL_LINK)],
            [InlineKeyboardButton("✅ Katıldım, Devam Et", callback_data="kanal_kontrol")],
        ]
        await update.message.reply_text(
            f"👋 Merhaba *{isim}*!\n\nBotu kullanmak için önce kanalımıza katılman gerekiyor 👇\n\n"
            f"📢 *Ekonomi ve Borsa Kanalı*\n`{KANAL_LINK}`\n\nKanala katıldıktan sonra aşağıdaki butona bas ✅",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    if user_id not in data:
        data[user_id] = {"isim": isim, "davet_edilenler": []}
        sha = davet_kaydet(data, sha)

    await ana_menu_gonder(update.message, user_id, isim, data)

# ── /hisse komutu ─────────────────────────────────────────────────────────────

async def hisse_sorgula(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📊 *Hisse Sorgula*\n\nKullanım: `/hisse THYAO`\nÖrnek: `/hisse GARAN`",
            parse_mode="Markdown"
        )
        return

    ad   = context.args[0].upper().strip()
    veri = veri_yukle()
    if not veri:
        await update.message.reply_text("❌ Veri yüklenemedi.")
        return

    h = veri["hisseler"].get(ad)
    if not h:
        await update.message.reply_text(f"❌ *{ad}* bulunamadı. Hisse kodunu kontrol et.")
        return

    seviye_emoji = {"Altin": "🏆", "Gumus": "🥈", "Bronz": "🥉"}.get(h.get("altin", ""), "—")
    sinyaller    = h.get("sinyaller", [])

    mesaj = (
        f"📊 *{ad}* Hisse Analizi\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💰 Kapanış: *{h['kapanis']} TL*\n"
        f"🏅 Seviye: {seviye_emoji} {h.get('altin', 'Sinyal Yok')}\n\n"
        f"📈 *Göstergeler*\n"
        f"• RSI: `{h.get('rsi', '—')}` — {rsi_yorum(h.get('rsi'))}\n"
        f"• MACD: {macd_yorum(h)}\n"
        f"• Hacim: {hacim_yorum(h)}\n\n"
    )

    if sinyaller:
        mesaj += f"🔔 *Aktif Sinyaller* ({len(sinyaller)})\n"
        for s in sinyaller[:8]:
            mesaj += f"• {s}\n"
        if len(sinyaller) > 8:
            mesaj += f"_...ve {len(sinyaller)-8} sinyal daha_\n"

    if h.get("ozel_tarama"):
        mesaj += "\n🏅 *Özel Tarama sinyali mevcut!*\n"

    mesaj += f"\n📅 Güncelleme: {veri.get('tarih', '—')}\n\n⚠️ _Yatırım tavsiyesi değildir._"

    keyboard = [[
        InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
        InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
    ]]

    await update.message.reply_text(
        mesaj, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ── /favori ve /favorisil komutları ──────────────────────────────────────────

async def favori_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if not context.args:
        fav_data, _ = favori_yukle()
        favoriler   = fav_data.get(user_id, [])
        if not favoriler:
            await update.message.reply_text(
                "⭐ *Favorilerin*\n\nHenüz favori eklemedin.\n\nEklemek için: `/favori THYAO`\nSilmek için: `/favorisil THYAO`",
                parse_mode="Markdown"
            )
        else:
            veri  = veri_yukle()
            mesaj = f"⭐ *Favorilerin* ({len(favoriler)} hisse)\n━━━━━━━━━━━━━━━━━━━━\n\n"
            for ad in favoriler:
                if veri and ad in veri["hisseler"]:
                    h      = veri["hisseler"][ad]
                    seviye = {"Altin": "🏆", "Gumus": "🥈", "Bronz": "🥉"}.get(h.get("altin", ""), "—")
                    mesaj += f"{seviye} *{ad}* — {h['kapanis']} TL | RSI: {h.get('rsi','—')} | Hacim: {hacim_yorum(h)}\n"
                else:
                    mesaj += f"• *{ad}*\n"
            mesaj += "\n⚠️ _Yatırım tavsiyesi değildir._"
            await update.message.reply_text(mesaj, parse_mode="Markdown")
        return

    ad   = context.args[0].upper().strip()
    veri = veri_yukle()
    if not veri or ad not in veri["hisseler"]:
        await update.message.reply_text(f"❌ *{ad}* bulunamadı.", parse_mode="Markdown")
        return

    fav_data, sha = favori_yukle()
    favoriler     = fav_data.get(user_id, [])
    if ad in favoriler:
        await update.message.reply_text(f"ℹ️ *{ad}* zaten favorilerinde.", parse_mode="Markdown")
        return

    favoriler.append(ad)
    fav_data[user_id] = favoriler
    favori_kaydet(fav_data, sha)
    await update.message.reply_text(f"⭐ *{ad}* favorilerine eklendi!\n\nSinyal çıkınca seni haberdar ederim.", parse_mode="Markdown")

async def favori_sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Kullanım: `/favorisil THYAO`", parse_mode="Markdown")
        return

    ad            = context.args[0].upper().strip()
    fav_data, sha = favori_yukle()
    favoriler     = fav_data.get(user_id, [])
    if ad not in favoriler:
        await update.message.reply_text(f"❌ *{ad}* favorilerinde yok.", parse_mode="Markdown")
        return

    favoriler.remove(ad)
    fav_data[user_id] = favoriler
    favori_kaydet(fav_data, sha)
    await update.message.reply_text(f"🗑️ *{ad}* favorilerinden silindi.", parse_mode="Markdown")

# ── Ana menü ──────────────────────────────────────────────────────────────────

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
        [InlineKeyboardButton("🏅 Özel Tarama" + (f" ({len(ozel)})" if not ozel_kilitli else " 🔒"), callback_data="ozel_tarama")],
        [InlineKeyboardButton("📊 Terminali Aç", web_app=WebAppInfo(url=webapp_full))],
        [InlineKeyboardButton("🏆 Altın Grafikleri" + (" 🔒" if altin_kilitli else ""), callback_data="altin_grafik")],
        [InlineKeyboardButton("⭐ Favorilerim", callback_data="favorilerim"),
         InlineKeyboardButton("👥 Davet Linkim", callback_data="davet_link")],
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
        f"💡 `/hisse THYAO` yazarak anlık analiz al\n"
        f"⭐ `/favori THYAO` ile favori ekle\n\n"
        f"_Bu platform yatırım tavsiyesi vermez. Risk içerir._",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ── Buton işlemleri ───────────────────────────────────────────────────────────

async def buton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = str(query.from_user.id)
    isim    = query.from_user.first_name
    await query.answer()
    data, sha = davet_yukle()

    if query.data == "kanal_kontrol":
        uye = await kanal_uye_mi(context, int(user_id))
        if uye:
            await query.message.delete()
            if user_id not in data:
                data[user_id] = {"isim": isim, "davet_edilenler": []}
                davet_kaydet(data, sha)
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
            f"👥 *Davet Linkin*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"`{davet_link}`\n\n"
            f"📊 Davet durumun: *{sayi}*\n\n"
            f"• 5 davet → 🏆 Altın hisse grafikleri\n"
            f"• 10 davet → 🏅 Özel Tarama Bölümü\n\n"
            f"_Her davet farklı bir kullanıcı olmalıdır._",
            parse_mode="Markdown"
        )

    elif query.data == "favorilerim":
        fav_data, _ = favori_yukle()
        favoriler   = fav_data.get(user_id, [])
        if not favoriler:
            await query.message.reply_text(
                "⭐ *Favorilerin boş!*\n\n`/favori THYAO` yazarak hisse ekleyebilirsin.",
                parse_mode="Markdown"
            )
            return
        veri  = veri_yukle()
        mesaj = f"⭐ *Favorilerin* ({len(favoriler)} hisse)\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for ad in favoriler:
            if veri and ad in veri["hisseler"]:
                h      = veri["hisseler"][ad]
                seviye = {"Altin": "🏆", "Gumus": "🥈", "Bronz": "🥉"}.get(h.get("altin", ""), "—")
                mesaj += (
                    f"{seviye} *{ad}* — {h['kapanis']} TL\n"
                    f"   RSI: `{h.get('rsi','—')}` | MACD: {macd_yorum(h)} | Hacim: {hacim_yorum(h)}\n\n"
                )
            else:
                mesaj += f"• *{ad}*\n"
        mesaj += "\n⚠️ _Yatırım tavsiyesi değildir._"
        await query.message.reply_text(mesaj, parse_mode="Markdown")

    elif query.data == "altin_grafik":
        if kilitli_mi(user_id, data):
            sayi       = davet_sayisi(user_id, data)
            davet_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Bu özellik kilitli!*\n\nAltın grafikleri için *5 kişi davet* gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/5*\n\nDavet linkin:\n`{davet_link}`",
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
            h         = veri["hisseler"][ad]
            sinyaller = h["sinyaller"][:4]
            keyboard  = [[
                InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
                InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
            ]]
            await query.message.reply_text(
                f"🏆 *{ad}* — {h['kapanis']} TL\n"
                f"RSI: `{h.get('rsi','—')}` | MACD: {macd_yorum(h)} | Hacim: {hacim_yorum(h)}\n"
                f"_{', '.join(sinyaller)}_\n\n"
                f"⚠️ _Yatırım tavsiyesi değildir._",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif query.data == "ozel_tarama":
        if ozel_kilitli_mi(user_id, data):
            sayi       = davet_sayisi(user_id, data)
            davet_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Özel Tarama Bölümü Kilitli!*\n\n"
                f"Bu özel bölüme erişmek için *{OZEL_KILIT} farklı kişiyi* davet etmen gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/{OZEL_KILIT}*\n\nDavet linkin:\n`{davet_link}`\n\n"
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
            f"🏅 *ÖZEL TARAMA — {len(ozel_hisseler)} Hisse*\n━━━━━━━━━━━━━━━━━━━━\n_Yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )
        for ad in ozel_hisseler:
            h        = veri["hisseler"][ad]
            keyboard = [[
                InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
                InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
            ]]
            await query.message.reply_text(
                f"🏅 *{ad}* — {h['kapanis']} TL\n"
                f"RSI: `{h.get('rsi','—')}` | MACD: {macd_yorum(h)} | Hacim: {hacim_yorum(h)}\n\n"
                f"⚠️ _Yatırım tavsiyesi değildir._",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# ── Başlat ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hisse", hisse_sorgula))
    app.add_handler(CommandHandler("favori", favori_ekle))
    app.add_handler(CommandHandler("favorisil", favori_sil))
    app.add_handler(CallbackQueryHandler(buton))
    print("✅ Bot çalışıyor...")
    app.run_polling()
