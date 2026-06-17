import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config import STAGGER_SECONDS, SOURCE_RELOAD_INTERVAL_MIN
from src.db import fetch_active_sources, upsert_raw_news, log_poll, upsert_nse_filing
from src.rss_poller import fetch_rss, parse_raw_news
from src.nse_poller import (
    fetch_nse_announcements, parse_nse_announcement,
    fetch_nse_events, parse_nse_event, fetch_nse_board_meetings,
    parse_nse_board_meeting
)

logger = logging.getLogger(__name__)

_registered_sources: set[str] = set()


def poll(source: dict):
    """
    Polls the results from source passed.
    """
    try:
        if source['source_type'] == 'rss':
            news = fetch_rss(source['url'])
            parsed_news = []
            for n in news:
                parsed = parse_raw_news(n, source_id=source['source_id'])
                if parsed is not None:
                    parsed_news.append(parsed)
            items_new = upsert_raw_news(parsed_news)
            log_poll(source_id=source['source_id'], items_fetched=len(parsed_news),
                     items_new=items_new, success=True, error="")

            logger.info('@%s: %d new | %d dupes skipped',
                        source['display_name'], items_new, (len(parsed_news)-items_new))
        else:
            parsed = []
            if source['source_id'].find('announcements'):
                announcements = fetch_nse_announcements()
                parsed = [parse_nse_announcement(ann) for ann in announcements]
            if source['source_id'].find('calendar'):
                events = fetch_nse_events()
                parsed = [parse_nse_event(event) for event in events]
            if source['source_id'].find('board_meeeting'):
                bms = fetch_nse_board_meetings()
                parsed = [parse_nse_board_meeting(bm) for bm in bms]
            parsed = [p for p in parsed if p]
            items_new = upsert_nse_filing(parsed)
            log_poll(source_id=source['source_id'], items_fetched=len(parsed),
                     items_new=items_new, success=True)
            logger.info('@%s: %d new | %d dupes skipped',
                        source['display_name'], items_new, (len(parsed)-items_new))
    except Exception as e:
        logger.error('Error occured while polling @%s:%s',
                     source['display_name'], e, exc_info=True)
        log_poll(source_id=source['source_id'], items_fetched=0,
                 items_new=0, success=False, error=str(e))


def sync_sources(scheduler: BlockingScheduler):
    """
    Syncs all the active and removes the job of inactive sources.
    """
    global _registered_sources

    active_sources = fetch_active_sources()
    active_set = {s['source_id']for s in active_sources}
    for i, source in enumerate(active_sources):
        source_id = source['source_id']
        interval = source['poll_interval_min']
        job_id = f'poll_{source_id}'

        if source_id not in _registered_sources:
            start_time = datetime.now(timezone.utc)+timedelta(
                seconds=i*STAGGER_SECONDS
            )
            scheduler.add_job(
                poll,
                id=job_id,
                trigger=IntervalTrigger(minutes=interval),
                args=[source],
                name=f"Poll @{source_id}",
                next_run_time=start_time,
                misfire_grace_time=20,
                replace_existing=True
            )
            logger.info('Scheduled a new job: Poll @%s every %d minutes',
                        source_id, interval)
            _registered_sources.add(source_id)
    removed_sources = _registered_sources - active_set
    for source in removed_sources:
        job_id = f'poll_{source}'
        scheduler.remove_job(job_id)
        logger.info('Removed job: @%s (paused or deleted from DB)', source)
    _registered_sources = active_set


def start():
    """
    It starts the scheduler, adds the job to sync sources.
    """
    scheduler = BlockingScheduler(timezone='Asia/Kolkata')
    sync_sources(scheduler=scheduler)

    scheduler.add_job(
        sync_sources,
        trigger=IntervalTrigger(minutes=SOURCE_RELOAD_INTERVAL_MIN),
        args=[scheduler],
        id="sync_sources",
        name="Sync active sources from DB"
    )
    logger.info("Scheduler started. Active sources are sync in every %d min",
                SOURCE_RELOAD_INTERVAL_MIN)
    scheduler.start()
