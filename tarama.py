import yfinance as yf
import ta
import time
import json
from datetime import datetime

hisseler = ["A1CAP.IS","A1YEN.IS","ACSEL.IS","ADEL.IS","ADESE.IS","ADGYO.IS","AFYON.IS","AGESA.IS","AGHOL.IS","AGROT.IS","AHGAZ.IS","AHSGY.IS","AKCNS.IS","AKENR.IS","AKFGY.IS","AKFIS.IS","AKFYE.IS","AKGRT.IS","AKSA.IS","AKSEN.IS","AKSGY.IS","AKSUE.IS","AKYHO.IS","ALARK.IS","ALCAR.IS","ALCTL.IS","ALFAS.IS","ALGYO.IS","ALKA.IS","ALKIM.IS","ALKLC.IS","ALTNY.IS","ALVES.IS","ANELE.IS","ANGEN.IS","ANHYT.IS","ANSGR.IS","ARASE.IS","ARCLK.IS","ARDYZ.IS","ARENA.IS","ARFYE.IS","ARMGD.IS","ARSAN.IS","ARTMS.IS","ARZUM.IS","ASELS.IS","ASGYO.IS","ASTOR.IS","ASUZU.IS","ATAKP.IS","ATATP.IS","ATATR.IS","AVGYO.IS","AVHOL.IS","AVOD.IS","AVPGY.IS","AYCES.IS","AYDEM.IS","AYEN.IS","AYGAZ.IS","AZTEK.IS","BAGFS.IS","BAHKM.IS","BAKAB.IS","BALAT.IS","BALSU.IS","BANVT.IS","BARMA.IS","BASCM.IS","BASGZ.IS","BAYRK.IS","BEGYO.IS","BERA.IS","BESLR.IS","BEYAZ.IS","BFREN.IS","BIENY.IS","BIGCH.IS","BIGEN.IS","BIMAS.IS","BINBN.IS","BINHO.IS","BIOEN.IS","BIZIM.IS","BLCYT.IS","BLUME.IS","BMSCH.IS","BMSTL.IS","BNTAS.IS","BOBET.IS","BORLS.IS","BORSK.IS","BOSSA.IS","BRISA.IS","BRKSN.IS","BRKVY.IS","BRLSM.IS","BRSAN.IS","BRYAT.IS","BSOKE.IS","BTCIM.IS","BUCIM.IS","BULGS.IS","BURCE.IS","BURVA.IS","BVSAN.IS","BYDNR.IS","CANTE.IS","CATES.IS","CCOLA.IS","CELHA.IS","CEMAS.IS","CEMTS.IS","CEMZY.IS","CEOEM.IS","CGCAM.IS","CIMSA.IS","CLEBI.IS","CMBTN.IS","CONSE.IS","COSMO.IS","CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAGI.IS","DAPGM.IS","DARDL.IS","DCTTR.IS","DENGE.IS","DERHL.IS","DERIM.IS","DESA.IS","DESPC.IS","DEVA.IS","DGATE.IS","DGNMO.IS","DITAS.IS","DMRGD.IS","DMSAS.IS","DNISI.IS","DOAS.IS","DOCO.IS","DOFER.IS","DOFRB.IS","DOGUB.IS","DOHOL.IS","DOKTA.IS","DSTKF.IS","DURDO.IS","DURKN.IS","DYOBY.IS","DZGYO.IS","EBEBK.IS","ECILC.IS","ECZYT.IS","EDATA.IS","EDIP.IS","EGEEN.IS","EGEGY.IS","EGEPO.IS","EGGUB.IS","EGPRO.IS","EGSER.IS","EKGYO.IS","EKOS.IS","EKSUN.IS","ELITE.IS","EMKEL.IS","ENDAE.IS","ENERY.IS","ENJSA.IS","ENKAI.IS","ENSRI.IS","ENTRA.IS","EPLAS.IS","ERBOS.IS","ERCB.IS","EREGL.IS","ERSU.IS","ESCAR.IS","ESCOM.IS","ESEN.IS","ETILR.IS","EUPWR.IS","EUREN.IS","EYGYO.IS","FADE.IS","FLAP.IS","FMIZP.IS","FONET.IS","FORMT.IS","FORTE.IS","FRIGO.IS","FROTO.IS","FZLGY.IS","GEDIK.IS","GEDZA.IS","GENIL.IS","GENTS.IS","GEREL.IS","GESAN.IS","GIPTA.IS","GLCVY.IS","GLRMK.IS","GLRYH.IS","GLYHO.IS","GMTAS.IS","GOKNR.IS","GOLTS.IS","GOODY.IS","GOZDE.IS","GRSEL.IS","GRTHO.IS","GSDDE.IS","GSDHO.IS","GSRAY.IS","GUBRF.IS","GUNDG.IS","GWIND.IS","GZNMI.IS","HATEK.IS","HATSN.IS","HDFGS.IS","HEDEF.IS","HEKTS.IS","HKTM.IS","HOROZ.IS","HRKET.IS","HTTBT.IS","HUBVC.IS","HUNER.IS","HURGZ.IS","ICUGS.IS","IEYHO.IS","IHAAS.IS","IHEVA.IS","IHGZT.IS","IHLAS.IS","IHLGM.IS","IHYAY.IS","IMASM.IS","INDES.IS","INFO.IS","INGRM.IS","INTEM.IS","INVEO.IS","INVES.IS","ISDMR.IS","ISKPL.IS","ISSEN.IS","IZENR.IS","IZFAS.IS","IZINV.IS","IZMDC.IS","JANTS.IS","KAPLM.IS","KAREL.IS","KARSN.IS","KARTN.IS","KATMR.IS","KAYSE.IS","KBORU.IS","KCAER.IS","KCHOL.IS","KFEIN.IS","KGYO.IS","KIMMR.IS","KLGYO.IS","KLKIM.IS","KLMSN.IS","KLRHO.IS","KLSER.IS","KLSYN.IS","KLYPV.IS","KMPUR.IS","KNFRT.IS","KOCMT.IS","KONKA.IS","KONTR.IS","KONYA.IS","KOPOL.IS","KORDS.IS","KOTON.IS","KRDMD.IS","KRGYO.IS","KRONT.IS","KRPLS.IS","KRSTL.IS","KRTEK.IS","KRVGD.IS","KTLEV.IS","KTSKR.IS","KUTPO.IS","KUYAS.IS","KZBGY.IS","KZGYO.IS","LIDER.IS","LILAK.IS","LINK.IS","LKMNH.IS","LMKDC.IS","LOGO.IS","LRSHO.IS","LUKSK.IS","LYDHO.IS","MAALT.IS","MACKO.IS","MAGEN.IS","MAKIM.IS","MAKTK.IS","MANAS.IS","MARBL.IS","MARMR.IS","MARTI.IS","MAVI.IS","MEDTR.IS","MEGMT.IS","MEKAG.IS","MERCN.IS","MERIT.IS","MERKO.IS","METRO.IS","MEYSU.IS","MGROS.IS","MHRGY.IS","MIATK.IS","MNDRS.IS","MNDTR.IS","MOBTL.IS","MOGAN.IS","MOPAS.IS","MPARK.IS","MRGYO.IS","MRSHL.IS","MSGYO.IS","MTRKS.IS","MTRYO.IS","NATEN.IS","NETAS.IS","NIBAS.IS","NTGAZ.IS","NTHOL.IS","NUGYO.IS","NUHCM.IS","OBAMS.IS","OBASE.IS","ODAS.IS","ODINE.IS","OFSYM.IS","ONCSM.IS","ONRYT.IS","ORCAY.IS","ORGE.IS","OSMEN.IS","OSTIM.IS","OTKAR.IS","OYAKC.IS","OYLUM.IS","OYYAT.IS","OZATD.IS","OZGYO.IS","OZKGY.IS","OZRDN.IS","OZSUB.IS","OZYSR.IS","PAGYO.IS","PAHOL.IS","PAMEL.IS","PAPIL.IS","PARSN.IS","PASEU.IS","PATEK.IS","PCILT.IS","PEKGY.IS","PENGD.IS","PENTA.IS","PETKM.IS","PETUN.IS","PGSUS.IS","PINSU.IS","PKART.IS","PKENT.IS","PLTUR.IS","PNLSN.IS","PNSUT.IS","POLHO.IS","POLTK.IS","PRDGS.IS","PRKAB.IS","PRKME.IS","PRZMA.IS","PSDTC.IS","PSGYO.IS","QUAGR.IS","RALYH.IS","RAYSG.IS","REEDR.IS","RGYAS.IS","RTALB.IS","RUBNS.IS","RUZYE.IS","RYGYO.IS","RYSAS.IS","SAFKR.IS","SAHOL.IS","SAMAT.IS","SANEL.IS","SANFM.IS","SANKO.IS","SARKY.IS","SASA.IS","SAYAS.IS","SDTTR.IS","SEGMN.IS","SEKUR.IS","SELEC.IS","SELVA.IS","SERNT.IS","SEYKM.IS","SILVR.IS","SISE.IS","SKTAS.IS","SKYLP.IS","SMART.IS","SMRTG.IS","SMRVA.IS","SNGYO.IS","SNICA.IS","SOKE.IS","SOKM.IS","SRVGY.IS","SUNTK.IS","SURGY.IS","SUWEN.IS","TABGD.IS","TARKM.IS","TATEN.IS","TATGD.IS","TAVHL.IS","TCELL.IS","TCKRC.IS","TEHOL.IS","TEKTU.IS","TERA.IS","TEZOL.IS","THYAO.IS","TKFEN.IS","TKNSA.IS","TLMAN.IS","TMPOL.IS","TMSN.IS","TNZTP.IS","TOASO.IS","TRCAS.IS","TRGYO.IS","TRHOL.IS","TRILC.IS","TSGYO.IS","TSPOR.IS","TTKOM.IS","TTRAK.IS","TUCLK.IS","TUKAS.IS","TUPRS.IS","TUREX.IS","TURGG.IS","TURSG.IS","ULAS.IS","ULKER.IS","ULUSE.IS","ULUUN.IS","UNLU.IS","USAK.IS","VAKKO.IS","VBTYZ.IS","VERTU.IS","VERUS.IS","VESBE.IS","VESTL.IS","VRGYO.IS","VSNMD.IS","YAPRK.IS","YATAS.IS","YBTAS.IS","YEOTK.IS","YESIL.IS","YGGYO.IS","YIGIT.IS","YKSLN.IS","YUNSA.IS","YYAPI.IS","YYLGD.IS","ZEDUR.IS","ZERGY.IS","ZGYO.IS"]

