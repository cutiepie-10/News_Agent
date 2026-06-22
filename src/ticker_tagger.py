import re

SYMBOL_MAP: dict[str, str] = {
    # ── Indices ─────────────────────────────────────────────
    "nifty":          "NIFTY",
    "nifty50":        "NIFTY",
    "nifty 50":       "NIFTY",
    "banknifty":      "BANKNIFTY",
    "bank nifty":     "BANKNIFTY",
    "finnifty":       "FINNIFTY",
    "fin nifty":      "FINNIFTY",
    "midcapnifty":    "MIDCPNIFTY",
    "midcap nifty":   "MIDCPNIFTY",
    "sensex":         "SENSEX",

    # ── Large caps ──────────────────────────────────────────
    "reliance":       "RELIANCE",
    "ril":            "RELIANCE",
    "tcs":            "TCS",
    "infosys":        "INFY",
    "infy":           "INFY",
    "hdfc":           "HDFCBANK",
    "hdfc bank":      "HDFCBANK",
    "hdfcbank":       "HDFCBANK",
    "icici":          "ICICIBANK",
    "icici bank":     "ICICIBANK",
    "icicibank":      "ICICIBANK",
    "itc":            "ITC",
    "wipro":          "WIPRO",
    "bajaj finance":  "BAJFINANCE",
    "bajfinance":     "BAJFINANCE",
    "sbi":            "SBIN",
    "state bank":     "SBIN",
    "adani":          "ADANIENT",
    "tatamotors":     "TATAMOTORS",
    "tata motors":    "TATAMOTORS",
    "maruti":         "MARUTI",
    "asian paint":    "ASIANPAINT",
    "asianpaint":     "ASIANPAINT",
    "hcl":            "HCLTECH",
    "hcltech":        "HCLTECH",
    "axis bank":      "AXISBANK",
    "axisbank":       "AXISBANK",
    "kotak":          "KOTAKBANK",
    "kotakbank":      "KOTAKBANK",
    "ongc":           "ONGC",
    "ntpc":           "NTPC",
    "powergrid":      "POWERGRID",
    "power grid":     "POWERGRID",
    "sun pharma":     "SUNPHARMA",
    "sunpharma":      "SUNPHARMA",
    "dr reddy":       "DRREDDY",
    "drreddy":        "DRREDDY",
    "l&t":            "LT",
    "larsen":         "LT",
    "coal india":     "COALINDIA",
    "coalindia":      "COALINDIA",
    "bajaj auto":     "BAJAJ-AUTO",
    "bajaj fin serv": "BAJAJFINSV",
    "bajajfinsv":     "BAJAJFINSV",
    "titan":          "TITAN",
    "tata steel":     "TATASTEEL",
    "tatasteel":      "TATASTEEL",
    "hindalco":       "HINDALCO",
    "jswsteel":       "JSWSTEEL",
    "jsw steel":      "JSWSTEEL",
    "ultratech":      "ULTRACEMCO",
    "ultracemco":     "ULTRACEMCO",
    "nestle":         "NESTLEIND",
    "nestleind":      "NESTLEIND",
    "cipla":          "CIPLA",
    "divis":          "DIVISLAB",
    "divislab":       "DIVISLAB",
    "tata consumer":  "TATACONSUM",
    "tataconsum":     "TATACONSUM",
    "britannia":      "BRITANNIA",
    "eicher":         "EICHERMOT",
    "eichermot":      "EICHERMOT",
    "hero moto":      "HEROMOTOCO",
    "heromotoco":     "HEROMOTOCO",
    "m&m":            "M&M",
    "mahindra":       "M&M",
    "apollo hosp":    "APOLLOHOSP",
    "apollohosp":     "APOLLOHOSP",
    "tech mahindra":  "TECHM",
    "techm":          "TECHM",
    "indusind":       "INDUSINDBK",
    "indusindbk":     "INDUSINDBK",
    "grasim":         "GRASIM",
    "shriram":        "SHRIRAMFIN",
    "shriramfin":     "SHRIRAMFIN",
    'hinduja':        'HGS',
    # ── Add more here as you observe
}


def extract_ticker_tags(text: str) -> list[str]:
    """
    Extract the ticker tags from the news headline and summary.
    Returns the extracted ticker tags in a list.
    """
    found: set[str] = set()
    text_lower = text.lower()
    for keyword, ticker in SYMBOL_MAP.items():
        pattern = rf"\b{re.escape(keyword)}\b"
        if re.search(pattern=pattern, string=text_lower):
            found.add(ticker)

    return sorted(found)
