from os import environ
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    DATABASE_URL = environ.get("DATABASE_URL")

    RABBITMQ_URL = environ.get("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_BALANCER = environ.get("RABBITMQ_QUEUE_FOR_BALANCER")

    REDIS_URL = environ.get("REDIS_URL")
    
    BOT_ALERT_API_URL = environ.get("BOT_ALERT_API_URL")


