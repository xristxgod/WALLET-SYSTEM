import os
import logging
import decimal

decimals = decimal.Context()
decimals.prec = 18

logger = logging.getLogger(__name__)

class Config(object):
    DEBUG = bool(os.getenv("DEBUG", "1"))
    BASE_APP_SECRET_KEY = os.getenv("BASE_APP_SECRET_KEY", "django-insecure-d07ohkof%-t&2x0-&p8-d5+d0d9ph-)&ysqw!d43&*$%y$8gob")
    DB_NAME = os.environ.get("POSTGRES_DB", "wallet_system")
    USERNAME = os.environ.get("POSTGRES_USER", "postgres")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mamedov00")
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PORT = int(os.getenv("POSTGRES_PORT", "5432"))