import sys
from datetime import datetime, timezone, timedelta
from src.db import (
    fetch_active_sources,
    get_volume, get_last_successfull_poll,
    get_duplicate_count,
    get_ticker_tag_pct
)


NOW = datetime.now(timezone.utc)

PASS = '✅ PASS'
FAIL = '❌ FAIL'


def check_volume():
    """Checks the volume of news from each active source."""
    sources = fetch_active_sources()
    all_ok = True
    for source in sources:
        count = get_volume(
            source_id=source['source_id'], source_type=source['source_type'])
        ok = count >= 5
        print(f'{PASS if ok else FAIL} @{source['source_id']} {count} news')
        if not ok:
            all_ok = False
    return all_ok


def check_coverage():
    """All active sources must have a successful poll in last 45 mins."""
    sources = fetch_active_sources()
    all_ok = True
    for source in sources:
        source_id = source['source_id']
        last = get_last_successfull_poll(source_id)
        if last and (NOW-last) < timedelta(minutes=45):
            mins = int((NOW-last).total_seconds()/60)
            print(f'{PASS} @{source_id} last poll {mins}m ago')
        else:
            lag = "never" if not last else f"{int((NOW-last).total_seconds()/60)}m ago"
            print(f"  {FAIL}  @{source_id:<20} last poll {lag}")
            all_ok = False
        return all_ok


def check_no_duplicates():
    """
    Checks for the duplicates in the raw_news table
    """
    print("\n── Duplicate Check ──")
    dupes = get_duplicate_count()
    ok = dupes == 0
    print(f"  {PASS if ok else FAIL}  Duplicate news: {dupes}")
    return ok


def check_ticker_tagging():
    """
    Checks for the ticker tag percentage in the nse_filings and the news
    """
    print("\n── Ticker Tagging Rate (last 24h) ──")

    pct = get_ticker_tag_pct('rss')
    ok = pct >= 30
    print(f"  {PASS if ok else FAIL}  {pct}% news ticker-tagged (need ≥30%)")
    pct = get_ticker_tag_pct('nse')
    print(f"  {PASS if ok else FAIL}  {pct}% nse_filings ticker-tagged (need ≥30%)")
    return ok

if __name__=='main':
    results = [check_coverage(),
    check_volume(),
    check_no_duplicates(),
    check_ticker_tagging()
    ]
    print(f'\n {'='*44}')
    if all(results):
        print("✅  ALL CHECKS PASSED — Week 3 complete")
        sys.exit(0)
    else:
        print("❌  SOME CHECKS FAILED — fix before marking complete")
        sys.exit(1)
