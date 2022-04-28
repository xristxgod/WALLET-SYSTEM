import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config(object):
    SECRET_KEY: str = os.getenv("SECRET_KEY_ADMIN_SITE", "0UIwb0EU7RNwkPIfyLNwJs4H-8kBJP8PjFjFTg4pf_Q")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/wallets_system")

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    ADMIN_GOOGLE_AUTH_SECRET_KEY = os.getenv("ADMIN_GOOGLE_AUTH_SECRET_KEY", "")

