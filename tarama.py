import json
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

TR_TZ = pytz.timezone('Europe/Istanbul')
simdi = datetime.now(TR_TZ)
saat = simdi.hour
dakika = simdi.minute

# 18:00 ve sonrası = günlük tarama, öncesi = 4h tarama
if saat >= 18:
    PERIYOT = "1d"
else:
    PERIYOT = "4h"

# Borsa saatleri dışındaysa 4h taramayı atla
if PERIYOT == "4h":
    if not (9 <= saat < 18):
        print(f"Borsa saatleri dışında ({simdi.strftime('%H:%M')}), 4h tarama atlanıyor.")
        exit(0)

print(f"Tarama başlıyor... {simdi.strftime('%d.%m.%Y %H:%M')} | Periyot: {PERIYOT}")

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


def bist_4h_olustur(df_1h):
    if df_1h.empty:
        return pd.DataFrame()
    if df_1h.index.tz is None:
        df_1h.index = df_1h.index.tz_localize('UTC')
    else:
        df_1h.index = df_1h.index.tz_convert('UTC')
    # offset='6h' → 06:00 UTC = 09:00 TR başlangıcı
    df_4h = df_1h.resample('4h', offset='6h').agg(
        Open=('Open', 'first'),
        High=('High', 'max'),
        Low=('Low', 'min'),
        Close=('Close', 'last'),
        Volume=('Volume', 'sum')
    ).dropna(subset=['Open', 'Close'])
    simdi_utc = pd.Timestamp.now(tz='UTC')
    df_4h = df_4h[df_4h.index + pd.Timedelta(hours=4) <= simdi_utc]
    df_4h = df_4h[df_4h['Volume'] > 0]
    return df_4h.reset_index(drop=True)


def hesapla_gosterge(df):
    close  = df['Close']
    high   = df['High']
    low    = df['Low']
    volume = df['Volume']
    ema20  = close.ewm(span=20).mean()
    ema50  = close.ewm(span=50).mean()
    sma200 = close.rolling(200).mean()
    delta  = close.diff()
    gain   = delta.clip(lower=0).rolling(14).mean()
    loss   = (-delta.clip(upper=0)).rolling(14).mean()
    rs     = gain / loss
    rsi    = 100 - (100 / (1 + rs))
    ema12  = close.ewm(span=12).mean()
    ema26  = close.ewm(span=26).mean()
    macd   = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    sma20    = close.rolling(20).mean()
    std20    = close.rolling(20).std()
    bb_lower = sma20 - 2 * std20
    bb_upper = sma20 + 2 * std20
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    return {
        'close': close, 'high': high, 'low': low, 'volume': volume,
        'ema20': ema20, 'ema50': ema50, 'sma200': sma200,
        'rsi': rsi, 'macd': macd, 'signal': signal,
        'bb_lower': bb_lower, 'bb_upper': bb_upper, 'atr': atr
    }


