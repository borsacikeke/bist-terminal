import yfinance as yf
import ta
import time
import json
import schedule
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from datetime import datetime

hisseler = ["A1CAP.IS","A1YEN.IS","ACSEL.IS","ADEL.IS","ADESE.IS","ADGYO.IS","AFYON.IS","AGESA.IS","AGHOL.IS","AGROT.IS","AHGAZ.IS","AHSGY.IS","AKCNS.IS","AKENR.IS","AKFGY.IS","AKFIS.IS","AKFYE.IS","AKGRT.IS","AKSA.IS","AKSEN.IS","AKSGY.IS","AKSUE.IS","AKYHO.IS","ALARK.IS","ALCAR.IS","ALCTL.IS","ALFAS.IS","ALGYO.IS","ALKA.IS","ALKIM.IS","ALKLC.IS","ALTNY.IS","ALVES.IS","ANELE.IS","ANGEN.IS","ANHYT.IS","ANSGR.IS","ARASE.IS","ARCLK.IS","ARDYZ.IS","ARENA.IS","ARFYE.IS","ARMGD.IS","ARSAN.IS","ARTMS.IS","ARZUM.IS","ASELS.IS","ASGYO.IS","ASTOR.IS","ASUZU.IS","ATAKP.IS","ATATP.IS","ATATR.IS","AVGYO.IS","AVHOL.IS","AVOD.IS","AVPGY.IS","AYCES.IS","AYDEM.IS","AYEN.IS","AYGAZ.IS","AZTEK.IS","BAGFS.IS","BAHKM.IS","BAKAB.IS","BALAT.IS","BALSU.IS","BANVT.IS","BARMA.IS","BASCM.IS","BASGZ.IS","BAYRK.IS","BEGYO.IS","BERA.IS","BESLR.IS","BEYAZ.IS","BFREN.IS","BIENY.IS","BIGCH.IS","BIGEN.IS","BIMAS.IS","BINBN.IS","BINHO.IS","BIOEN.IS","BIZIM.IS","BLCYT.IS","BLUME.IS","BMSCH.IS","BMSTL.IS","BNTAS.IS","BOBET.IS","BORLS.IS","BORSK.IS","BOSSA.IS","BRISA.IS","BRKSN.IS","BRKVY.IS","BRLSM.IS","BRSAN.IS","BRYAT.IS","BSOKE.IS","BTCIM.IS","BUCIM.IS","BULGS.IS","BURCE.IS","BURVA.IS","BVSAN.IS","BYDNR.IS","CANTE.IS","CATES.IS","CCOLA.IS","CELHA.IS","CEMAS.IS","CEMTS.IS","CEMZY.IS","CEOEM.IS","CGCAM.IS","CIMSA.IS","CLEBI.IS","CMBTN.IS","CONSE.IS","COSMO.IS","CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAGI.IS","DAPGM.IS","DARDL.IS","DCTTR.IS","DENGE.IS","DERHL.IS","DERIM.IS","DESA.IS","DESPC.IS","DEVA.IS","DGATE.IS","DGNMO.IS","DITAS.IS","DMRGD.IS","DMSAS.IS","DNISI.IS","DOAS.IS","DOCO.IS","DOFER.IS","DOFRB.IS","DOGUB.IS","DOHOL.IS","DOKTA.IS","DSTKF.IS","DURDO.IS","DURKN.IS","DYOBY.IS","DZGYO.IS","EBEBK.IS","ECILC.IS","ECZYT.IS","EDATA.IS","EDIP.IS","EGEEN.IS","EGEGY.IS","EGEPO.IS","EGGUB.IS","EGPRO.IS","EGSER.IS","EKGYO.IS","EKOS.IS","EKSUN.IS","ELITE.IS","EMKEL.IS","ENDAE.IS","ENERY.IS","ENJSA.IS","ENKAI.IS","ENSRI.IS","ENTRA.IS","EPLAS.IS","ERBOS.IS","ERCB.IS","EREGL.IS","ERSU.IS","ESCAR.IS","ESCOM.IS","ESEN.IS","ETILR.IS","EUPWR.IS","EUREN.IS","EYGYO.IS","FADE.IS","FLAP.IS","FMIZP.IS","FONET.IS","FORMT.IS","FORTE.IS","FRIGO.IS","FROTO.IS","FZLGY.IS","GEDIK.IS","GEDZA.IS","GENIL.IS","GENTS.IS","GEREL.IS","GESAN.IS","GIPTA.IS","GLCVY.IS","GLRMK.IS","GLRYH.IS","GLYHO.IS","GMTAS.IS","GOKNR.IS","GOLTS.IS","GOODY.IS","GOZDE.IS","GRSEL.IS","GRTHO.IS","GSDDE.IS","GSDHO.IS","GSRAY.IS","GUBRF.IS","GUNDG.IS","GWIND.IS","GZNMI.IS","HATEK.IS","HATSN.IS","HDFGS.IS","HEDEF.IS","HEKTS.IS","HKTM.IS","HOROZ.IS","HRKET.IS","HTTBT.IS","HUBVC.IS","HUNER.IS","HURGZ.IS","ICUGS.IS","IEYHO.IS","IHAAS.IS","IHEVA.IS","IHGZT.IS","IHLAS.IS","IHLGM.IS","IHYAY.IS","IMASM.IS","INDES.IS","INFO.IS","INGRM.IS","INTEM.IS","INVEO.IS","INVES.IS","ISDMR.IS","ISKPL.IS","ISSEN.IS","IZENR.IS","IZFAS.IS","IZINV.IS","IZMDC.IS","JANTS.IS","KAPLM.IS","KAREL.IS","KARSN.IS","KARTN.IS","KATMR.IS","KAYSE.IS","KBORU.IS","KCAER.IS","KCHOL.IS","KFEIN.IS","KGYO.IS","KIMMR.IS","KLGYO.IS","KLKIM.IS","KLMSN.IS","KLRHO.IS","KLSER.IS","KLSYN.IS","KLYPV.IS","KMPUR.IS","KNFRT.IS","KOCMT.IS","KONKA.IS","KONTR.IS","KONYA.IS","KOPOL.IS","KORDS.IS","KOTON.IS","KRDMD.IS","KRGYO.IS","KRONT.IS","KRPLS.IS","KRSTL.IS","KRTEK.IS","KRVGD.IS","KTLEV.IS","KTSKR.IS","KUTPO.IS","KUYAS.IS","KZBGY.IS","KZGYO.IS","LIDER.IS","LILAK.IS","LINK.IS","LKMNH.IS","LMKDC.IS","LOGO.IS","LRSHO.IS","LUKSK.IS","LYDHO.IS","MAALT.IS","MACKO.IS","MAGEN.IS","MAKIM.IS","MAKTK.IS","MANAS.IS","MARBL.IS","MARMR.IS","MARTI.IS","MAVI.IS","MEDTR.IS","MEGMT.IS","MEKAG.IS","MERCN.IS","MERIT.IS","MERKO.IS","METRO.IS","MEYSU.IS","MGROS.IS","MHRGY.IS","MIATK.IS","MNDRS.IS","MNDTR.IS","MOBTL.IS","MOGAN.IS","MOPAS.IS","MPARK.IS","MRGYO.IS","MRSHL.IS","MSGYO.IS","MTRKS.IS","MTRYO.IS","NATEN.IS","NETAS.IS","NIBAS.IS","NTGAZ.IS","NTHOL.IS","NUGYO.IS","NUHCM.IS","OBAMS.IS","OBASE.IS","ODAS.IS","ODINE.IS","OFSYM.IS","ONCSM.IS","ONRYT.IS","ORCAY.IS","ORGE.IS","OSMEN.IS","OSTIM.IS","OTKAR.IS","OYAKC.IS","OYLUM.IS","OYYAT.IS","OZATD.IS","OZGYO.IS","OZKGY.IS","OZRDN.IS","OZSUB.IS","OZYSR.IS","PAGYO.IS","PAHOL.IS","PAMEL.IS","PAPIL.IS","PARSN.IS","PASEU.IS","PATEK.IS","PCILT.IS","PEKGY.IS","PENGD.IS","PENTA.IS","PETKM.IS","PETUN.IS","PGSUS.IS","PINSU.IS","PKART.IS","PKENT.IS","PLTUR.IS","PNLSN.IS","PNSUT.IS","POLHO.IS","POLTK.IS","PRDGS.IS","PRKAB.IS","PRKME.IS","PRZMA.IS","PSDTC.IS","PSGYO.IS","QUAGR.IS","RALYH.IS","RAYSG.IS","REEDR.IS","RGYAS.IS","RTALB.IS","RUBNS.IS","RUZYE.IS","RYGYO.IS","RYSAS.IS","SAFKR.IS","SAHOL.IS","SAMAT.IS","SANEL.IS","SANFM.IS","SANKO.IS","SARKY.IS","SASA.IS","SAYAS.IS","SDTTR.IS","SEGMN.IS","SEKUR.IS","SELEC.IS","SELVA.IS","SERNT.IS","SEYKM.IS","SILVR.IS","SISE.IS","SKTAS.IS","SKYLP.IS","SMART.IS","SMRTG.IS","SMRVA.IS","SNGYO.IS","SNICA.IS","SOKE.IS","SOKM.IS","SRVGY.IS","SUNTK.IS","SURGY.IS","SUWEN.IS","TABGD.IS","TARKM.IS","TATEN.IS","TATGD.IS","TAVHL.IS","TCELL.IS","TCKRC.IS","TEHOL.IS","TEKTU.IS","TERA.IS","TEZOL.IS","THYAO.IS","TKFEN.IS","TKNSA.IS","TLMAN.IS","TMPOL.IS","TMSN.IS","TNZTP.IS","TOASO.IS","TRCAS.IS","TRGYO.IS","TRHOL.IS","TRILC.IS","TSGYO.IS","TSPOR.IS","TTKOM.IS","TTRAK.IS","TUCLK.IS","TUKAS.IS","TUPRS.IS","TUREX.IS","TURGG.IS","TURSG.IS","ULAS.IS","ULKER.IS","ULUSE.IS","ULUUN.IS","UNLU.IS","USAK.IS","VAKKO.IS","VBTYZ.IS","VERTU.IS","VERUS.IS","VESBE.IS","VESTL.IS","VRGYO.IS","VSNMD.IS","YAPRK.IS","YATAS.IS","YBTAS.IS","YEOTK.IS","YESIL.IS","YGGYO.IS","YIGIT.IS","YKSLN.IS","YUNSA.IS","YYAPI.IS","YYLGD.IS","ZEDUR.IS","ZERGY.IS","ZGYO.IS"]

