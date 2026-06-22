import re

CATEGORY_MAP: dict[str, list[str]] = {
    'results': [
        'quarterly result', "q1 - q4 result", "annual result", "net profit", 'net loss',
        'revenue jumps', 'revenue falls', 'revenue rises', 'ebitda', 'pat rises', 'pat falls',
        'beats etimate', 'misses estimate', 'earnings', 'expects revenue', 'operational revenue',
        'pat', 'pbt', 'operating profit', 'topline', 'bottomline', 'eps', 'earning per share',
        'revenue growth', 'loss widens', 'turnaround', 'guidance', 'margins contract',
        'beats street', 'sales surge', 'profit jumps', 'profit slips', 'margins expand',
        'financial metrics', 'expects volume growth', 'growth forecast', 'outperformed'
    ],
    'macro': [
        'rbi', 'repo rate', 'inflation', 'cpi', 'wpi', "gdp", "iip", "fed rate", 'crude oil',
        "fii", "dii", "rupee", "dollar index", "current account", "trade deficit", 'forex reserve',
        'monetary policy', 'mifor', 'sofr', 'basis points', 'bps', 'rate hike', 'rate cut',
        'hawkish', 'dovish', 'bond yield', 'treasury yield', 'brent crude', 'forex inflow',
        'fpi', 'foreign institutional investors', 'currency depreciation', 'rupee slides',
        'fiscal deficit', 'g7 summit', 'g20 economic', 'macroeconomic indicators',
        'rupee strengthens',  'export contraction',
    ],
    'policy': [
        'sebi', "budget", 'government', 'ministry', 'regulation', "income tax",
        'gst', 'import duty', "export ban", 'customs duty', 'pli scheme', 'disinvestment',
        'trade deal', 'fta', 'export duty', 'g7',  'g20', 'tariffs', 'bilateral talks',
        'free trade agreement', 'anti-dumping duty', 'export incentive',  'insolvency',
        'ibc code', 'bankruptcy proceedings', 'cabinet approves', 'gazette notification',
        'competition commission', 'regulatory filing', 'compliance hurdle', 'irdai',
        'subsidy', 'fema regulation', 'nclt',  'cci probe', 'trai guidelines',
    ],

    'ipo': [
        'ipo', 'initial public offering', 'listing', 'allotment', 'gmp',
        'subscription status', 'anchor investor', 'qualified institutional buyers',
        'grey market premium', 'listing gain', 'listing pop', 'red herring prospectus', 'drhp',
        'rhp filing', 'public issue', 'book building', 'oversubscribed', 'unlisted shares',
        'qib portion', 'retail bidding', 'ipo bound', 'market debut',  'offer price band'
    ],
    'corporate': [
        "board meeting", 'dividend', 'buyback', 'merger', 'acquisition', 'stake sale', 'open offer',
        'delisting', 'rights issue', 'ceo', 'cfo', 'chairman', 'managing director', 'joint venture',
        'interim dividend', 'special dividend', 'ex-dividend', 'bonus shares', 'stock split',
        'share consolidation', 'share repurchase', 'promoter buying', 'insider trading filing',
        'block deal', 'bulk deal', 'promoter pledge', 'pledged shares revoked', 'takeover',
        'spin-off', 'divestment', 'fundraising', 'ncds', 'preferential allotment', 'demerger',
        'qip', 'executive transition', 'appoints ceo', 'cfo resigns', 'order win',
        'secures contract', 'qualified institutional placement'
    ],
    'sector': [
        'it sector', 'banking sector', 'pharma sector', 'auto sector', 'fmcg',
        'metal sector', 'realty', 'infrastructure', 'power sector', 'psu bank', 'private bank',
        'nbfc', 'oil and gas', 'telecom', 'consumer durables', 'green energy', 'ev segment',
        'electric vehicles', 'renewable energy', 'specialty chemicals', 'defense manufacturing',
        'real estate demand', 'auto dispatches', 'telecom subscriber data', 'microfinance',
        'cement volumes', 'steel prices', 'agrochemicals', 'logistics sector', 'semiconductor',
        'aviation sector', 'hospitality industry'
    ],
    'market': [
        'sensex', 'nifty', 'market rally', 'market crash', 'bull run', 'bear market',
        'circuit breaker', 'upper circuit', 'lower circuit', '52-week low', '52-week high',
        'market breadth', 'nifty 50', 'bank nifty', 'midcap index', 'smallcap index', 
        'profit booking', 'short covering', 'long unwinding', 'correction', 'oversold territory',
        'overbought', 'market capitalization', 'm-cap', 'market turnover', 
        'opening bell', 'closing trade', 'pre-market session', 'trade-to-trade', 'asm framework',
        'volatility index', 'advances declines ratio', 'india vix'

    ]
}


def categorise(text: str) -> list[str]:
    """
    Rule-based categorisation of news articles.
    Buckets: results|macro|ipo|sector|market|policy|corporate|other
    """
    buckets: set[str] = set()
    lower_text = text.lower()
    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            if re.search(pattern=pattern, string=lower_text):
                buckets.add(category)
                break
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
    """
    Categorises the nse filings(rule based)
    """
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
