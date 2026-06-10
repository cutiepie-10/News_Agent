import logging
import hashlib
from datetime import datetime, timedelta,timezone
from time import mktime
import requests
import feedparser
from src.categoriser import categorise
from src.ticker_tagger import extract_ticker_tags
from src.config import USER_AGENT

logger = logging.getLogger(__name__)

def fetch_rss(source_url: str)->list[dict]:
    """
    Fetches the .xml or .rss document for a particular source.
    Then parses the document and returns the list of dict of fresh news. 
    """
    headers = {
        "User-Agent": USER_AGENT,
    }
    respo = requests.get(source_url, headers=headers, timeout=5)
    if (respo.status_code != 200):
        logger.error('Error occured fetching raws news from "%s" with status code of %d',
                     source_url, respo.status_code)
    parsed = feedparser.parse(respo.text)
    logger.info('Parsed the rss file from "%s"',source_url)
    return parsed.entries


def parse_raw_news(news: dict, source_id: str) -> dict:
    """
    Parses the news given by the rss feed into the db ingestable form.
    It returns None for the news which are older than 12 hours.
    """

    pub_time = datetime.fromtimestamp(mktime(news['published_parsed']),tz= timezone.utc)
    if (datetime.now(timezone.utc) > pub_time+timedelta(hours=12)):
        return None
    headline = news['title']
    if not headline:
        return None
    content_hash = hashlib.md5(headline.encode('utf-8')).hexdigest()
    summary = news['summary']
    ticker_tags = extract_ticker_tags(headline+' '+summary)
    category = categorise(headline+' '+summary)
    return {
        "url": news.link,
        "content_hash": content_hash,
        "source_id": source_id,
        "source_group": "rss",
        "headline": headline,
        "summary": summary,
        "published_at": pub_time,
        "ticker_tags": ticker_tags,
        "category": category
    }