def sinyal_uret(df, g):
    sinyaller = []
    close = g['close']
    n = -1
    if len(close) < 3:
        return sinyaller

    avg_vol = g['volume'].rolling(20).mean().iloc[n]

    if g['macd'].iloc[n] > g['signal'].iloc[n] and g['macd'].iloc[n-1] <= g['signal'].iloc[n-1]:
        sinyaller.append("MACD Al Kesisimi")
    if g['macd'].iloc[n] > g['signal'].iloc[n]:
        sinyaller.append("MACD Pozitif")
    if close.iloc[n] > g['ema20'].iloc[n]:
        sinyaller.append("Fiyat EMA20 Ustunde")
    if g['ema20'].iloc[n] > g['ema50'].iloc[n]:
        sinyaller.append("EMA20 > EMA50")
    if close.iloc[n] > g['sma200'].iloc[n]:
        sinyaller.append("Fiyat SMA200 Ustunde")
    if g['rsi'].iloc[n] < 35:
        sinyaller.append("RSI Asiri Satim")
    if close.iloc[n] <= g['bb_lower'].iloc[n]:
        sinyaller.append("BB Alt Bant")
    if g['ema20'].iloc[n-1] <= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] > g['ema50'].iloc[n]:
        sinyaller.append("Golden Cross")
    if g['ema20'].iloc[n-1] >= g['ema50'].iloc[n-1] and g['ema20'].iloc[n] < g['ema50'].iloc[n]:
        sinyaller.append("Death Cross")
    if pd.notna(avg_vol) and avg_vol > 0 and g['volume'].iloc[n] > avg_vol * 2:
        sinyaller.append("Hacim Alarmi")

    o  = df['Open'].iloc[n];   h  = df['High'].iloc[n]
    l  = df['Low'].iloc[n];    c  = df['Close'].iloc[n]
    o1 = df['Open'].iloc[n-1]; h1 = df['High'].iloc[n-1]
    l1 = df['Low'].iloc[n-1];  c1 = df['Close'].iloc[n-1]
    body  = abs(c  - o)
    body1 = abs(c1 - o1)
    range_ = h - l

    if body > 0 and range_ > 0:
        lower_shadow = min(o, c) - l
        upper_shadow = h - max(o, c)

        if lower_shadow >= body * 2 and upper_shadow <= body * 0.5:
            sinyaller.append("Cekic")
        if upper_shadow >= body * 2 and lower_shadow <= body * 0.5:
            sinyaller.append("Ters Cekic")
        if (c1 < o1 and c > o and o < c1 and c > o1):
            sinyaller.append("Yutan Boga")
        if (c1 < o1 and c > o and o > c1 and c < o1 and body < body1 * 0.5):
            sinyaller.append("Boga Harami")

        if len(df) >= 3:
            o2    = df['Open'].iloc[n-2]
            c2    = df['Close'].iloc[n-2]
            body2 = abs(c2 - o2)
            if (c2 < o2 and body1 < body2 * 0.3 and c > o and c > (o2 + c2) / 2):
                sinyaller.append("Sabah Yildizi")
            if (c2 > o2 and c1 > o1 and c > o and
                c1 > c2 and c > c1 and o1 > o2 and o > o1):
                sinyaller.append("3 Beyaz Asker")

    if g['rsi'].iloc[n] < 35 and close.iloc[n] <= g['bb_lower'].iloc[n]:
        sinyaller.append("Dip Vurusu")
    bb_width = (g['bb_upper'] - g['bb_lower']) / g['bb_lower'].rolling(20).mean()
    if pd.notna(bb_width.iloc[n]) and pd.notna(bb_width.rolling(20).mean().iloc[n]):
        if bb_width.iloc[n] < bb_width.rolling(20).mean().iloc[n] * 0.7:
            sinyaller.append("Bant Sikismasi")
    if g['rsi'].iloc[n] > 55 and g['macd'].iloc[n] > g['signal'].iloc[n] and close.iloc[n] > g['ema20'].iloc[n]:
        sinyaller.append("Guc Patlamasi")
    if close.iloc[n] > g['ema20'].iloc[n] * 0.98 and close.iloc[n] < g['ema20'].iloc[n] * 1.02:
        sinyaller.append("Destek Testi")
    if pd.notna(avg_vol) and avg_vol > 0 and g['volume'].iloc[n] > avg_vol * 2.5:
        sinyaller.append("Hacim Bombasi")
    if (close.iloc[n] > g['ema20'].iloc[n] and
        g['ema20'].iloc[n] > g['ema50'].iloc[n] and
        g['macd'].iloc[n] > g['signal'].iloc[n]):
        sinyaller.append("Trend Uyumu")

    return sinyaller


def altin_seviye(sinyaller):
    boga = [
        "Yutan Boga", "Cekic", "Ters Cekic", "Sabah Yildizi",
        "Boga Harami", "3 Beyaz Asker",
        "MACD Al Kesisimi", "Golden Cross",
        "RSI Asiri Satim", "BB Alt Bant",
        "Hacim Alarmi", "Dip Vurusu", "Guc Patlamasi"
    ]
    puan = sum(1 for s in sinyaller if s in boga)
    if puan >= 5: return "Altin"
    if puan >= 3: return "Gumus"
    if puan >= 1: return "Bronz"
    return None


sonuclar = {}

for ticker in HISSELER:
    try:
        if PERIYOT == "1d":
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
        else:
            df_1h = yf.download(
                ticker,
                period="60d",
                interval="1h",
                progress=False,
                auto_adjust=True
            )
            if df_1h is None or len(df_1h) < 20:
                continue
            df_1h.columns = [c[0] if isinstance(c, tuple) else c for c in df_1h.columns]
            df = bist_4h_olustur(df_1h)
            if df is None or len(df) < 20:
                continue

        g         = hesapla_gosterge(df)
        sinyaller = sinyal_uret(df, g)
        seviye    = altin_seviye(sinyaller)
        ad        = ticker.replace(".IS", "")

        sonuclar[ad] = {
            "kapanis":        round(float(g['close'].iloc[-1]), 2),
            "rsi":            round(float(g['rsi'].iloc[-1]),   1),
            "sinyaller":      sinyaller,
            "altin":          seviye,
            "dip_vurusu":     "Dip Vurusu"     in sinyaller,
            "bant_sikismasi": "Bant Sikismasi"  in sinyaller,
            "guc_patlamasi":  "Guc Patlamasi"   in sinyaller,
            "destek_testi":   "Destek Testi"    in sinyaller,
            "hacim_bombasi":  "Hacim Bombasi"   in sinyaller,
            "trend_uyumu":    "Trend Uyumu"     in sinyaller,
        }

    except Exception as e:
        print(f"Hata {ticker}: {e}")

cikti = {
    "tarih":    simdi.strftime("%d.%m.%Y %H:%M"),
    "periyot":  "gunluk" if PERIYOT == "1d" else "4h",
    "hisseler": sonuclar
}

dosya_adi = "sonuclar4h.json" if PERIYOT == "4h" else "sonuclar.json"
with open(dosya_adi, "w", encoding="utf-8") as f:
    json.dump(cikti, f, ensure_ascii=False, indent=2)

print(f"Tamamlandı! {len(sonuclar)} hisse işlendi. → {dosya_adi}")