def grafik_ciz(ad, v):
    try:
        v20 = v.tail(20).copy()
        v20["RSI"] = ta.momentum.RSIIndicator(v["Close"], window=14).rsi().tail(20).values
        v20["RSI_EMA"] = v20["RSI"].ewm(span=9).mean()
        macd = ta.trend.MACD(v["Close"])
        v20["MACD"] = macd.macd().tail(20).values
        v20["MACD_S"] = macd.macd_signal().tail(20).values
        v20["MACD_H"] = macd.macd_diff().tail(20).values
        fig = plt.figure(figsize=(12, 9), facecolor="#0d1117")
        gs = gridspec.GridSpec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.05)
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax3 = fig.add_subplot(gs[2], sharex=ax1)
        ax4 = fig.add_subplot(gs[3], sharex=ax1)
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor("#0d1117")
            ax.tick_params(colors="#aaaaaa", labelsize=7)
            ax.yaxis.label.set_color("#aaaaaa")
            for spine in ax.spines.values():
                spine.set_edgecolor("#333333")
        for i, (_, row) in enumerate(v20.iterrows()):
            renk = "#26a69a" if row["Close"] >= row["Open"] else "#ef5350"
            ax1.plot([i, i], [row["Low"], row["High"]], color=renk, linewidth=0.8)
            ax1.bar(i, row["Close"] - row["Open"], bottom=row["Open"], color=renk, width=0.6)
        ax1.set_title(f"{ad} - Altin Sinyal", color="white", fontsize=10, pad=8)
        ax1.set_ylabel("Fiyat", color="#aaaaaa", fontsize=7)
        renkler = ["#26a69a" if v20["Close"].iloc[i] >= v20["Open"].iloc[i] else "#ef5350" for i in range(len(v20))]
        ax2.bar(range(len(v20)), v20["Volume"], color=renkler, alpha=0.6, width=0.6)
        ax2.set_ylabel("Hacim", color="#aaaaaa", fontsize=7)
        ax3.plot(range(len(v20)), v20["MACD"], color="#2196f3", linewidth=1)
        ax3.plot(range(len(v20)), v20["MACD_S"], color="#ff9800", linewidth=1)
        hist_renkler = ["#26a69a" if x >= 0 else "#ef5350" for x in v20["MACD_H"]]
        ax3.bar(range(len(v20)), v20["MACD_H"], color=hist_renkler, alpha=0.5, width=0.6)
        ax3.axhline(0, color="#444444", linewidth=0.5)
        ax3.set_ylabel("MACD", color="#aaaaaa", fontsize=7)
        ax4.plot(range(len(v20)), v20["RSI"], color="#ce93d8", linewidth=1)
        ax4.plot(range(len(v20)), v20["RSI_EMA"], color="#ffeb3b", linewidth=1, linestyle="--")
        ax4.axhline(70, color="#ef5350", linewidth=0.5, linestyle="--")
        ax4.axhline(30, color="#26a69a", linewidth=0.5, linestyle="--")
        ax4.set_ylim(0, 100)
        ax4.set_ylabel("RSI", color="#aaaaaa", fontsize=7)
        tarihler = [v20.index[i].strftime("%d/%m") for i in range(len(v20))]
        ax4.set_xticks(range(len(v20)))
        ax4.set_xticklabels(tarihler, rotation=45, fontsize=6)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)
        os.makedirs("C:/bist_terminal/grafikler", exist_ok=True)
        plt.savefig(f"C:/bist_terminal/grafikler/{ad}.png", dpi=150, bbox_inches="tight", facecolor="#0d1117")
        plt.close()
        print(f"  {ad} grafigi kaydedildi")
    except Exception as e:
        print(f"  {ad} grafik hatasi: {e}")

