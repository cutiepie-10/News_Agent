import pytest
from src.rss_poller import fetch_rss, parse_raw_news
URL ="https://www.business-standard.com/rss/latest.rss"
SOURCE_ID= "Bussiness standard"

def test_rss_parser():
    rss = fetch_rss(source_url=URL)
    assert len(rss)>=10
    for r in rss:
        parse_raw_news(r,SOURCE_ID)
