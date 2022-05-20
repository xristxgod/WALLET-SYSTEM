import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)
COINS = {
    "trx": "tron",
    "usdt": "tether"
}

class Config(object):
    NODE_URL = os.getenv("TRON_NODE_URL", "https://3.225.171.164:8090")
    TRON_API_KEYS = os.getenv("TRON_API_KEYS", "a684fa6d-6893-4928-9f8e-8decd5f034f2,16c3b7ca-d498-4314-aa1d-a224135faa26,8d375175-fa31-490d-a224-63a056adb60b").split(",")
    NETWORK = os.getenv("NETWORK", "TESTNET")
    DATABASE_URL = os.getenv("DATABASE_URL")
    CHECKER_NODE_BLOCK = os.getenv("CHECKER_NODE_BLOCK", "https://ngx.com")