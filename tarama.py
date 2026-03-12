import json
import math
import os
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

TR_TZ = pytz.timezone('Europe/Istanbul')
simdi = datetime.now(TR_TZ)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_KANAL = os.environ.get("TELEGRAM_KANAL", "@ekonomiveborsa")

print(f"Tarama başlıyor... {simdi.strftime('%d.%m.%Y %H:%M')} | Periyot: Günlük")

HISSE_KODLARI = [
    # A - B
    "A1CAP","A1YEN","ACSEL","ADEL","ADESE","ADGYO","AEFES","AFYON","AGESA","AGHOL",
    "AGROT","AGYO","AHGAZ","AHSGY","AKBNK","AKCNS","AKENR","AKFGY","AKFIS","AKFYE",
    "AKGRT","AKHAN","AKMGY","AKSA","AKSEN","AKSGY","AKSUE","AKYHO","ALARK","ALBRK",
    "ALCAR","ALCTL","ALFAS","ALGYO","ALKA","ALKIM","ALKLC","ALTNY","ALVES","ANELE",
    "ANGEN","ANHYT","ANSGR","ARASE","ARCLK","ARDYZ","ARENA","ARFYE","ARMGD","ARSAN",
    "ARTMS","ARZUM","ASELS","ASGYO","ASTOR","ASUZU","ATAGY","ATAKP","ATATP","ATATR",
    "ATEKS","ATLAS","ATSYH","AVGYO","AVHOL","AVOD","AVPGY","AVTUR","AYCES","AYDEM",
    "AYEN","AYES","AYGAZ","AZTEK","BAGFS","BAHKM","BAKAB","BALAT","BALSU","BANVT",
    "BARMA","BASCM","BASGZ","BAYRK","BEGYO","BERA","BESLR","BESTE","BEYAZ","BFREN",
    "BIENY","BIGCH","BIGEN","BIGTK","BIMAS","BINBN","BINHO","BIOEN","BIZIM","BJKAS",
    "BLCYT","BLUME","BMSCH","BMSTL","BNTAS","BOBET","BORLS","BORSK","BOSSA","BRISA",
    "BRKO","BRKSN","BRKVY","BRLSM","BRMEN","BRSAN","BRYAT","BSOKE","BTCIM","BUCIM",
    "BULGS","BURCE","BURVA","BVSAN","BYDNR",
    # C - D - E
    "CANTE","CASA","CATES","CCOLA","CELHA","CEMAS","CEMTS","CEMZY","CEOEM","CGCAM",
    "CIMSA","CLEBI","CMBTN","CMENT","CONSE","COSMO","CRDFA","CRFSA","CUSAN","CVKMD",
    "CWENE","DAGI","DAPGM","DARDL","DCTTR","DENGE","DERHL","DERIM","DESA","DESPC",
    "DEVA","DGATE","DGGYO","DGNMO","DIRIT","DITAS","DMRGD","DMSAS","DNISI","DOAS",
    "DOCO","DOFER","DOFRB","DOGUB","DOHOL","DOKTA","DSTKF","DUNYH","DURDO","DURKN",
    "DYOBY","DZGYO","EBEBK","ECILC","ECOGR","ECZYT","EDATA","EDIP","EFOR","EGEEN",
    "EGEGY","EGEPO","EGGUB","EGPRO","EGSER","EKGYO","EKIZ","EKOS","EKSUN","ELITE",
    "EMKEL","EMNIS","EMPAE","ENDAE","ENERY","ENJSA","ENKAI","ENSRI","ENTRA","EPLAS",
    "ERBOS","ERCB","EREGL","ERSU","ESCAR","ESCOM","ESEN","ETILR","ETYAT","EUHOL",
    "EUKYO","EUPWR","EUREN","EUYO","EYGYO",
    # F - G - H
    "FADE","FENER","FLAP","FMIZP","FONET","FORMT","FORTE","FRIGO","FRMPL","FROTO",
    "FZLGY","GARAN","GARFA","GATEG","GEDIK","GEDZA","GENIL","GENKM","GENTS","GEREL",
    "GESAN","GIPTA","GLBMD","GLCVY","GLRMK","GLRYH","GLYHO","GMTAS","GOKNR","GOLTS",
    "GOODY","GOZDE","GRNYO","GRSEL","GRTHO","GSDDE","GSDHO","GSRAY","GUBRF","GUNDG",
    "GWIND","GZNMI","HALKB","HALKS","HATEK","HATSN","HDFGS","HEDEF","HEKTS","HKTM",
    "HLGYO","HOROZ","HRKET","HTTBT","HUBVC","HUNER","HURGZ",
    # I - J - K - L
    "ICBCT","ICUGS","IDGYO","IEYHO","IHAAS","IHEVA","IHGZT","IHLAS","IHLGM","IHYAY",
    "IMASM","INDES","INFO","INGRM","INTEK","INTEM","INVEO","INVES","ISATR","ISBIR",
    "ISBTR","ISCTR","ISDMR","ISFIN","ISGSY","ISGYO","ISKPL","ISKUR","ISMEN","ISSEN",
    "ISYAT","IZENR","IZFAS","IZINV","IZMDC","JANTS","KAPLM","KAREL","KARSN","KARTN",
    "KATMR","KAYSE","KBORU","KCAER","KCHOL","KENT","KERVN","KFEIN","KGYO","KIMMR",
    "KLGYO","KLKIM","KLMSN","KLNMA","KLRHO","KLSER","KLSYN","KLYPV","KMPUR","KNFRT",
    "KOCMT","KONKA","KONTR","KONYA","KOPOL","KORDS","KOTON","KRDMA","KRDMB","KRDMD",
    "KRGYO","KRONT","KRPLS","KRSTL","KRTEK","KRVGD","KSTUR","KTLEV","KTSKR","KUTPO",
    "KUVVA","KUYAS","KZBGY","KZGYO","LIDER","LIDFA","LILAK","LINK","LKMNH","LMKDC",
    "LOGO","LRSHO","LUKSK","LXGYO","LYDHO","LYDYE",
    # M - N - O - P
    "MAALT","MACKO","MAGEN","MAKIM","MAKTK","MANAS","MARBL","MARKA","MARMR","MARTI",
    "MAVI","MCARD","MEDTR","MEGAP","MEGMT","MEKAG","MEPET","MERCN","MERIT","MERKO",
    "METRO","MEYSU","MGROS","MHRGY","MIATK","MMCAS","MNDRS","MNDTR","MOBTL","MOGAN",
    "MOPAS","MPARK","MRGYO","MRSHL","MSGYO","MTRKS","MTRYO","MZHLD","NATEN","NETAS",
    "NETCD","NIBAS","NTGAZ","NTHOL","NUGYO","NUHCM","OBAMS","OBASE","ODAS","ODINE",
    "OFSYM","ONCSM","ONRYT","ORCAY","ORGE","ORMA","OSMEN","OSTIM","OTKAR","OTTO",
    "OYAKC","OYAYO","OYLUM","OYYAT","OZATD","OZGYO","OZKGY","OZRDN","OZSUB","OZYSR",
    "PAGYO","PAHOL","PAMEL","PAPIL","PARSN","PASEU","PATEK","PCILT","PEKGY","PENGD",
    "PENTA","PETKM","PETUN","PGSUS","PINSU","PKART","PKENT","PLTUR","PNLSN","PNSUT",
    "POLHO","POLTK","PRDGS","PRKAB","PRKME","PRZMA","PSDTC","PSGYO",
    # Q - R - S - T
    "QNBFK","QNBTR","QUAGR","RALYH","RAYSG","REEDR","RGYAS","RNPOL","RODRG","ROYAL",
    "RTALB","RUBNS","RUZYE","RYGYO","RYSAS","SAFKR","SAHOL","SAMAT","SANEL","SANFM",
    "SANKO","SARKY","SASA","SAYAS","SDTTR","SEGMN","SEGYO","SEKFK","SEKUR","SELEC",
    "SELVA","SERNT","SEYKM","SILVR","SISE","SKBNK","SKTAS","SKYLP","SKYMD","SMART",
    "SMRTG","SMRVA","SNGYO","SNICA","SNPAM","SODSN","SOKE","SOKM","SONME","SRVGY",
    "SUMAS","SUNTK","SURGY","SUWEN","SVGYO","TABGD","TARKM","TATEN","TATGD","TAVHL",
    "TBORG","TCELL","TCKRC","TDGYO","TEHOL","TEKTU","TERA","TEZOL","TGSAS","THYAO",
    "TKFEN","TKNSA","TLMAN","TMPOL","TMSN","TNZTP","TOASO","TRALT","TRCAS","TRENJ",
    "TRGYO","TRHOL","TRILC","TRMET","TSGYO","TSKB","TSPOR","TTKOM","TTRAK","TUCLK",
    "TUKAS","TUPRS","TUREX","TURGG","TURSG",
    # U - V - Y - Z
    "UCAYM","UFUK","ULAS","ULKER","ULUFA","ULUSE","ULUUN","UMPAS","UNLU","USAK",
    "USDTR","VAKBN","VAKFA","VAKFN","VAKKO","VANGD","VBTYZ","VERTU","VERUS","VESBE",
    "VESTL","VKFYO","VKGYO","VKING","VRGYO","VSNMD","YAPRK","YATAS","YAYLA","YBTAS",
    "YEOTK","YESIL","YGGYO","YGYO","YIGIT","YKBNK","YKSLN","YONGA","YUNSA","YYAPI",
    "YYLGD","ZEDUR","ZERGY","ZGYO","ZOREN",
]

