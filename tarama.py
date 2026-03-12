import json
import math
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

TR_TZ = pytz.timezone('Europe/Istanbul')
simdi = datetime.now(TR_TZ)

print(f"Tarama başlıyor... {simdi.strftime('%d.%m.%Y %H:%M')} | Periyot: Günlük")

HISSELER = [h + ".IS" for h in [
    "ACSEL","ADEL","ADESE","AEFES","AFYON","AGESA","AGHOL","AGROT","AGYO","AHGAZ",
    "AKCNS","AKFGY","AKFYE","AKGRT","AKIS","AKSA","AKSEN","AKSGY","AKSUE","AKTIF",
    "ALARK","ALBRK","ALCAR","ALFAS","ALGYO","ALKA","ALKIM","ALKLC","ALMAD","ALOKA",
    "ALTINS","ALTNY","ALVES","ANELE","ANENR","ANHYT","ANSGR","ARASE","ARCLK","ARDYZ",
    "ARENA","ARSAN","ASELS","ASLAN","ASTOR","ATAGY","ATAKP","ATATP","ATEKS","ATLAS",
    "ATSYH","AVHOL","AVGYO","AVOD","AVPGY","AVTUR","AYCES","AYEN","AYGAZ","AYGLD",
    "AYNES","AYYGE","BAGFS","BAKAB","BALAT","BANVT","BARMA","BASCM","BASGZ","BAYRK",
    "BEGYO","BERA","BEYAZ","BFREN","BIMAS","BIOEN","BIZIM","BJKAS","BLCYT","BMSCH",
    "BMSTL","BNTAS","BOBET","BOSSA","BRISA","BRKO","BRKSN","BRKVY","BRLSM","BRMEN",
    "BRSAN","BRYAT","BSOKE","BTCIM","BUCIM","BURCE","BURVA","BVSAN","BYDNR","CAFER",
    "CANTE","CARFA","CEMAS","CEMTS","CEOEM","CIMSA","CLEBI","CMBTN","CMENT","CONSE",
    "COSMO","CRDFA","CRFSA","CUSAN","CVKMD","CWENE","DAGHL","DAGI","DARDL","DENGE",
    "DERHL","DERIM","DESA","DESPC","DEVA","DGATE","DGNMO","DIRIT","DITAS","DMSAS",
    "DNISI","DOAS","DOBUR","DOGUB","DOHOL","DOKTH","DURDO","DYOBY","DZGYO","EBEBK",
    "ECILC","ECZYT","EDATA","EDIP","EFORC","EGEEN","EGGUB","EGPRO","EGSER","EKGYO",
    "EKSUN","ELITE","EMKEL","EMNIS","ENERY","ENJSA","ENKAI","ENSRI","EPLAS","ERBOS",
    "ERCB","ERDMR","EREGL","ERSU","ESCAR","ESCOM","ESEN","ETILR","ETYAT","EUHOL",
    "EUKYO","EUPWR","EUREN","EUYO","EYGYO","FADE","FENER","FLAP","FMIZP","FONET",
    "FORMT","FORTE","FROTO","FZLGY","GARAN","GARFA","GEDIK","GEDZA","GENIL","GENTS",
    "GEREL","GESAN","GLBMD","GLCVY","GLRYH","GLYHO","GMTAS","GOKNR","GOLTS","GOODY",
    "GOZDE","GRTHO","GRTRK","GSDDE","GSDHO","GSRAY","GUBRF","GWIND","GZNMI","HALKB",
    "HATEK","HDFGS","HEDEF","HEKTS","HLGYO","HOROZ","HRKET","HTTBT","HUBVC","HUNER",
    "HURGZ","ICBCT","ICUGS","IDEAS","IEYHO","IHAAS","IHEVA","IHGZT","IHLAS","IHLGM",
    "IHYAY","IISBF","IKNAS","IMASM","INDES","INFO","INTEM","INVEO","INVES","IPEKE",
    "ISATR","ISBIR","ISYAT","ITTFK","IZENR","IZFAS","IZGYO","IZINV","IZMDC","IZTAR",
    "JANTS","KAPLM","KAREL","KARSN","KARTN","KATMR","KAYSE","KCAER","KCHOL","KENT",
    "KERVN","KERVT","KFEIN","KGYO","KIMMR","KLGYO","KLKIM","KLMSN","KLNMA","KLRHO",
    "KLSER","KLSYN","KMPUR","KNFRT","KONYA","KOPOL","KORDS","KOTON","KRDMA","KRDMB",
    "KRDMD","KRPLS","KRSTL","KRTEK","KRVGD","KSTUR","KTLEV","KTSKR","KUTPO","KUVVA",
    "KUYAS","KZBGY","KZGYO","LIDER","LIDFA","LILAK","LINK","LKMNH","LMKDC","LOGO",
    "LRESY","LUKSK","MAALT","MACKO","MAGEN","MAKIM","MAKTK","MANAS","MARKA","MARTI",
    "MAVI","MEDTR","MEGAP","MEKAG","METEM","METRO","METUR","MGROS","MHRGY","MIATK",
    "MIGRS","MMCAS","MNDRS","MNDTR","MOBTL","MOGAN","MPARK","MRGYO","MRSHL","MSGYO",
    "MTRKS","MTSGY","MZHLD","NATEN","NETAS","NIBAS","NILFE","NTHOL","NUGYO","NUHCM",
    "OBAMS","OBASE","ODAS","ODINE","OFSYM","ONCSM","ONRYT","ORCAY","ORGE","ORMA",
    "OSMEN","OSTIM","OTKAR","OTTO","OYAKC","OYAYO","OYLUM","OYYAT","OZGYO","OZKGY",
    "OZRDN","OZSUB","PAGYO","PAMEL","PAPIL","PARSN","PASEU","PCILT","PEHOL","PEKGY",
    "PENGD","PENTA","PETKM","PETUN","PGSUS","PINSU","PKART","PKENT","PLTUR","PNLSN",
    "POLHO","POLTK","PRDGS","PRKAR","PRZMA","PSDTC","PSGYO","PTOFS","QNBFB","QNBFL",
    "RALYH","RAYSG","REEDR","RGYAS","RODRG","RTALB","RUBNS","RYSAS","SAFKR","SAHOL",
    "SAMAT","SANEL","SANFM","SANKO","SARKY","SASA","SAYAS","SDTTR","SEGYO","SEKFK",
    "SEKUR","SELEC","SELGD","SELVA","SEYKM","SILVR","SISE","SKBNK","SKTAS","SMART",
    "SNGYO","SNKRN","SODSN","SOKM","SONME","SRVGY","SUMAS","SUNTK","SURGY","SUWEN",
    "TABGD","TARKM","TATGD","TAVHL","TBORG","TCELL","TCKRC","TDGYO","TEKTU","TERA",
    "TEZOL","TGSAS","THYAO","TKFEN","TKNSA","TLMAN","TMSN","TOASO","TRCAS","TRGYO",
    "TRILC","TSPOR","TTKOM","TTRAK","TUCLK","TUKAS","TUPRS","TUREX","TURGG","TURSG",
    "ULUFA","ULUSE","ULUUN","UMPAS","UNLU","USAK","USDTR","UTPYA","UVDDE","UYUM",
    "UZERT","VAKBN","VAKFN","VAKKO","VANGD","VBTS","VERTU","VERUS","VESBE","VESTL",
    "VKFYO","VKGYO","VRGYO","YAPRK","YATAS","YAYLA","YBTAS","YELCO","YESIL","YETAR",
    "YGGYO","YGYO","YKSLN","YLDNM","YLGYO","YONGA","YORSA","YSDNM","YSLTM","YTKYO",
    "YUFER","ZEDUR","ZRGYO","ZYMRT"
]]


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
    sma20    = close.rolling(20).mean()
    std20    = close.rolling(20).std()
    bb_lower = sma20 - 2 * std20
    bb_upper = sma20 + 2 * std20
    return {
        'close': close, 'high': high, 'low': low, 'volume': volume,
        'ema20': ema20, 'ema50': ema50, 'sma200': sma200,
        'rsi': rsi, 'macd': macd, 'signal': signal,
        'bb_lower': bb_lower, 'bb_upper': bb_upper
    }


