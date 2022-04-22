import os
import decimal
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "files")
ERROR = os.path.join(BASE_DIR, "error.txt")
NOT_SEND = os.path.join(BASE_DIR, 'not_send')
LAST_BLOCK = os.path.join(BASE_DIR, "last_block.txt")

if "files" not in os.listdir(ROOT_DIR):
    os.mkdir(BASE_DIR)

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config:
    NODE_URL = os.getenv("TRON_NODE_URL", "https://3.225.171.164:8090")
    TRON_API_KEYS = os.getenv("TRON_API_KEYS", "a684fa6d-6893-4928-9f8e-8decd5f034f2,16c3b7ca-d498-4314-aa1d-a224135faa26,8d375175-fa31-490d-a224-63a056adb60b").split(",")
    NODE_NETWORK = os.getenv("NETWORK", "TEST")
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    RABBITMQ_QUEUE_SENDER = os.getenv("DEMONS_QUEUE_SENDER")
    RABBITMQ_ROUTING_KEY_SENDER = os.getenv("DEMONS_ROUTING_KEY_SENDER")

    RABBITMQ_QUEUE_CHECKER = os.getenv("RABBITMQ_QUEUE_CHECKER")
    RABBITMQ_ROUTING_KEY_CHECKER = os.getenv("RABBITMQ_ROUTING_KEY_CHECKER")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")