def tarama_yap():
    print(f"\nTarama basladi — {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    def yutan_boga(v):
        s, o = v.iloc[-1], v.iloc[-2]
        return (o["Close"] < o["Open"] and s["Close"] > s["Open"] and s["Open"] < o["Close"] and s["Close"] > o["Open"])

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
        return (a["Open"] > a["Close"] and abs(b["Close"] - b["Open"]) <= abs(a["Close"] - a["Open"]) * 0.3 and c["Close"] > c["Open"] and c["Close"] > (a["Open"] + a["Close"]) / 2)

    def boga_harami(v):
        s, o = v.iloc[-1], v.iloc[-2]
        return (o["Close"] < o["Open"] and s["Close"] > s["Open"] and s["Open"] > o["Close"] and s["Close"] < o["Open"] and abs(s["Close"] - s["Open"]) < abs(o["Close"] - o["Open"]))

    def uc_beyaz_asker(v):
        if len(v) < 3: return False
        a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
        return (a["Close"] > a["Open"] and b["Close"] > b["Open"] and c["Close"] > c["Open"] and b["Close"] > a["Close"] and c["Close"] > b["Close"] and b["Open"] > a["Open"] and c["Open"] > b["Open"])

    def delikli_bulut(v):
        s, o = v.iloc[-1], v.iloc[-2]
        orta = (o["Open"] + o["Close"]) / 2
        return (o["Close"] < o["Open"] and s["Close"] > s["Open"] and s["Open"] < o["Close"] and s["Close"] > orta and s["Close"] < o["Open"])

    def yutan_ayi(v):
        s, o = v.iloc[-1], v.iloc[-2]
        return (o["Close"] > o["Open"] and s["Close"] < s["Open"] and s["Open"] > o["Close"] and s["Close"] < o["Open"])

    def asilan_adam(v):
        s = v.iloc[-1]
        govde = abs(s["Close"] - s["Open"])
        alt_fitil = min(s["Close"], s["Open"]) - s["Low"]
        ust_fitil = s["High"] - max(s["Close"], s["Open"])
        return govde > 0 and alt_fitil >= 2 * govde and ust_fitil <= govde * 0.3

    def aksam_yildizi(v):
        if len(v) < 3: return False
        a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
        return (a["Close"] > a["Open"] and abs(b["Close"] - b["Open"]) <= abs(a["Close"] - a["Open"]) * 0.3 and c["Close"] < c["Open"] and c["Close"] < (a["Open"] + a["Close"]) / 2)

    def ayi_harami(v):
        s, o = v.iloc[-1], v.iloc[-2]
        return (o["Close"] > o["Open"] and s["Close"] < s["Open"] and s["Open"] < o["Close"] and s["Close"] > o["Open"] and abs(s["Close"] - s["Open"]) < abs(o["Close"] - o["Open"]))

    def uc_siyah_karga(v):
        if len(v) < 3: return False
        a, b, c = v.iloc[-3], v.iloc[-2], v.iloc[-1]
        return (a["Close"] < a["Open"] and b["Close"] < b["Open"] and c["Close"] < c["Open"] and b["Close"] < a["Close"] and c["Close"] < b["Close"] and b["Open"] < a["Open"] and c["Open"] < b["Open"])

    def kara_bulut_ortusu(v):
        s, o = v.iloc[-1], v.iloc[-2]
        orta = (o["Open"] + o["Close"]) / 2
        return (o["Close"] > o["Open"] and s["Close"] < s["Open"] and s["Open"] > o["Close"] and s["Close"] < orta and s["Close"] > o["Open"])

    sonuclar = {}
    gruplar = [hisseler[i:i+100] for i in range(0, len(hisseler), 100)]

    for g, grup in enumerate(gruplar):
        print(f"Grup {g+1}/5 taranıyor...")
        for hisse in grup:
            try:
                v = yf.Ticker(hisse).history(period="1y")
                if len(v) < 60:
                    continue

                ad = hisse.replace(".IS", "")
                kapanis = round(float(v["Close"].iloc[-1]), 2)

                rsi_seri = ta.momentum.RSIIndicator(v["Close"], window=14).rsi()
                rsi = round(float(rsi_seri.iloc[-1]), 2)

                macd_obj = ta.trend.MACD(v["Close"])
                macd_val = float(macd_obj.macd().iloc[-1])
                macd_sig_val = float(macd_obj.macd_signal().iloc[-1])
                macd_hist_onceki = float(macd_obj.macd_diff().iloc[-2])
                macd_hist_son = float(macd_obj.macd_diff().iloc[-1])

                bb = ta.volatility.BollingerBands(v["Close"], window=20)
                bb_alt = float(bb.bollinger_lband().iloc[-1])
                bb_ust = float(bb.bollinger_hband().iloc[-1])
                bb_width = float(bb.bollinger_wband().iloc[-1])
                bb_width_ort = float(bb.bollinger_wband().rolling(20).mean().iloc[-1])

                ema20_seri = v["Close"].ewm(span=20).mean()
                ema50_seri = v["Close"].ewm(span=50).mean()
                sma200_seri = v["Close"].rolling(window=200).mean()
                ema20 = float(ema20_seri.iloc[-1])
                ema50 = float(ema50_seri.iloc[-1])
                sma200 = float(sma200_seri.iloc[-1])
                ema20_onceki = float(ema20_seri.iloc[-2])
                ema50_onceki = float(ema50_seri.iloc[-2])

                hacim_ort = float(v["Volume"].iloc[-51:-1].mean())
                hacim_son = float(v["Volume"].iloc[-1])
                hacim_orani = round(hacim_son / hacim_ort, 2) if hacim_ort > 0 else 0

                sma200_gecerli = not (sma200 != sma200)

                sinyaller = []
                if rsi < 30: sinyaller.append("RSI Asiri Satim")
                if rsi > 70: sinyaller.append("RSI Asiri Alim")
                if macd_hist_onceki < 0 and macd_hist_son > 0: sinyaller.append("MACD Al Kesisimi")
                if macd_hist_onceki > 0 and macd_hist_son < 0: sinyaller.append("MACD Sat Kesisimi")
                if macd_val > macd_sig_val: sinyaller.append("MACD Pozitif")
                if macd_val < macd_sig_val: sinyaller.append("MACD Negatif")
                if kapanis <= bb_alt * 1.01: sinyaller.append("BB Alt Bant")
                if kapanis >= bb_ust * 0.99: sinyaller.append("BB Ust Bant")
                if kapanis > ema20: sinyaller.append("Fiyat EMA20 Ustunde")
                if kapanis < ema20: sinyaller.append("Fiyat EMA20 Altinda")
                if ema20 > ema50: sinyaller.append("EMA20 > EMA50")
                if ema20 < ema50: sinyaller.append("EMA20 < EMA50")
                if ema20_onceki < ema50_onceki and ema20 > ema50: sinyaller.append("Golden Cross")
                if ema20_onceki > ema50_onceki and ema20 < ema50: sinyaller.append("Death Cross")
                if hacim_orani >= 3: sinyaller.append(f"Anormal Hacim {hacim_orani}x")
                if sma200_gecerli:
                    if kapanis > sma200: sinyaller.append("Fiyat SMA200 Ustunde")
                    if kapanis < sma200: sinyaller.append("Fiyat SMA200 Altinda")
                if yutan_boga(v): sinyaller.append("Yutan Boga")
                if cekic(v): sinyaller.append("Cekic")
                if ters_cekic(v): sinyaller.append("Ters Cekic")
                if sabah_yildizi(v): sinyaller.append("Sabah Yildizi")
                if boga_harami(v): sinyaller.append("Boga Harami")
                if uc_beyaz_asker(v): sinyaller.append("3 Beyaz Asker")
                if delikli_bulut(v): sinyaller.append("Delikli Bulut")
                if yutan_ayi(v): sinyaller.append("Yutan Ayi")
                if asilan_adam(v): sinyaller.append("Asilan Adam")
                if aksam_yildizi(v): sinyaller.append("Aksam Yildizi")
                if ayi_harami(v): sinyaller.append("Ayi Harami")
                if uc_siyah_karga(v): sinyaller.append("3 Siyah Karga")
                if kara_bulut_ortusu(v): sinyaller.append("Kara Bulut Ortusu")

                dip_avcisi = bool(25 <= rsi <= 42 and sma200_gecerli and kapanis > sma200 * 0.97)
                patlama_oncesi = bool(not (bb_width_ort != bb_width_ort) and bb_width < bb_width_ort * 0.7)
                roket_rampa = bool(kapanis >= bb_ust * 0.98 and hacim_orani >= 2 and rsi > 55)
                destek_kalkani = bool(sma200_gecerli and abs(kapanis - sma200) / sma200 < 0.04 and rsi < 48)
                akilli_para = bool(hacim_orani >= 2 and float(v["Close"].iloc[-1]) > float(v["Open"].iloc[-1]) and kapanis > ema20)
                trend_sorfcusu = bool(ema20 > ema50 and macd_val > macd_sig_val and 48 <= rsi <= 72)

                if dip_avcisi: sinyaller.append("Dip Avcisi")
                if patlama_oncesi: sinyaller.append("Patlama Oncesi")
                if roket_rampa: sinyaller.append("Roket Rampa")
                if destek_kalkani: sinyaller.append("Destek Kalkani")
                if akilli_para: sinyaller.append("Akilli Para")
                if trend_sorfcusu: sinyaller.append("Trend Sorfcusu")

                ayi_sinyaller = ["MACD Sat Kesisimi","MACD Negatif","Fiyat EMA20 Altinda","EMA20 < EMA50",
                                 "Death Cross","Yutan Ayi","Asilan Adam","Aksam Yildizi","Ayi Harami",
                                 "3 Siyah Karga","Kara Bulut Ortusu","RSI Asiri Alim","BB Ust Bant","Fiyat SMA200 Altinda"]
                altin_skor = len([s for s in sinyaller if s not in ayi_sinyaller])

                if altin_skor >= 5: altin = "Altin"
                elif altin_skor >= 4: altin = "Gumus"
                elif altin_skor >= 2: altin = "Bronz"
                else: altin = None

                if sinyaller:
                    sonuclar[ad] = {
                        "kapanis": kapanis,
                        "rsi": rsi,
                        "sinyaller": sinyaller,
                        "sinyal_sayisi": altin_skor,
                        "altin": altin,
                        "dip_avcisi": dip_avcisi,
                        "patlama_oncesi": patlama_oncesi,
                        "roket_rampa": roket_rampa,
                        "destek_kalkani": destek_kalkani,
                        "akilli_para": akilli_para,
                        "trend_sorfcusu": trend_sorfcusu,
                        "golden_cross": bool(ema20_onceki < ema50_onceki and ema20 > ema50),
                        "death_cross": bool(ema20_onceki > ema50_onceki and ema20 < ema50),
                    }
                    if altin == "Altin":
                        grafik_ciz(ad, v)

            except Exception as e:
                print(f"HATA: {hisse} — {e}")
        time.sleep(3)

    with open("C:/bist_terminal/sonuclar.json", "w", encoding="utf-8") as f:
        json.dump({"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "hisseler": sonuclar}, f, ensure_ascii=False, indent=2)

    os.system("copy C:\\bist_terminal\\sonuclar.json C:\\bist_terminal\\bist-terminal\\sonuclar.json /Y")
    os.system('cd C:\\bist_terminal\\bist-terminal && git add . && git commit -m "otomatik guncelleme" && git push')

    altin_liste = [k for k, v in sonuclar.items() if v["altin"] == "Altin"]
    gumus_liste = [k for k, v in sonuclar.items() if v["altin"] == "Gumus"]
    bronz_liste = [k for k, v in sonuclar.items() if v["altin"] == "Bronz"]

    print(f"\nTARAMA TAMAMLANDI — {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print(f"Altin: {len(altin_liste)} | Gumus: {len(gumus_liste)} | Bronz: {len(bronz_liste)}")
    print("Sonuclar kaydedildi!")

schedule.every().day.at("18:26").do(tarama_yap)
print("Zamanlayici aktif — her gun 18:26'da tarama baslar")
print("Test icin tarama basliyor...\n")
tarama_yap()

while True:
    schedule.run_pending()
    time.sleep(30)