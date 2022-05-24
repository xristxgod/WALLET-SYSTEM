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
if 'not_send' not in os.listdir(BASE_DIR):
    os.mkdir(NOT_SEND)
if "last_block.txt" not in os.listdir(BASE_DIR):
    with open(LAST_BLOCK, "w") as file:
        file.write("")

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    TRON_NODE_URL = os.getenv("TRON_NODE_URL", "http://tron-mainnet.mangobank.elcorp.io:8090")
    TRON_API_KEYS = os.getenv("TRON_API_KEYS", "a684fa6d-6893-4928-9f8e-8decd5f034f2,16c3b7ca-d498-4314-aa1d-a224135faa26,8d375175-fa31-490d-a224-63a056adb60b").split(",")

    NETWORK = os.getenv("NETWORK", "TESTNET")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mamedov00@127.0.0.1:5432/telegram_bot_system")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqps://yubbvrbt:52cIr-IEy45n6hptj5n0aIT0LRn0cnZ6@goose.rmq2.cloudamqp.com/yubbvrbt")
    RABBITMQ_QUEUE_FOR_SENDER = os.getenv("RABBITMQ_QUEUE_FOR_SENDER", "to_sender_queue")