HISSELER = [h + ".IS" for h in HISSE_KODLARI]


def nan_temizle(obj):
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: nan_temizle(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [nan_temizle(i) for i in obj]
    return obj


def hesapla_gosterge(df):
    close  = df['Close'].astype(float)
    high   = df['High'].astype(float)
    low    = df['Low'].astype(float)
    volume = df['Volume'].astype(float)
    ema20  = close.ewm(span=20, adjust=False).mean()
    ema50  = close.ewm(span=50, adjust=False).mean()
    sma200 = close.rolling(200).mean()
    delta  = close.diff()
    gain   = delta.clip(lower=0).rolling(14).mean()
    loss   = (-delta.clip(upper=0)).rolling(14).mean()
    rs     = gain / loss.replace(0, np.nan)
    rsi    = 100 - (100 / (1 + rs))
    ema12  = close.ewm(span=12, adjust=False).mean()
    ema26  = close.ewm(span=26, adjust=False).mean()
    macd   = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    sma20    = close.rolling(20).mean()
    std20    = close.rolling(20).std()
    bb_lower = sma20 - 2 * std20
    bb_upper = sma20 + 2 * std20
    vol_ort  = volume.rolling(20).mean()
    return {
        'close': close, 'high': high, 'low': low, 'volume': volume,
        'ema20': ema20, 'ema50': ema50, 'sma200': sma200,
        'rsi': rsi, 'macd': macd, 'signal': signal, 'histogram': histogram,
        'bb_lower': bb_lower, 'bb_upper': bb_upper, 'vol_ort': vol_ort
    }


def mum_formasyonlari(df):
    sinyaller = []
    if len(df) < 3:
        return sinyaller
    o  = float(df['Open'].iloc[-1]);  h  = float(df['High'].iloc[-1])
    l  = float(df['Low'].iloc[-1]);   c  = float(df['Close'].iloc[-1])
    o1 = float(df['Open'].iloc[-2]);  h1 = float(df['High'].iloc[-2])
    l1 = float(df['Low'].iloc[-2]);   c1 = float(df['Close'].iloc[-2])
    o2 = float(df['Open'].iloc[-3]);  c2 = float(df['Close'].iloc[-3])
    body  = abs(c - o)
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    ort_fiyat = float(df['Close'].tail(10).mean())
    min_body  = ort_fiyat * 0.005
    boga  = c > o;  ayi1 = c1 < o1;  ayi2 = c2 < o2;  boga1 = c1 > o1
    ust_golge = h - max(o, c)
    alt_golge = min(o, c) - l
    if body >= min_body and alt_golge >= body * 2.0 and ust_golge <= body * 0.3:
        sinyaller.append("Cekic")
    if ayi1 and body >= min_body and ust_golge >= body * 2.0 and alt_golge <= body * 0.3:
        sinyaller.append("Ters Cekic")
    if body1 >= min_body and body >= min_body and ayi1 and boga and o < c1 and c > o1:
        sinyaller.append("Yutan Boga")
    if body1 >= min_body and body >= min_body and ayi1 and boga and o > c1 and c < o1 and body < body1 * 0.6:
        sinyaller.append("Boga Harami")
    orta2 = (o2 + c2) / 2
    yildiz_tepesi = max(o1, c1)
    if (body2 >= min_body and ayi2 and body1 < body2 * 0.35 and
            yildiz_tepesi < c2 and boga and body >= min_body and c > orta2):
        sinyaller.append("Sabah Yildizi")
    if (body2 >= min_body and body1 >= min_body and body >= min_body and
            c2 > o2 and boga1 and boga and c > c1 > c2 and o > o1 > o2 and o <= c1 and o1 <= c2):
        sinyaller.append("3 Beyaz Asker")
    return sinyaller


def ozel_tarama_kontrol(df):
    try:
        if len(df) < 15:
            return False
        close = df['Close'].astype(float)
        low   = df['Low'].astype(float)
        high  = df['High'].astype(float)
        ema5  = close.ewm(span=5,  adjust=False).mean()
        ema8  = close.ewm(span=8,  adjust=False).mean()
        ema13 = close.ewm(span=13, adjust=False).mean()
        ema34 = close.ewm(span=34, adjust=False).mean()
        def temas_var(ema_ser):
            e  = float(ema_ser.iloc[-1]); e1 = float(ema_ser.iloc[-2])
            l_ = float(low.iloc[-1]);     h_ = float(high.iloc[-1])
            c_ = float(close.iloc[-1]);   c1 = float(close.iloc[-2])
            return (l_ <= e <= h_) or (c_ > e and c1 <= e1)
        if not any(temas_var(e) for e in [ema5, ema8, ema13, ema34]):
            return False
        mumlar = mum_formasyonlari(df)
        return "Yutan Boga" in mumlar or "Sabah Yildizi" in mumlar
    except:
        return False


def sinyal_uret(df, g):
    sinyaller = []
    close = g['close']
    n = -1
    if len(close) < 3:
        return sinyaller
    vol_ort = float(g['vol_ort'].iloc[n]) if pd.notna(g['vol_ort'].iloc[n]) else 0

    # MACD
    if (pd.notna(g['macd'].iloc[n]) and pd.notna(g['signal'].iloc[n]) and
            pd.notna(g['macd'].iloc[n-1]) and pd.notna(g['signal'].iloc[n-1])):
        if g['macd'].iloc[n] > g['signal'].iloc[n] and g['macd'].iloc[n-1] <= g['signal'].iloc[n-1]:
            sinyaller.append("MACD Al Kesisimi")
        if g['macd'].iloc[n] > g['signal'].iloc[n]:
            sinyaller.append("MACD Pozitif")
        else:
            sinyaller.append("MACD Negatif")

    # EMA konumu
    if pd.notna(g['ema20'].iloc[n]):
        if close.iloc[n] > g['ema20'].iloc[n]:
            sinyaller.append("Fiyat EMA20 Ustunde")
        else:
            sinyaller.append("Fiyat EMA20 Altinda")
    if pd.notna(g['ema50'].iloc[n]):
        if close.iloc[n] > g['ema50'].iloc[n]:
            sinyaller.append("Fiyat EMA50 Ustunde")
        else:
            sinyaller.append("Fiyat EMA50 Altinda")
    if pd.notna(g['sma200'].iloc[n]):
        if close.iloc[n] > g['sma200'].iloc[n]:
            sinyaller.append("Fiyat SMA200 Ustunde")
        else:
            sinyaller.append("Fiyat SMA200 Altinda")

    # EMA20 vs EMA50 kesişim
    if pd.notna(g['ema20'].iloc[n]) and pd.notna(g['ema50'].iloc[n]):
        if g['ema20'].iloc[n] > g['ema50'].iloc[n]:
            sinyaller.append("EMA20 > EMA50")
        else:
            sinyaller.append("EMA20 < EMA50")
        if pd.notna(g['ema20'].iloc[n-1]) and pd.notna(g['ema50'].iloc[n-1]):
            if g['ema20'].iloc[n-1] <= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] > g['ema50'].iloc[n]:
                sinyaller.append("Golden Cross")
            if g['ema20'].iloc[n-1] >= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] < g['ema50'].iloc[n]:
                sinyaller.append("Death Cross")

    # RSI
    if pd.notna(g['rsi'].iloc[n]):
        rsi = g['rsi'].iloc[n]
        if rsi < 35:
            sinyaller.append("RSI Asiri Satim")
        elif rsi > 70:
            sinyaller.append("RSI Asiri Alim")
        elif rsi >= 50:
            sinyaller.append("RSI Yukseliyor")
        else:
            sinyaller.append("RSI Dusuyor")

    # Bollinger
    if pd.notna(g['bb_lower'].iloc[n]) and pd.notna(g['bb_upper'].iloc[n]):
        if close.iloc[n] <= g['bb_lower'].iloc[n]:
            sinyaller.append("BB Alt Bant")
        elif close.iloc[n] >= g['bb_upper'].iloc[n]:
            sinyaller.append("BB Ust Bant")

    # Hacim
    if vol_ort > 0 and g['volume'].iloc[n] > vol_ort * 2:
        sinyaller.append("Hacim Alarmi")

    # Mum formasyonları
    sinyaller += mum_formasyonlari(df)

    # Kombine sinyaller
    if pd.notna(g['rsi'].iloc[n]) and pd.notna(g['bb_lower'].iloc[n]):
        if g['rsi'].iloc[n] < 35 and close.iloc[n] <= g['bb_lower'].iloc[n]:
            sinyaller.append("Dip Vurusu")

    if pd.notna(g['bb_upper'].iloc[n]) and pd.notna(g['bb_lower'].iloc[n]):
        bb_width = g['bb_upper'] - g['bb_lower']
        bb_ort   = bb_width.rolling(20).mean()
        if pd.notna(bb_width.iloc[n]) and pd.notna(bb_ort.iloc[n]) and bb_ort.iloc[n] > 0:
            if bb_width.iloc[n] < bb_ort.iloc[n] * 0.7:
                sinyaller.append("Bant Sikismasi")

    if (pd.notna(g['rsi'].iloc[n]) and g['rsi'].iloc[n] > 55 and
            pd.notna(g['macd'].iloc[n]) and pd.notna(g['signal'].iloc[n]) and
            g['macd'].iloc[n] > g['signal'].iloc[n] and
            pd.notna(g['ema20'].iloc[n]) and close.iloc[n] > g['ema20'].iloc[n]):
        sinyaller.append("Guc Patlamasi")

    if pd.notna(g['ema20'].iloc[n]):
        if close.iloc[n] > g['ema20'].iloc[n] * 0.98 and close.iloc[n] < g['ema20'].iloc[n] * 1.02:
            sinyaller.append("Destek Testi")

    if vol_ort > 0 and g['volume'].iloc[n] > vol_ort * 2.5:
        sinyaller.append("Hacim Bombasi")

    if (pd.notna(g['ema20'].iloc[n]) and pd.notna(g['ema50'].iloc[n]) and
            pd.notna(g['macd'].iloc[n]) and pd.notna(g['signal'].iloc[n]) and
            close.iloc[n] > g['ema20'].iloc[n] and
            g['ema20'].iloc[n] > g['ema50'].iloc[n] and
            g['macd'].iloc[n] > g['signal'].iloc[n]):
        sinyaller.append("Trend Uyumu")

    return list(dict.fromkeys(sinyaller))


