--TABLE 1: news sources
-- This table stores all the news sources, their type and whether they are active or not.
CREATE TABLE IF NOT EXISTS news_sources (
    source_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    url TEXT ,
    source_type TEXT NOT NULL,
    poll_interval_min INT DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    paused_at TIMESTAMPTZ
);
INSERT INTO news_sources (
    source_id, display_name, url,
    source_type, poll_interval_min
)
VALUES
(
    'ndtv_profit', ' NDTV Profit',
    'https://feeds.feedburner.com/ndtvprofit-latest',
    'rss', 10
),
(
    'livemint', 'Livemint',
    'https://www.livemint.com/rss/markets',
    'rss', 5
),
(
    'bussiness_standards', ' Bussiness Standard',
    'https://www.business-standard.com/rss/latest.rss',
    'rss', 5
),
(
    'et_money', 'ET Money',
    'https://bfsi.economictimes.indiatimes.com/rss/topstories',
    'rss', 5
),
(
    'nse_announcements', 'NSE announcements',
    NULL,
    'nse_api', 5
),
(
    'nse_calendar', 'NSE Events Calendar',
    NULL,
    'nse_api', 30
),
(
    'nse_board_meeting', 'NSE Board Meeting',
    NULL,
    'nse_api',30
);

--TABLE 2: raw_news 
-- Stores all the raw news from all different sources. 
-- It should not contain any duplicate news

CREATE EXTENSION pgcrypto; -- loads gen_random_uuid()

CREATE TABLE IF NOT EXISTS raw_news (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT UNIQUE NOT NULL,
    content_hash TEXT UNIQUE NOT NULL,
    source_id TEXT REFERENCES news_sources (source_id),
    source_group TEXT NOT NULL,
    headline TEXT NOT NULL,
    body TEXT,
    summary TEXT,
    published_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    ticker_tags TEXT [],
    category TEXT [], -- results|macro|policy|ipo|corporate|sector|market|other
    is_processed BOOLEAN DEFAULT FALSE,
    is_filing BOOLEAN DEFAULT FALSE
);


CREATE INDEX IF NOT EXISTS idx_news_source_time
ON raw_news (source_id, ingested_at DESC);

CREATE INDEX IF NOT EXISTS idx_news_unprocessed
ON raw_news (is_processed) WHERE is_processed = FALSE;

CREATE INDEX IF NOT EXISTS idx_news_tickers
ON raw_news USING gin (ticker_tags);

CREATE INDEX IF NOT EXISTS idx_news_category
ON raw_news USING gin (category);


--TABLE 3: nse_filings
CREATE TABLE nse_filings (
    filing_id TEXT PRIMARY KEY,--md5(symbol|subject|date)= stable dedup
    symbol TEXT NOT NULL,
    company_name TEXT,
    filing_type TEXT,
    subject TEXT,
    description TEXT,
    exchange TEXT DEFAULT 'NSE',
    filing_date TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    pdf_url TEXT,
    is_processed BOOLEAN DEFAULT FALSE
);


CREATE INDEX IF NOT EXISTS idx_filing_symbol
ON nse_filings (symbol, filing_date DESC);

CREATE INDEX IF NOT EXISTS idx_type_time
ON nse_filings (filing_type, filing_date DESC);


--TABLE 4: poll_logs
--Stores the result of polls.
--One row per poll. Used to detect dead sources.
CREATE TABLE poll_logs (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL,
    polled_at TIMESTAMPTZ DEFAULT NOW(),
    items_fetched INT DEFAULT 0,
    items_new INT DEFAULT 0,
    success BOOLEAN,
    error_message TEXT
);
CREATE INDEX IF NOT EXISTS idx_poll_log_source_time
ON poll_logs (source_id, polled_at DESC);