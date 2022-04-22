import os
import decimal
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "files")
ERROR = os.path.join(BASE_DIR, "error.txt")
NOT_SEND = os.path.join(BASE_DIR, 'not_send')
ENDPOINTS_FILE = os.path.join(BASE_DIR, "endpoints.json")

if "files" not in os.listdir(ROOT_DIR):
    os.mkdir(BASE_DIR)

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config:
    BOT_TOKEN_CHECKER = os.getenv("BOT_TOKEN_CHECKER")

    DATABASE_URL = os.getenv("DATABASE_URL")

    RABBITMQ_QUEUE_SENDER = os.getenv("RABBITMQ_QUEUE_SENDER")
    RABBITMQ_ROUTING_KEY_SENDER = os.getenv("RABBITMQ_ROUTING_KEY_SENDER")

    RABBITMQ_QUEUE_CHECKER = os.getenv("RABBITMQ_QUEUE_CHECKER")
    RABBITMQ_ROUTING_KEY_CHECKER = os.getenv("RABBITMQ_ROUTING_KEY_CHECKER")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")