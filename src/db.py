import logging
import psycopg2
import psycopg2.extras

from src.config import DATABASE_URL

logger = logging.getLogger(__name__)

def get_connection():
    """
    Gives the connection to the database through DATABASE_URL\
    """
    return psycopg2.connect(dsn = DATABASE_URL)

def fetch_active_sources()->list[dict]:
    """
    Reads all the active sources from the DB.
    It is called in every RELOAD_INTERVAL_MIN.
    It returns a list of dict active sources:{source_id}, {display_name}, {poll_interval_min}
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory= psycopg2.extras.RealDictCursor) as curr:
            curr.execute("""
                SELECT source_id, display_name,source_type, poll_interval_min, url
                FROM news_sources
                WHERE is_active
                ORDER BY source_id;
            """)
            res= curr.fetchall()
    sources= [dict(r) for r in res]
    logger.info("Loaded %d active sources",len(sources))
    return sources

def upsert_raw_news(news:list[dict])->int :
    """
    Insert news into the raw_news DB.
    Returns the count of new rows only.
    DOES nothing ON CONFLICT -- dedupes
    """
    if not news:
        return 0
    sql ="""
        INSERT INTO raw_news(
        url,content_hash, source_id, source_group,
        headline, summary, published_at,
        ticker_tags, category)
        VALUES(
        %(url)s, %(content_hash)s, %(source_id)s, %(source_group)s,
        %(headline)s, %(summary)s,%(published_at)s,
        %(ticker_tags)s,%(category)s)
        ON CONFLICT DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as curr:
            for n in news:
                n['ticker_tags']= n.get('ticker_tags') or []
                n['category'] = n.get('category') or ['other']
                curr.execute(sql, n)
                inserted= curr.rowcount
        conn.commit()

    logger.info('Added %d new rows to raws_news DB', inserted)
    return inserted


def log_poll(source_id:str, items_fetched:int,
    items_new:int, success:bool, error:str = ""):
    """One row per source after every poll attempt"""
    sql ="""
    INSERT INTO poll_logs(
    source_id, items_fetched,
    items_new , success, error_message)
    VALUES(%s, %s , %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as curr:
            curr.execute(sql,(source_id, items_fetched, items_new, success, error))
        conn.commit()

def upsert_nse_filing(filings:list[dict])->int:
    if not filings:
        return 0
    sql="""
    INSERT INTO nse_filings(
    filing_id, company_name, filing_type,
    symbol, subject, description,
    filing_date, pdf_url)
    VALUES(
    %(filing_id)s, %(company_name)s,%(filing_type)s,
    %(symbol)s, %(subject)s, %(description)s,
    %(filing_date)s, %(pdf_url)s)
    ON CONFLICT DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as curr:
            for filing in filings:
                curr.execute(sql, filing)
                inserted= curr.rowcount
            logger.info('Added %d new rows to nse_filings DB',inserted)
            return inserted
