import os
import logging

logger = logging.getLogger(__name__)

class Config(object):
    DATABASE_URL = os.getenv("DATABASE_URL")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_SENDER = os.getenv("RABBITMQ_QUEUE_FOR_SENDER")

    BOT_CHECKER_TOKEN = os.getenv("BOT_CHECKER_TOKEN")
    BOT_ALERT_TOKEN = os.getenv("BOT_ALERT_TOKEN")
    BOT_MAIN_TOKEN = os.getenv("BOT_MAIN_TOKEN")

    TRON_BLOCKCHAIN = os.getenv("TRON_BLOCKCHAIN", "https://shasta.tronscan.org/")