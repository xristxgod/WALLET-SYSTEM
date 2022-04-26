import os
import decimal
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "files")
COINS_LIST = os.path.join(BASE_DIR, "coins.json")
COINS_LIST_TOP_100 = os.path.join(BASE_DIR, "coins_top_100.json")
ERROR = os.path.join(BASE_DIR, "error.txt")

if "files" not in os.listdir(ROOT_DIR):
    os.mkdir(BASE_DIR)

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    DATABASE_URL = os.getenv("DATABASE_COINS_URL")

    API_COINS = os.getenv("API_COINS", "https://api.coingecko.com")

    RABBITMQ_QUEUE_CHECKER = os.getenv("RABBITMQ_QUEUE_CHECKER")
    RABBITMQ_ROUTING_KEY_CHECKER = os.getenv("RABBITMQ_ROUTING_KEY_CHECKER")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")