# ── BOĞA FORMASYON FONKSİYONLARI ─────────────────────────

def yutan_boga(v):
    s, o = v.iloc[-1], v.iloc[-2]
    return (o["Close"] < o["Open"] and s["Close"] > s["Open"]
            and s["Open"] < o["Close"] and s["Close"] > o["Open"])

def cekic(v):
    s = v.iloc[-1]
    govde = abs(s["Close"] - s["Open"])
    alt_fitil = min(s["Close"], s["Open"]) - s["Low"]
    ust_fitil = s["High"] - max(s["Close"], s["Open"])
    return govde > 0 and alt_fitil >= 2 * govde and ust_fitil <= govde * 0.3

def ters_cekic(v):
    s = v.iloc[-1]
    govde = abs(s["Close"] - s["Open"])
    ust_fitil = s["High"] - max(s["Close"], s["Open"])
    alt_fitil = min(s["Close"], s["Open"]) - s["Low"]
    return govde > 0 and ust_fitil >= 2 * govde and alt_fitil <= govde * 0.3

def sabah_yildizi(v):
    if len(v) < 3: return False
    a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
    return (a["Open"] > a["Close"] and
            abs(b["Close"] - b["Open"]) <= abs(a["Close"] - a["Open"]) * 0.3 and
            c["Close"] > c["Open"] and
            c["Close"] > (a["Open"] + a["Close"]) / 2)

