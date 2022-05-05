import os
import logging

logger = logging.getLogger(__name__)

class Config(object):
    BOT_CHECKER_TOKEN = os.getenv("BOT_CHECKER_TOKEN")
    BOT_ALERT_TOKEN = os.getenv("BOT_ALERT_TOKEN")