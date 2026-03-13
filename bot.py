import os
import json
import requests
import base64
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
from datetime import datetime
import pytz

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ── Sabitler ──────────────────────────────────────────────────────────────────
TOKEN        = os.environ.get("TOKEN", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPO", "borsacikeke/bist-terminal")
BOT_USERNAME = "BistTerminalBot"
KANAL        = "@ekonomiveborsa"
KANAL_LINK   = "https://t.me/ekonomiveborsa"
WEBAPP_URL   = "https://borsacikeke.github.io/bist-terminal"
SONUCLAR_URL = "https://borsacikeke.github.io/bist-terminal/sonuclar.json"
TR_TZ        = pytz.timezone("Europe/Istanbul")

DAVET_ESIK_ALTIN = 5   # Altın grafikleri
DAVET_ESIK_OZEL  = 10  # Tavan Tarama Grafikleri + özel terminal

YASAL_UYARI = (
    "⚠️ *YASAL UYARI*\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Bu platform yalnızca algoritmik teknik analiz sinyalleri sunar. "
    "Buradaki veriler *yatırım tavsiyesi değildir*. "
    "Göstergeler otomatik hesaplanmakta olup hatalar içerebilir. "
    "Sermaye piyasası işlemleri *risk içerir*.\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

# ── GitHub API ────────────────────────────────────────────────────────────────
GH_HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def gh_dosya_oku(dosya_adi):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{dosya_adi}"
        r = requests.get(url, headers=GH_HEADERS, timeout=10)
        if r.status_code == 200:
            icerik = r.json()
            veri = json.loads(base64.b64decode(icerik["content"]).decode("utf-8"))
            return veri, icerik["sha"]
    except:
        pass
    return {}, None

def gh_dosya_yaz(dosya_adi, veri, sha=None):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{dosya_adi}"
        icerik = base64.b64encode(
            json.dumps(veri, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("utf-8")
        payload = {"message": f"Bot güncelleme - {dosya_adi}", "content": icerik}
        if sha:
            payload["sha"] = sha
        requests.put(url, headers=GH_HEADERS, json=payload, timeout=15)
    except:
        pass

# ── Davet yönetimi ────────────────────────────────────────────────────────────
def davet_yukle():
    # davetler.json GitHub'dan okunur — mevcut verin KORUNUR
    veri, _ = gh_dosya_oku("davetler.json")
    return veri

def davet_kaydet(veri):
    _, sha = gh_dosya_oku("davetler.json")
    gh_dosya_yaz("davetler.json", veri, sha)

def davet_sayisi(user_id, data):
    return len(data.get(str(user_id), {}).get("davet_edilenler", []))

def ozel_erisim_var_mi(user_id, data):
    return davet_sayisi(user_id, data) >= DAVET_ESIK_OZEL

def altin_erisim_var_mi(user_id, data):
    return davet_sayisi(user_id, data) >= DAVET_ESIK_ALTIN

# ── Favori yönetimi ───────────────────────────────────────────────────────────
def favori_yukle():
    veri, _ = gh_dosya_oku("favoriler.json")
    return veri

def favori_kaydet(veri):
    _, sha = gh_dosya_oku("favoriler.json")
    gh_dosya_yaz("favoriler.json", veri, sha)

# ── Veri çek ──────────────────────────────────────────────────────────────────
def veri_yukle():
    try:
        r = requests.get(SONUCLAR_URL + "?t=" + str(int(datetime.now().timestamp())), timeout=10)
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
        return "📈 Pozitif" if h["macd"] > h["macd_sinyal"] else "📉 Negatif"
    return "—"

def hacim_yorum(h):
    oran = h.get("hacim_oran")
    if oran is None:
        return "—"
    if oran >= 2.5:
        return f"🔥 Çok Yüksek ({oran}x)"
    elif oran >= 1.5:
        return f"📊 Yüksek ({oran}x)"
    return f"Normal ({oran}x)"

# ── Grafik çizici ─────────────────────────────────────────────────────────────
def grafik_ciz(ad, h):
    try:
        ticker = ad + ".IS"
        df = yf.download(ticker, period="3mo", interval="1d", progress=False, auto_adjust=True)
        if df is None or len(df) < 10:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        close = df["Close"].astype(float)
        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6),
                                        gridspec_kw={"height_ratios": [3, 1]},
                                        facecolor="#0a0a0f")
        for ax in (ax1, ax2):
            ax.set_facecolor("#111118")
            ax.tick_params(colors="#888", labelsize=8)
            for spine in ax.spines.values():
                spine.set_edgecolor("#2a2a3a")

        ax1.plot(close.index, close.values, color="#e0e0e0", linewidth=1.5, label="Fiyat")
        ax1.plot(ema20.index, ema20.values, color="#2962ff", linewidth=1, linestyle="--", label="EMA20")
        ax1.plot(ema50.index, ema50.values, color="#f59e0b", linewidth=1, linestyle="--", label="EMA50")
        ax1.set_title(f"{ad}  |  {h.get('kapanis', '—')} TL  |  RSI: {h.get('rsi', '—')}",
                      color="#fff", fontsize=12, pad=8)
        ax1.legend(loc="upper left", fontsize=7, facecolor="#1a1a24", labelcolor="#ccc", framealpha=0.8)
        ax1.set_ylabel("Fiyat (TL)", color="#888", fontsize=8)

        ax2.bar(df.index, df["Volume"].astype(float), color="#2962ff", alpha=0.6, width=0.8)
        ax2.set_ylabel("Hacim", color="#888", fontsize=8)

        sinyaller = h.get("sinyaller", [])[:5]
        if sinyaller:
            ax1.annotate(
                "📊 " + " · ".join(sinyaller),
                xy=(0.01, 0.05), xycoords="axes fraction",
                fontsize=7, color="#f59e0b",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#1a1200", edgecolor="#3a2800", alpha=0.9)
            )

        plt.tight_layout(pad=1.5)
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=110, bbox_inches="tight", facecolor="#0a0a0f")
        plt.close(fig)
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Grafik hatası {ad}: {e}")
        return None

# ── Ana menü ──────────────────────────────────────────────────────────────────
async def ana_menu_gonder(message, user_id, isim, data):
    veri  = veri_yukle()
    tarih = veri["tarih"] if veri else "—"
    altin = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Altin"] if veri else []
    gumus = [k for k, v in veri["hisseler"].items() if v.get("altin") == "Gumus"] if veri else []
    ozel  = [k for k, v in veri["hisseler"].items() if v.get("ozel_tarama")]       if veri else []

    sayi       = davet_sayisi(user_id, data)
    altin_acik = altin_erisim_var_mi(user_id, data)
    ozel_acik  = ozel_erisim_var_mi(user_id, data)

    # Terminal URL'ye erişim parametreleri
    ozel_param  = "1" if ozel_acik  else "0"
    altin_param = "1" if altin_acik else "0"
    terminal_url = f"{WEBAPP_URL}?ozel={ozel_param}&altin={altin_param}"

    if ozel_acik:
        durum = f"🔓 *{sayi}* davet — tüm özellikler açık 🏆"
    elif altin_acik:
        durum = f"🔓 *{sayi}* davet — altın grafikleri açık ({DAVET_ESIK_OZEL - sayi} davet daha → tavan tarama)"
    else:
        durum = f"🔒 *{sayi}/{DAVET_ESIK_ALTIN}* davet — özellikler kilitli"

    keyboard = [
        [InlineKeyboardButton("📊 Terminali Aç", web_app=WebAppInfo(url=terminal_url))],
        [InlineKeyboardButton(
            "🏆 Tavan Tarama Grafikleri" + (" 🔒" if not ozel_acik else ""),
            callback_data="tavan_grafik"
        )],
        [InlineKeyboardButton(
            "🥇 Altın Grafikleri" + (" 🔒" if not altin_acik else ""),
            callback_data="altin_grafik"
        )],
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
        f"🥇 Altın: *{len(altin)}* · 🥈 Gümüş: *{len(gumus)}* · 🏆 Özel: *{len(ozel)}*\n\n"
        f"{durum}\n\n"
        f"💡 `/hisse THYAO` → anlık analiz\n"
        f"⭐ `/favori THYAO` → favoriye ekle\n\n"
        f"_Bu platform yatırım tavsiyesi vermez. Risk içerir._",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ── /start ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = str(user.id)
    isim    = user.first_name
    data    = davet_yukle()

    # Davet linki işle
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
                    acildimi = ""
                    if yeni_sayi == DAVET_ESIK_ALTIN:
                        acildimi = " — 🥇 Altın grafikleri açıldı!"
                    elif yeni_sayi == DAVET_ESIK_OZEL:
                        acildimi = " — 🏆 Tavan Tarama Grafikleri açıldı!"
                    await context.bot.send_message(
                        chat_id=int(davet_eden_id),
                        text=f"🎉 Yeni davet! *{isim}* bota katıldı.\n"
                             f"Toplam davetiniz: *{yeni_sayi}*{acildimi}",
                        parse_mode="Markdown"
                    )
                except:
                    pass

    # Kanal üyelik kontrolü
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

# ── /hisse ────────────────────────────────────────────────────────────────────
async def hisse_komut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📊 *Hisse Sorgula*\n\nKullanım: `/hisse THYAO`",
            parse_mode="Markdown"
        )
        return
    ad   = context.args[0].upper().strip()
    veri = veri_yukle()
    if not veri or ad not in veri.get("hisseler", {}):
        await update.message.reply_text(f"❌ *{ad}* bulunamadı.", parse_mode="Markdown")
        return
    h         = veri["hisseler"][ad]
    seviye    = {"Altin": "🥇 Altın", "Gumus": "🥈 Gümüş", "Bronz": "🥉 Bronz"}.get(h.get("altin"), "—")
    sinyaller = "\n".join(f"• {s}" for s in h.get("sinyaller", [])) or "Aktif sinyal yok"
    keyboard  = [[
        InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
        InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
    ]]
    await update.message.reply_text(
        f"📊 *{ad}* — {h.get('kapanis','—')} TL\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏅 Seviye: {seviye}\n"
        f"📈 RSI: `{h.get('rsi','—')}`\n"
        f"⚡ MACD: {macd_yorum(h)}\n"
        f"🔥 Hacim: {hacim_yorum(h)}\n\n"
        f"*Sinyaller:*\n{sinyaller}\n\n"
        f"📅 {veri.get('tarih','—')}\n"
        f"_Yatırım tavsiyesi değildir._",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ── /favori ───────────────────────────────────────────────────────────────────
async def favori_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Argümansız → liste göster
    if not context.args:
        fav_data  = favori_yukle()
        favoriler = fav_data.get(user_id, [])
        if not favoriler:
            await update.message.reply_text(
                "⭐ *Favorilerin boş!*\n\n`/favori THYAO` ile ekle · `/favorisil THYAO` ile sil",
                parse_mode="Markdown"
            )
            return
        veri  = veri_yukle()
        mesaj = f"⭐ *Favorilerin* ({len(favoriler)} hisse)\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for ad in favoriler:
            if veri and ad in veri["hisseler"]:
                h      = veri["hisseler"][ad]
                seviye = {"Altin":"🥇","Gumus":"🥈","Bronz":"🥉"}.get(h.get("altin"),"—")
                mesaj += f"{seviye} *{ad}* — {h['kapanis']} TL | RSI:`{h.get('rsi','—')}` | {hacim_yorum(h)}\n"
            else:
                mesaj += f"• *{ad}*\n"
        mesaj += "\n_Yatırım tavsiyesi değildir._"
        await update.message.reply_text(mesaj, parse_mode="Markdown")
        return

    ad   = context.args[0].upper().strip()
    veri = veri_yukle()
    if not veri or ad not in veri["hisseler"]:
        await update.message.reply_text(f"❌ *{ad}* bulunamadı.", parse_mode="Markdown")
        return
    fav_data  = favori_yukle()
    favoriler = fav_data.get(user_id, [])
    if ad in favoriler:
        await update.message.reply_text(f"ℹ️ *{ad}* zaten favorilerinde.", parse_mode="Markdown")
        return
    favoriler.append(ad)
    fav_data[user_id] = favoriler
    favori_kaydet(fav_data)
    await update.message.reply_text(f"⭐ *{ad}* favorilerine eklendi!", parse_mode="Markdown")

async def favori_sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Kullanım: `/favorisil THYAO`", parse_mode="Markdown")
        return
    ad        = context.args[0].upper().strip()
    fav_data  = favori_yukle()
    favoriler = fav_data.get(user_id, [])
    if ad not in favoriler:
        await update.message.reply_text(f"❌ *{ad}* favorilerinde yok.", parse_mode="Markdown")
        return
    favoriler.remove(ad)
    fav_data[user_id] = favoriler
    favori_kaydet(fav_data)
    await update.message.reply_text(f"🗑️ *{ad}* favorilerinden silindi.", parse_mode="Markdown")

# ── Buton işleyici ────────────────────────────────────────────────────────────
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
            await query.answer("❌ Henüz kanala katılmadın! Önce kanala katıl.", show_alert=True)
        return

    uye = await kanal_uye_mi(context, int(user_id))
    if not uye:
        keyboard = [
            [InlineKeyboardButton("📢 Kanala Katıl", url=KANAL_LINK)],
            [InlineKeyboardButton("✅ Katıldım, Devam Et", callback_data="kanal_kontrol")],
        ]
        await query.message.reply_text(
            "⚠️ Kanaldan ayrılmışsın!\n\nBotu kullanmaya devam etmek için kanala katılman gerekiyor.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if query.data == "yasal_uyari":
        await query.message.reply_text(YASAL_UYARI, parse_mode="Markdown")

    elif query.data == "davet_link":
        sayi      = davet_sayisi(user_id, data)
        davet_url = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        await query.message.reply_text(
            f"👥 *Davet Linkin*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Aşağıdaki linki arkadaşlarınla paylaş:\n\n"
            f"`{davet_url}`\n\n"
            f"📊 Davet durumun: *{sayi}* kişi\n\n"
            f"🔓 *{DAVET_ESIK_ALTIN} davet* → Altın hisse grafikleri\n"
            f"🏆 *{DAVET_ESIK_OZEL} davet* → Tavan Tarama Grafikleri + Özel Terminal\n\n"
            f"_Linki kopyalayıp Telegram'da paylaşabilirsin._",
            parse_mode="Markdown"
        )

    elif query.data == "favorilerim":
        fav_data  = favori_yukle()
        favoriler = fav_data.get(user_id, [])
        if not favoriler:
            await query.message.reply_text(
                "⭐ *Favorilerin boş!*\n\n`/favori THYAO` yazarak ekleyebilirsin.",
                parse_mode="Markdown"
            )
            return
        veri  = veri_yukle()
        mesaj = f"⭐ *Favorilerin* ({len(favoriler)} hisse)\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for ad in favoriler:
            if veri and ad in veri["hisseler"]:
                h      = veri["hisseler"][ad]
                seviye = {"Altin":"🥇","Gumus":"🥈","Bronz":"🥉"}.get(h.get("altin"),"—")
                mesaj += (
                    f"{seviye} *{ad}* — {h['kapanis']} TL\n"
                    f"   RSI:`{h.get('rsi','—')}` | MACD:{macd_yorum(h)} | {hacim_yorum(h)}\n\n"
                )
            else:
                mesaj += f"• *{ad}*\n"
        mesaj += "_Yatırım tavsiyesi değildir._"
        await query.message.reply_text(mesaj, parse_mode="Markdown")

    # ── Altın Grafikleri (5 davet) ────────────────────────────────────────────
    elif query.data == "altin_grafik":
        if not altin_erisim_var_mi(user_id, data):
            sayi      = davet_sayisi(user_id, data)
            davet_url = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Bu özellik kilitli!*\n\n"
                f"Altın hisse grafiklerini görmek için *{DAVET_ESIK_ALTIN} kişi davet* etmen gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/{DAVET_ESIK_ALTIN}*\n\n"
                f"Davet linkin:\n`{davet_url}`",
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
            f"🥇 *{len(altin_hisseler)} Altın Sinyal* — Grafikler hazırlanıyor...\n"
            f"_Yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )
        for ad in altin_hisseler[:8]:
            h   = veri["hisseler"][ad]
            buf = grafik_ciz(ad, h)
            sinyaller_str = " · ".join(h.get("sinyaller", [])[:4])
            caption = (
                f"🥇 *{ad}* — {h.get('kapanis','—')} TL\n"
                f"RSI:`{h.get('rsi','—')}` | MACD:{macd_yorum(h)} | {hacim_yorum(h)}\n"
                f"📊 {sinyaller_str}\n"
                f"_Yatırım tavsiyesi değildir._"
            )
            keyboard = [[
                InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
                InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
            ]]
            if buf:
                await query.message.reply_photo(photo=buf, caption=caption, parse_mode="Markdown",
                                                reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text(caption, parse_mode="Markdown",
                                               reply_markup=InlineKeyboardMarkup(keyboard))

    # ── Tavan Tarama Grafikleri (10 davet) ────────────────────────────────────
    elif query.data == "tavan_grafik":
        if not ozel_erisim_var_mi(user_id, data):
            sayi      = davet_sayisi(user_id, data)
            davet_url = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            await query.message.reply_text(
                f"🔒 *Bu özellik kilitli!*\n\n"
                f"Tavan Tarama Grafiklerini görmek için *{DAVET_ESIK_OZEL} kişi davet* etmen gerekiyor.\n\n"
                f"Davet durumun: *{sayi}/{DAVET_ESIK_OZEL}*\n\n"
                f"Davet linkin:\n`{davet_url}`",
                parse_mode="Markdown"
            )
            return

        veri = veri_yukle()
        if not veri:
            await query.message.reply_text("Veri bulunamadı.")
            return

        ozel_hisseler = [k for k, v in veri["hisseler"].items() if v.get("ozel_tarama")]
        if not ozel_hisseler:
            await query.message.reply_text("Bugün özel tarama sinyali veren hisse bulunamadı.")
            return

        await query.message.reply_text(
            f"🏆 *{len(ozel_hisseler)} Tavan Tarama Sinyali* — Grafikler hazırlanıyor...\n"
            f"_Yatırım tavsiyesi değildir._",
            parse_mode="Markdown"
        )
        for ad in ozel_hisseler[:8]:
            h   = veri["hisseler"][ad]
            buf = grafik_ciz(ad, h)
            sinyaller_str = " · ".join(h.get("sinyaller", [])[:4])
            caption = (
                f"🏆 *{ad}* — {h.get('kapanis','—')} TL\n"
                f"RSI:`{h.get('rsi','—')}` | MACD:{macd_yorum(h)} | {hacim_yorum(h)}\n"
                f"📊 {sinyaller_str}\n"
                f"_Yatırım tavsiyesi değildir._"
            )
            keyboard = [[
                InlineKeyboardButton("📈 TradingView", url=f"https://tr.tradingview.com/chart/?symbol=BIST:{ad}"),
                InlineKeyboardButton("📰 KAP", url=f"https://www.kap.org.tr/tr/bildirim-sorgu?subjectTypes=FR,DR,IA&companies={ad}")
            ]]
            if buf:
                await query.message.reply_photo(photo=buf, caption=caption, parse_mode="Markdown",
                                                reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text(caption, parse_mode="Markdown",
                                               reply_markup=InlineKeyboardMarkup(keyboard))

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("hisse",     hisse_komut))
    app.add_handler(CommandHandler("favori",    favori_ekle))
    app.add_handler(CommandHandler("favorisil", favori_sil))
    app.add_handler(CallbackQueryHandler(buton))
    print("✅ Bot çalışıyor...")
    app.run_polling()
