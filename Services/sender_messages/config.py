import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    BOT_ALERT_API_URL = os.getenv("BOT_ALERT_API_URL")

    DATABASE_URL = os.getenv("DATABASE_URL")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_SENDER = os.getenv("RABBITMQ_QUEUE_FOR_SENDER")