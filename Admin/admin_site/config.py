import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    SECRET_KEY: str = os.getenv("SECRET_KEY_ADMIN_SITE")
    DATABASE_URL = os.getenv("DATABASE_URL")

