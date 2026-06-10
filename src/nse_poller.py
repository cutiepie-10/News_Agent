import logging
import hashlib
from pathlib import Path
from nse import NSE
from src.categoriser import categorise_filing

logger = logging.getLogger(__name__)
def fetch_nse_announcements():
    DIR= Path(__file__).parent
    with NSE(download_folder= DIR,server= False) as nse:
        announcements = nse.announcements()
        return announcements
def fetch_nse_events()->list[dict]:
    DIR = Path(__file__).parent
    with NSE(download_folder= DIR, server= False) as nse:
        events= nse.actions()
        return events
def fetch_nse_board_meetings()->list[dict]:
    DIR = Path(__file__).parent
    with NSE(download_folder= DIR, server=False) as nse:
        board_meetings = nse.boardMeetings()
        return board_meetings
def parse_nse_announcement(ann:dict)->dict:
    subject= ann['desc']
    symbol = ann['symbol']
    filing_date= ann['an_dt']
    description = ann['attchmntText']
    filing_id = symbol+description+filing_date
    filing_id= hashlib.md5(filing_id.encode('utf-8')).hexdigest()
    filing_type = categorise_filing(subject+" "+description)
    return {
        'filing_id':filing_id,
        'company_name':ann['sm_name'],
        'filing_type': filing_type,
        'symbol':symbol,
        'subject':subject,
        'description':description,
        'filing_date': filing_date,
        'pdf_url': ann['attchmntFile']
    }
def parse_nse_event(event:dict):
    description= ''
    subject= event['subject']
    company_name= event['comp']
    filing_date= event['recDate']
    symbol=event['symbol']
    filing_id= symbol+description+filing_date
    filing_id = hashlib.md5(filing_id.encode('utf-8')).hexdigest()
    filing_type= categorise_filing(subject+" "+description)
    return{
        'filing_id':filing_id,
        'filing_type':filing_type,
        'company_name':company_name,
        'symbol':symbol,
        'subject':subject,
        'description':description,
        'filing_date':filing_date,
        'pdf_url':None
    }
def parse_nse_board_meeting(board_meeeting:dict)->dict:
    subject= board_meeeting['bm_purpose']
    symbol = board_meeeting['bm_symbol']
    filing_date= board_meeeting['bm_timestamp']
    description = board_meeeting['bm_desc']
    filing_id = symbol+description+filing_date
    filing_id= hashlib.md5(filing_id.encode('utf-8')).hexdigest()
    filing_type = categorise_filing(subject+" "+description)
    return {
        'filing_id':filing_id,
        'company_name':board_meeeting['sm_name'],
        'filing_type': filing_type,
        'symbol':symbol,
        'subject':subject,
        'description':description,
        'filing_date': filing_date,
        'pdf_url': board_meeeting['attachment']
    }
