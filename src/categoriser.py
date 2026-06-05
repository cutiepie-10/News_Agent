import re

CATEGORY_MAP: dict[str, str] = {
    'quarterly result': 'results',
    "q1 - q4 result": 'results',
    "annual result": 'results',
    "net profit": 'results',
    'net loss': 'results',
    'revenue jumps': 'results',
    'revenue falls': 'results',
    'revenue rises': 'results',
    'ebitda': 'results',
    'pat rises': 'results',
    'pat falls': 'results',
    'beats etimate': 'results',
    'misses estimate': 'results',
    'earnings': 'results',
    'rbi': "macro",
    'repo rate': "macro",
    'inflation': "macro",
    'cpi': "macro",
    'wpi': "macro",
    "gdp": "macro",
    "iip": "macro",
    "fed rate": "macro",
    'crude oil': "macro",
    "fii": "macro",
    "dii": "macro",
    "rupee": "macro",
    "dollar index": "macro",
    "current account": "macro",
    "trade deficit": "macro",
    'forex reserve': "macro",
    'sebi': 'policy',
    "budget": 'policy',
    'government': 'policy',
    'ministry': 'policy',
    'regulation': 'policy',
    "income tax": 'policy',
    'gst': 'policy',
    'import duty': 'policy',
    "export ban": 'policy',
    'customs duty': 'policy',
    'pli scheme': 'policy',
    'disinvestment': 'policy',
    'ipo': 'ipo',
    'initial public offering': 'ipo',
    'listing': 'ipo',
    'allotment': 'ipo',
    'gmp': 'ipo',
    'subscription status': 'ipo',
    'anchor investor': 'ipo',
    "board meeting": 'corporate',
    'dividend': 'corporate',
    'buyback': 'corporate',
    'merger': 'corporate',
    'acquisition': 'corporate',
    'stake sale': 'corporate',
    'open offer': 'corporate',
    'delisting': 'corporate',
    'rights issue': 'corporate',
    'ceo': 'corporate',
    'cfo': 'corporate',
    'chairman': 'corporate',
    'managing director':  'corporate',
    'joint venture': 'corporate',
    'it sector':    'sector',
    'banking sector':    'sector',
    'pharma sector':    'sector',
    'auto sector':    'sector',
    'fmcg':    'sector',
    'metal sector':    'sector',
    'realty':    'sector',
    'infrastructure':    'sector',
    'power sector':    'sector',
    'psu bank':    'sector',
    'private bank':    'sector',
    'nbfc':    'sector',
    'oil and gas':    'sector',
    'telecom':    'sector',
    'sensex':   'market',
    'nifty':   'market',
    'market rally':   'market',
    'market crash':   'market',
    'bull run':   'market',
    'bear market':   'market',
    'circuit breaker':   'market',
    'upper circuit':   'market',
    'lower circuit':   'market',
    '52-week low':   'market',
    '52-week high': 'market',
    'market breadth':   'market'
}


def categorise(text: str) -> list[str]:
    """
    Rule-based categorisation of news articles.
    Buckets: results|macro|ipo|sector|market|policy|corporate|other
    """
    buckets: set[str] = set()
    lower_text = text.lower()
    for keyword, category in CATEGORY_MAP.items():
        pattern = rf'\b{re.escape(keyword)}\b'
        if re.search(pattern=pattern, string=lower_text):
            buckets.add(category)

    if len(buckets) == 0:
        buckets.add('other')
    return sorted(buckets)
