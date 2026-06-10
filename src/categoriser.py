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


FILING_TYPE_MAP = {
    'results': [
        'financial results', 'audited financials',
        'unaudited financials', 'quarterly results', 'earnings',
        'limited review report', 'balance sheet', 'profit and loss'
    ],
    'agm': [
        'agm notice', 'annual general meeting', 'egm notice',
        'extraordinary general meeting', 'voting results',
        'scrutinizer report', 'annual report', 'book closure agm'
    ],
    'board_meeting': [
        'board meeting intimation', 'prior intimation', 'outcome of board meeting',
        'meeting to be held', 'board to consider',
        'postponement of board meeting'
    ],
    'buyback': [
        'share buyback', 'buyback of equity',
        'public announcement buyback',
        'letter of offer buyback', 'capital reduction',
        'tender offer'],
    'dividend': [
        'interim dividend', 'final dividend', 'special dividend',
        'dividend declaration', 'dividend recommendation',
        'record date dividend'
    ],
    'management_changes': [
        'appointment of', 'resignation of', 'cessation of',
        'change in kmp', 'change in directors', 'appointment of auditor',
        'statutory auditor resignation', 'managing director', 'ceo change', 'cfo change'
    ],
    'fundraising': [
        'allotment of shares', 'rights issue', 'bonus issue',
        'preferential allotment', 'qip', 'qualified institutional placement',
        'issue of ncd', 'non-convertible debentures', 'commercial paper',
        'esop allotment', 'fund raising'
    ],
    'm_and_a': [
        'acquisition', 'amalgamation', 'scheme of arrangement',
        'demerger', 'joint venture', 'stake sale',
        'slump sale', 'business transfer agreement', 'takeover'
    ],
    'credit_ratings': [
        'credit rating', 'crisil', 'icra', 'care rating',
        'india ratings', 'downgrade', 'upgrade', 'rating reaffirmation'
    ],
    'legal_and_regulatory': [
        'penalty', 'sebi order', 'litigation', 'gst notice',
        'tax demand', 'show cause notice', 'cbi',
        'enforcement directorate', 'adjudication', 'sat order'
    ],
    'business_updates': [
        'order win', 'contract awarded', 'mou signed',
        'commercial production', 'plant shutdown', 'product launch',
        'business update', 'capacity expansion'
    ],
    'insider_trading': ['sast regulation', 'pit regulation', 'insider trading',
                        'promoter pledge', 'revocation of pledge', 'shareholding pattern',
                        'encumbrance', 'continual disclosure'
                        ],
    'compliance_and_governance': [
        'brsr report', 'business responsibility',
        'corporate governance report', 'investor grievance', 'secretarial compliance',
        'loss of share certificate', 'duplicate share certificate', 'newspaper publication'
    ]
}


def categorise_filing(text: str) -> str:
    filing_type: set[str] = set()
    lower_text = text.lower()
    for t, keywords in FILING_TYPE_MAP.items():
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            if re.search(pattern=pattern, string=lower_text):
                filing_type.add(t)
                break
    if filing_type:
        return filing_type.pop()
    return ""
