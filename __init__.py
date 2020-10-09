from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from .config import API_ID, API_HASH, STRING_SESSION, BOTS_CONFIG, BOTS_LIST, LOG_CHANNEL

LOG_CHANNEL = LOG_CHANNEL
BOTS_LIST = BOTS_LIST
BOTS_CONFIG = BOTS_CONFIG

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
