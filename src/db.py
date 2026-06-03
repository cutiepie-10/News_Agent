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
                SELECT source_id, display_name,source_type, poll_interval_min
                FROM news_sources
                WHERE is_active = TRUE
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
        headline, body, summary, published_at,
        ticker_tags, category, is_processed, is_filing)
        VALUES(
        %(url)s, %(content_hash)s, %(source_id)s, %(source_group)s,
        %(headline)s, %(body)s, %(summary)s,%(published_at)s,
        %(ticker_tags)s,%(category)s, %(is_processed)s, %(is_filing)s)
        ON CONFLICT DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as curr:
            for n in news:
                n['ticker_tags']= n.get('ticker_tags') or []
                curr.execute(sql, n)
                inserted= curr.rowcount
        conn.commit()

    logger.info('Added %d new rows to raws_news DB', inserted)
    return inserted
