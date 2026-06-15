import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL= os.environ['DATABASE_URL']

USER_AGENT = os.environ['USER_AGENT']

SOURCE_RELOAD_INTERVAL_MIN = int(os.environ['SOURCE_RELOAD_INTERVAL_MIN'])
STAGGER_SECONDS = 30
