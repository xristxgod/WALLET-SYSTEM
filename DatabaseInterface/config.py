from os import getenv
from typing import Tuple
import logging
import decimal

logger = logging.getLogger(__name__)

decimals = decimal.Context()
decimals.prec = 10

class Config(object):
    RABBITMQ_URL = getenv("RABBITMQ_URL")
    RABBITMQ_QUEUE_FOR_BALANCER = getenv("RABBITMQ_QUEUE_FOR_BALANCER")

    DATABASE_URL = getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")
    DATABASE_INTERFACE_USERNAME = getenv("DATABASE_INTERFACE_USERNAME")
    DATABASE_INTERFACE_PASSWORD = getenv("DATABASE_INTERFACE_PASSWORD")
    DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY = getenv("DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY")
    DATABASE_INTERFACE_SECRET_KEY = getenv("DATABASE_INTERFACE_SECRET_KEY", "django-insecure-yc25#g4+l$6_@q(41ct2d9zd@o!w4+yt&v8q68hv*esav^k-9n")

    COIN_TO_COIN_API = getenv("COIN_TO_COIN_API_URL")
    CRYPTO_NETWORKS_APIS = {"TRON": getenv("TRON_API_URL")}
    CRYPTO_NETWORKS_JWT_TOKENS = {"TRON": getenv("TRON_JWT_TOKEN")}

    BOT_ALERT_API_URL = getenv("BOT_ALERT_API_URL")
    BOT_ALERT_JWT_TOKEN = getenv("BOT_ALERT_JWT_TOKEN")

def get_db_config(url: str = Config.DATABASE_URL) -> Tuple:
    user = url.split(":")[1].replace("//", "")
    password = url.split(":")[2].split("@")[0]
    host = url.split(":")[2].split("@")[1].split("/")[0]
    try:
        port = url.split(":")[3].split("/")[0]
    except Exception:
        port = None
    try:
        db_name = url.split(":")[2].split("/")[1]
    except Exception:
        db_name = url.split(":")[3].split("/")[1]
    return user, password, host, port, db_name

USER, PASSWORD, HOST, PORT, DB_NAME = get_db_config()