def altin_seviye(sinyaller):
    boga = [
        "Yutan Boga","Cekic","Ters Cekic","Sabah Yildizi","Boga Harami","3 Beyaz Asker",
        "MACD Al Kesisimi","Golden Cross","RSI Asiri Satim","BB Alt Bant",
        "Hacim Alarmi","Dip Vurusu","Guc Patlamasi"
    ]
    puan = sum(1 for s in sinyaller if s in boga)
    if puan >= 5: return "Altin"
    if puan >= 3: return "Gumus"
    if puan >= 1: return "Bronz"
    return None


def telegram_gonder(mesaj):
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_KANAL,
            "text": mesaj,
            "parse_mode": "Markdown"
        }, timeout=10)
    except Exception as e:
        print(f"Telegram bildirim hatası: {e}")


sonuclar = {}
bugun_str = (simdi + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

for ticker in HISSELER:
    try:
        df = yf.download(
            ticker, start="2023-01-01", end=bugun_str,
            interval="1d", progress=False, auto_adjust=True
        )
        if df is None or len(df) < 10:
            continue
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        g         = hesapla_gosterge(df)
        sinyaller = sinyal_uret(df, g)
        seviye    = altin_seviye(sinyaller)
        ad        = ticker.replace(".IS", "")
        n = -1
        rsi_val    = round(float(g['rsi'].iloc[n]), 1)       if pd.notna(g['rsi'].iloc[n])       else None
        macd_val   = round(float(g['macd'].iloc[n]), 4)      if pd.notna(g['macd'].iloc[n])      else None
        signal_val = round(float(g['signal'].iloc[n]), 4)    if pd.notna(g['signal'].iloc[n])    else None
        hist_val   = round(float(g['histogram'].iloc[n]), 4) if pd.notna(g['histogram'].iloc[n]) else None
        vol_bugun  = float(g['volume'].iloc[n])
        vol_ort_v  = float(g['vol_ort'].iloc[n]) if pd.notna(g['vol_ort'].iloc[n]) else 0
        hacim_oran = round(vol_bugun / vol_ort_v, 2) if vol_ort_v > 0 else None
        sonuclar[ad] = {
            "kapanis":        round(float(g['close'].iloc[n]), 2),
            "rsi":            rsi_val,
            "macd":           macd_val,
            "macd_sinyal":    signal_val,
            "macd_histogram": hist_val,
            "hacim_oran":     hacim_oran,
            "sinyaller":      sinyaller,
            "altin":          seviye,
            "dip_vurusu":     "Dip Vurusu"     in sinyaller,
            "bant_sikismasi": "Bant Sikismasi"  in sinyaller,
            "guc_patlamasi":  "Guc Patlamasi"   in sinyaller,
            "destek_testi":   "Destek Testi"    in sinyaller,
            "hacim_bombasi":  "Hacim Bombasi"   in sinyaller,
            "trend_uyumu":    "Trend Uyumu"     in sinyaller,
            "ozel_tarama":    ozel_tarama_kontrol(df),
        }
    except Exception as e:
        print(f"Hata {ticker}: {e}")

cikti = {
    "tarih":    simdi.strftime("%d.%m.%Y %H:%M"),
    "periyot":  "gunluk",
    "hisseler": sonuclar
}
with open("sonuclar.json", "w", encoding="utf-8") as f:
    json.dump(nan_temizle(cikti), f, ensure_ascii=False, indent=2)

print(f"Tamamlandı! {len(sonuclar)} hisse işlendi. → sonuclar.json")

altin_list = [k for k, v in sonuclar.items() if v.get("altin") == "Altin"]
gumus_list = [k for k, v in sonuclar.items() if v.get("altin") == "Gumus"]
ozel_list  = [k for k, v in sonuclar.items() if v.get("ozel_tarama")]

mesaj = (
    f"📊 *BIST Günlük Tarama Tamamlandı*\n"
    f"━━━━━━━━━━━━━━━━━━━━\n"
    f"🕐 {simdi.strftime('%d.%m.%Y %H:%M')}\n\n"
    f"🏆 Altın Sinyal: *{len(altin_list)}* hisse\n"
    f"🥈 Gümüş Sinyal: *{len(gumus_list)}* hisse\n"
    f"🏅 Özel Tarama: *{len(ozel_list)}* hisse\n\n"
)
if altin_list:
    mesaj += "🔥 *Öne Çıkan Altın Hisseler:*\n"
    for ad in altin_list[:5]:
        h = sonuclar[ad]
        mesaj += f"• *{ad}* — {h['kapanis']} TL | RSI: {h['rsi']}\n"
    if len(altin_list) > 5:
        mesaj += f"_...ve {len(altin_list)-5} hisse daha_\n"
mesaj += "\n📱 Detaylar için terminali aç!\n⚠️ _Yatırım tavsiyesi değildir._"
telegram_gonder(mesaj)
print("Telegram bildirimi gönderildi.")
