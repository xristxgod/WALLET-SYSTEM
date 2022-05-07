import os
import decimal
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NOT_SEND = os.path.join(ROOT_DIR, 'not_send')
if 'not_send' not in os.listdir(ROOT_DIR):
    os.mkdir(NOT_SEND)

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    BOT_ALERT_API_URL = os.getenv("BOT_ALERT_API_URL")

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_SENDER = os.getenv("RABBITMQ_QUEUE_FOR_SENDER")