from os import getenv
from typing import Tuple
import logging
import decimal

logger = logging.getLogger(__name__)

decimals = decimal.Context()
decimals.prec = 10

class Config(object):
    RABBITMQ_URL = getenv("RABBITMQ_URL", "amqps://yubbvrbt:52cIr-IEy45n6hptj5n0aIT0LRn0cnZ6@goose.rmq2.cloudamqp.com/yubbvrbt")
    RABBITMQ_QUEUE_FOR_BALANCER = getenv("RABBITMQ_QUEUE_FOR_BALANCER", "to_balancer_queue")

    DATABASE_URL = getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")
    DATABASE_INTERFACE_USERNAME = getenv("DATABASE_INTERFACE_USERNAME", "root")
    DATABASE_INTERFACE_PASSWORD = getenv("DATABASE_INTERFACE_PASSWORD", "0000")
    DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY = getenv("DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY", "https://medium.com/aubergine-solutions/quick-start-two-factor-authentication-in-django-admin-panel-d15ceeb62591")
    DATABASE_INTERFACE_SECRET_KEY = getenv("DATABASE_INTERFACE_SECRET_KEY", "django-insecure-yc25#g4+l$6_@q(41ct2d9zd@o!w4+yt&v8q68hv*esav^k-9n")

    COIN_TO_COIN_API = getenv("COIN_TO_COIN_API", "https://api.coingecko.com")
    CRYPTO_NETWORKS_APIS = {
        "TRON": getenv("DOMAIN_TRON_API", "http://127.0.0.1:5000")
    }
    CRYPTO_NETWORKS_JWT_TOKENS = {
        "TRON": getenv("TRON_JWT_TOKEN", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IlRST04ifQ.TJf7gCgfP0nNBodmhewofAKdMhT-dThaGzjVe-EJgS8")
    }

    BOT_ALERT_API_URL = getenv("BOT_ALERT_API_URL", "-")

def get_db_config(url: str = Config.DATABASE_URL) -> Tuple:
    user = url.split(":")[1].replace("//", "")
    password = url.split(":")[2].split("@")[0]
    host = url.split(":")[2].split("@")[1].split("/")[0]
    port = url.split(":")[3].split("/")[0] if host != "localhost" else None
    db_name = url.split(":")[3].split("/")[1] if port else url.split(":")[2].split("/")[1]
    return user, password, host, port, db_name

USER, PASSWORD, HOST, PORT, DB_NAME = get_db_config()