def boga_harami(v):
    s, o = v.iloc[-1], v.iloc[-2]
    return (o["Close"] < o["Open"] and s["Close"] > s["Open"]
            and s["Open"] > o["Close"] and s["Close"] < o["Open"]
            and abs(s["Close"] - s["Open"]) < abs(o["Close"] - o["Open"]))

def uc_beyaz_asker(v):
    if len(v) < 3: return False
    a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
    return (a["Close"] > a["Open"] and b["Close"] > b["Open"] and c["Close"] > c["Open"]
            and b["Close"] > a["Close"] and c["Close"] > b["Close"]
            and b["Open"] > a["Open"] and c["Open"] > b["Open"])

def delikli_bulut(v):
    s, o = v.iloc[-1], v.iloc[-2]
    orta = (o["Open"] + o["Close"]) / 2
    return (o["Close"] < o["Open"] and s["Close"] > s["Open"]
            and s["Open"] < o["Close"] and s["Close"] > orta
            and s["Close"] < o["Open"])

# ── AYI FORMASYON FONKSİYONLARI ──────────────────────────

def yutan_ayi(v):
    s, o = v.iloc[-1], v.iloc[-2]
    return (o["Close"] > o["Open"] and s["Close"] < s["Open"]
            and s["Open"] > o["Close"] and s["Close"] < o["Open"])

