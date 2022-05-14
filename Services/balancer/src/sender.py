from typing import Dict

from config import Config

class SenderCrypto:
    API_URLs: Dict = {"TRON": Config.TRON_NODE_API_URL}
    CREATE_TRANSACTION_URL = "/api/<network>/create/transaction"
    SEND_TRANSACTION_URL = ""

class SenderBot:
    pass