def mum_formasyonlari(df):
    sinyaller = []
    if len(df) < 3:
        return sinyaller

    o  = float(df['Open'].iloc[-1])
    h  = float(df['High'].iloc[-1])
    l  = float(df['Low'].iloc[-1])
    c  = float(df['Close'].iloc[-1])
    o1 = float(df['Open'].iloc[-2])
    h1 = float(df['High'].iloc[-2])
    l1 = float(df['Low'].iloc[-2])
    c1 = float(df['Close'].iloc[-2])
    o2 = float(df['Open'].iloc[-3])
    h2 = float(df['High'].iloc[-3])
    l2 = float(df['Low'].iloc[-3])
    c2 = float(df['Close'].iloc[-3])

    body  = abs(c - o)
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)

    ort_fiyat = float(df['Close'].tail(10).mean())
    min_body  = ort_fiyat * 0.003

    boga  = c  > o
    ayi1  = c1 < o1
    ayi2  = c2 < o2
    boga1 = c1 > o1

    ust_golge = h - max(o, c)
    alt_golge = min(o, c) - l

    if body >= min_body and alt_golge >= body * 2.0 and ust_golge <= body * 0.3:
        sinyaller.append("Cekic")

    if ayi1 and body >= min_body and ust_golge >= body * 2.0 and alt_golge <= body * 0.3:
        sinyaller.append("Ters Cekic")

    if body1 >= min_body and body >= min_body and ayi1 and boga and o <= c1 and c >= o1:
        sinyaller.append("Yutan Boga")

    if (body1 >= min_body and body >= min_body and ayi1 and boga and
            o >= c1 and c <= o1 and body < body1 * 0.6):
        sinyaller.append("Boga Harami")

    orta2 = (o2 + c2) / 2
    yildiz_tepesi = max(o1, c1)
    if (body2 >= min_body and ayi2 and body1 < body2 * 0.35 and
            yildiz_tepesi < c2 and boga and body >= min_body and c > orta2):
        sinyaller.append("Sabah Yildizi")

    if (body2 >= min_body and body1 >= min_body and body >= min_body and
            c2 > o2 and boga1 and boga and c > c1 > c2 and o > o1 > o2 and
            o <= c1 and o1 <= c2 + body2):
        sinyaller.append("3 Beyaz Asker")

    return sinyaller


