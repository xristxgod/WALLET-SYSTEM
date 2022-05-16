from os import environ, path, mkdir, listdir
import decimal
import logging

ROOT_DIR = path.dirname(path.abspath(__file__))
NOT_SEND = path.join(ROOT_DIR, 'not_send')
if 'not_send' not in listdir(ROOT_DIR):
    mkdir(NOT_SEND)

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    DATABASE_URL = environ.get("DATABASE_URL")

    RABBITMQ_URL = environ.get("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_BALANCER = environ.get("RABBITMQ_QUEUE_FOR_BALANCER")

    REDIS_URL = environ.get("REDIS_URL")

    BOT_ALERT_API_URL = environ.get("BOT_ALERT_API_URL")

    TRON_NODE_API_URL = environ.get("TRON_NODE_URL")


