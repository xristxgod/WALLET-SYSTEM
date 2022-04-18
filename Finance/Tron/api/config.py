import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)

class Config:
    NODE_URL = os.getenv("TRON_NODE_URL", "https://3.225.171.164:8090")
    TRON_API_KEYS = os.getenv("TRON_API_KEYS", "a684fa6d-6893-4928-9f8e-8decd5f034f2,").split(",")
    NODE_NETWORK = os.getenv("NETWORK", "TEST")
    DATABASE_URL = os.getenv("DATABASE_URL", "")