def asilan_adam(v):
    s = v.iloc[-1]
    govde = abs(s["Close"] - s["Open"])
    alt_fitil = min(s["Close"], s["Open"]) - s["Low"]
    ust_fitil = s["High"] - max(s["Close"], s["Open"])
    return govde > 0 and alt_fitil >= 2 * govde and ust_fitil <= govde * 0.3

def aksam_yildizi(v):
    if len(v) < 3: return False
    a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
    return (a["Close"] > a["Open"] and
            abs(b["Close"] - b["Open"]) <= abs(a["Close"] - a["Open"]) * 0.3 and
            c["Close"] < c["Open"] and
            c["Close"] < (a["Open"] + a["Close"]) / 2)

def ayi_harami(v):
    s, o = v.iloc[-1], v.iloc[-2]
    return (o["Close"] > o["Open"] and s["Close"] < s["Open"]
            and s["Open"] < o["Close"] and s["Close"] > o["Open"]
            and abs(s["Close"] - s["Open"]) < abs(o["Close"] - o["Open"]))

def uc_siyah_karga(v):
    if len(v) < 3: return False
    a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
    return (a["Close"] < a["Open"] and b["Close"] < b["Open"] and c["Close"] < c["Open"]
            and b["Close"] < a["Close"] and c["Close"] < b["Close"]
            and b["Open"] < a["Open"] and c["Open"] < b["Open"])

def kara_bulut_ortusu(v):
    s, o = v.iloc[-1], v.iloc[-2]
    orta = (o["Open"] + o["Close"]) / 2
    return (o["Close"] > o["Open"] and s["Close"] < s["Open"]
            and s["Open"] > o["Close"] and s["Close"] < orta
            and s["Close"] > o["Open"])

# ── ANA TARAMA ───────────────────────────────────────────

sonuclar = {}
gruplar = [hisseler[i:i+100] for i in range(0, len(hisseler), 100)]