def ozel_tarama_kontrol(df):
    """Gizli strateji — koşullar dışarıya gösterilmez."""
    try:
        if len(df) < 35:
            return False

        close = df['Close'].astype(float)
        low   = df['Low'].astype(float)
        high  = df['High'].astype(float)

        ema5  = close.ewm(span=5,  adjust=False).mean()
        ema8  = close.ewm(span=8,  adjust=False).mean()
        ema13 = close.ewm(span=13, adjust=False).mean()
        ema34 = close.ewm(span=34, adjust=False).mean()

        def temas_var(ema_ser):
            e  = float(ema_ser.iloc[-1])
            e1 = float(ema_ser.iloc[-2])
            l  = float(low.iloc[-1])
            h  = float(high.iloc[-1])
            c  = float(close.iloc[-1])
            c1 = float(close.iloc[-2])
            temas   = l <= e <= h
            kesisim = c > e and c1 <= e1
            return temas or kesisim

        ema_temas = any(temas_var(e) for e in [ema5, ema8, ema13, ema34])
        if not ema_temas:
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

    vol_ort = float(g['volume'].rolling(20).mean().iloc[n])

    if (pd.notna(g['macd'].iloc[n]) and pd.notna(g['signal'].iloc[n]) and
            pd.notna(g['macd'].iloc[n-1]) and pd.notna(g['signal'].iloc[n-1])):
        if g['macd'].iloc[n] > g['signal'].iloc[n] and g['macd'].iloc[n-1] <= g['signal'].iloc[n-1]:
            sinyaller.append("MACD Al Kesisimi")
        if g['macd'].iloc[n] > g['signal'].iloc[n]:
            sinyaller.append("MACD Pozitif")

    if pd.notna(g['ema20'].iloc[n]) and close.iloc[n] > g['ema20'].iloc[n]:
        sinyaller.append("Fiyat EMA20 Ustunde")

    if pd.notna(g['ema20'].iloc[n]) and pd.notna(g['ema50'].iloc[n]):
        if g['ema20'].iloc[n] > g['ema50'].iloc[n]:
            sinyaller.append("EMA20 > EMA50")
        if pd.notna(g['ema20'].iloc[n-1]) and pd.notna(g['ema50'].iloc[n-1]):
            if g['ema20'].iloc[n-1] <= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] > g['ema50'].iloc[n]:
                sinyaller.append("Golden Cross")
            if g['ema20'].iloc[n-1] >= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] < g['ema50'].iloc[n]:
                sinyaller.append("Death Cross")

    if pd.notna(g['sma200'].iloc[n]) and close.iloc[n] > g['sma200'].iloc[n]:
        sinyaller.append("Fiyat SMA200 Ustunde")

    if pd.notna(g['rsi'].iloc[n]) and g['rsi'].iloc[n] < 35:
        sinyaller.append("RSI Asiri Satim")

    if pd.notna(g['bb_lower'].iloc[n]) and close.iloc[n] <= g['bb_lower'].iloc[n]:
        sinyaller.append("BB Alt Bant")

    if pd.notna(vol_ort) and vol_ort > 0 and g['volume'].iloc[n] > vol_ort * 2:
        sinyaller.append("Hacim Alarmi")

    sinyaller += mum_formasyonlari(df)

    if pd.notna(g['rsi'].iloc[n]) and pd.notna(g['bb_lower'].iloc[n]):
        if g['rsi'].iloc[n] < 35 and close.iloc[n] <= g['bb_lower'].iloc[n]:
            sinyaller.append("Dip Vurusu")

    if pd.notna(g['bb_upper'].iloc[n]) and pd.notna(g['bb_lower'].iloc[n]):
        bb_width = g['bb_upper'] - g['bb_lower']
        bb_ort = bb_width.rolling(20).mean()
        if pd.notna(bb_width.iloc[n]) and pd.notna(bb_ort.iloc[n]) and bb_ort.iloc[n] > 0:
            if bb_width.iloc[n] < bb_ort.iloc[n] * 0.7:
                sinyaller.append("Bant Sikismasi")

    if (pd.notna(g['rsi'].iloc[n]) and g['rsi'].iloc[n] > 55 and
            pd.notna(g['macd'].iloc[n]) and pd.notna(g['signal'].iloc[n]) and
            g['macd'].iloc[n] > g['signal'].iloc[n] and
            pd.notna(g['ema20'].iloc[n]) and close.iloc[n] > g['ema20'].iloc[n]):
        sinyaller.append("Guc Patlamasi")

    if (pd.notna(g['ema20'].iloc[n]) and
            close.iloc[n] > g['ema20'].iloc[n] * 0.98 and
            close.iloc[n] < g['ema20'].iloc[n] * 1.02):
        sinyaller.append("Destek Testi")

    if pd.notna(vol_ort) and vol_ort > 0 and g['volume'].iloc[n] > vol_ort * 2.5:
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
        "Yutan Boga", "Cekic", "Ters Cekic", "Sabah Yildizi",
        "Boga Harami", "3 Beyaz Asker", "MACD Al Kesisimi", "Golden Cross",
        "RSI Asiri Satim", "BB Alt Bant", "Hacim Alarmi", "Dip Vurusu", "Guc Patlamasi"
    ]
    puan = sum(1 for s in sinyaller if s in boga)
    if puan >= 5: return "Altin"
    if puan >= 3: return "Gumus"
    if puan >= 1: return "Bronz"
    return None


sonuclar = {}

for ticker in HISSELER:
    try:
        bugun_str = (simdi + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        df = yf.download(
            ticker,
            start="2023-01-01",
            end=bugun_str,
            interval="1d",
            progress=False,
            auto_adjust=True
        )
        if df is None or len(df) < 30:
            continue
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

        g         = hesapla_gosterge(df)
        sinyaller = sinyal_uret(df, g)
        seviye    = altin_seviye(sinyaller)
        ad        = ticker.replace(".IS", "")

        rsi_raw = g['rsi'].iloc[-1]
        rsi_val = None if not pd.notna(rsi_raw) else round(float(rsi_raw), 1)

        sonuclar[ad] = {
            "kapanis":        round(float(g['close'].iloc[-1]), 2),
            "rsi":            rsi_val,
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
