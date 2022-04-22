import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config:
    BOT_TOKEN_ALERT = os.getenv("BOT_TOKEN_ALERT")

    DATABASE_URL = os.getenv("DATABASE_URL")

    RABBITMQ_QUEUE_SENDER = os.getenv("RABBITMQ_QUEUE_SENDER")
    RABBITMQ_ROUTING_KEY_SENDER = os.getenv("RABBITMQ_ROUTING_KEY_SENDER")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")