for g, grup in enumerate(gruplar):
    print(f"Grup {g+1}/5 taranıyor...")
    for hisse in grup:
        try:
            v = yf.Ticker(hisse).history(period="3mo")
            if len(v) < 52:
                continue

            ad = hisse.replace(".IS", "")
            kapanis = round(float(v["Close"].iloc[-1]), 2)

            # Göstergeler
            rsi_seri = ta.momentum.RSIIndicator(v["Close"], window=14).rsi()
            rsi = round(float(rsi_seri.iloc[-1]), 2)

            macd_obj = ta.trend.MACD(v["Close"])
            macd_val = float(macd_obj.macd().iloc[-1])
            macd_sig = float(macd_obj.macd_signal().iloc[-1])
            macd_hist_onceki = float(macd_obj.macd_diff().iloc[-2])
            macd_hist_son = float(macd_obj.macd_diff().iloc[-1])

            bb = ta.volatility.BollingerBands(v["Close"], window=20)
            bb_alt = float(bb.bollinger_lband().iloc[-1])
            bb_ust = float(bb.bollinger_hband().iloc[-1])

            ema20_seri = v["Close"].ewm(span=20).mean()
            ema50_seri = v["Close"].ewm(span=50).mean()
            ema20 = float(ema20_seri.iloc[-1])
            ema50 = float(ema50_seri.iloc[-1])
            ema20_onceki = float(ema20_seri.iloc[-2])
            ema50_onceki = float(ema50_seri.iloc[-2])

            hacim_ort = float(v["Volume"].iloc[-51:-1].mean())
            hacim_son = float(v["Volume"].iloc[-1])
            hacim_orani = round(hacim_son / hacim_ort, 2) if hacim_ort > 0 else 0

            # Sinyaller
            sinyaller = []

            # RSI
            if rsi < 30: sinyaller.append("RSI Aşırı Satım")
            if rsi > 70: sinyaller.append("RSI Aşırı Alım")

            # MACD
            if macd_hist_onceki < 0 and macd_hist_son > 0: sinyaller.append("MACD Al Kesişimi")
            if macd_hist_onceki > 0 and macd_hist_son < 0: sinyaller.append("MACD Sat Kesişimi")
            if macd_val > macd_sig: sinyaller.append("MACD Pozitif")
            if macd_val < macd_sig: sinyaller.append("MACD Negatif")

            # Bollinger
            if kapanis <= bb_alt * 1.01: sinyaller.append("BB Alt Bant")
            if kapanis >= bb_ust * 0.99: sinyaller.append("BB Üst Bant")

            # EMA
            if kapanis > ema20: sinyaller.append("Fiyat EMA20 Üstünde")
            if kapanis < ema20: sinyaller.append("Fiyat EMA20 Altında")
            if ema20 > ema50: sinyaller.append("EMA20 > EMA50")
            if ema20 < ema50: sinyaller.append("EMA20 < EMA50")
            if ema20_onceki < ema50_onceki and ema20 > ema50: sinyaller.append("Golden Cross")
            if ema20_onceki > ema50_onceki and ema20 < ema50: sinyaller.append("Death Cross")

            # Hacim
            if hacim_orani >= 3: sinyaller.append(f"Anormal Hacim {hacim_orani}x")

            # Boğa Formasyonları
            if yutan_boga(v):     sinyaller.append("Yutan Boğa")
            if cekic(v):          sinyaller.append("Çekiç")
            if ters_cekic(v):     sinyaller.append("Ters Çekiç")
            if sabah_yildizi(v):  sinyaller.append("Sabah Yıldızı")
            if boga_harami(v):    sinyaller.append("Boğa Harami")
            if uc_beyaz_asker(v): sinyaller.append("3 Beyaz Asker")
            if delikli_bulut(v):  sinyaller.append("Delikli Bulut")

            # Ayı Formasyonları
            if yutan_ayi(v):        sinyaller.append("Yutan Ayı")
            if asilan_adam(v):      sinyaller.append("Asılan Adam")
            if aksam_yildizi(v):    sinyaller.append("Akşam Yıldızı")
            if ayi_harami(v):       sinyaller.append("Ayı Harami")
            if uc_siyah_karga(v):   sinyaller.append("3 Siyah Karga")
            if kara_bulut_ortusu(v):sinyaller.append("Kara Bulut Örtüsü")

            # Altın Tarama — sadece boğa sinyallerine bak
            boga_sinyaller = [s for s in sinyaller if s not in [
                "MACD Sat Kesişimi", "MACD Negatif", "Fiyat EMA20 Altında",
                "EMA20 < EMA50", "Death Cross", "Yutan Ayı", "Asılan Adam",
                "Akşam Yıldızı", "Ayı Harami", "3 Siyah Karga", "Kara Bulut Örtüsü",
                "RSI Aşırı Alım"
            ]]
            altin_skor = len(boga_sinyaller)

            altin_skor = len(sinyaller)
            if altin_skor >= 7: altin = "🥇 Altın"
            elif altin_skor >= 5: altin = "🥈 Gümüş"
            elif altin_skor >= 3: altin = "🥉 Bronz"
            else: altin = None

            if sinyaller:
                sonuclar[ad] = {
                    "kapanis": kapanis,
                    "rsi": rsi,
                    "macd_pozitif": macd_val > macd_sig,
                    "golden_cross": ema20_onceki < ema50_onceki and ema20 > ema50,
                    "death_cross": ema20_onceki > ema50_onceki and ema20 < ema50,
                    "bb_alt_bant": kapanis <= bb_alt * 1.01,
                    "hacim_orani": hacim_orani,
                    "sinyaller": sinyaller,
                    "sinyal_sayisi": altin_skor,
                    "altin": altin
                }

        except Exception as e:
            pass
    time.sleep(3)

# Kaydet
with open("C:/bist_terminal/sonuclar.json", "w", encoding="utf-8") as f:
    json.dump({
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "hisseler": sonuclar
    }, f, ensure_ascii=False, indent=2)

# Özet
altin_liste = [(k, v) for k, v in sonuclar.items() if v["altin"] == "🥇 Altın"]
gumus_liste = [(k, v) for k, v in sonuclar.items() if v["altin"] == "🥈 Gümüş"]
bronz_liste = [(k, v) for k, v in sonuclar.items() if v["altin"] == "🥉 Bronz"]

print(f"\n✅ TARAMA TAMAMLANDI — {datetime.now().strftime('%d.%m.%Y %H:%M')}")
print(f"📊 Toplam sinyal veren: {len(sonuclar)} hisse")
print(f"🥇 Altın: {len(altin_liste)} | 🥈 Gümüş: {len(gumus_liste)} | 🥉 Bronz: {len(bronz_liste)}")
print("\n💾 Sonuçlar kaydedildi!")