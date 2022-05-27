import decimal
from typing import Union

TG_CHAT_ID = Union[int, str, bytes]
TG_USERNAME = str

CRYPRO_ADDRESS = str
CRYPTO_MNEMONIC_WORDS = str

FULL_NETWORK = str
NETWORK = str
DOMAIN = str
JWT_TOKEN_BEARER = str

COINS = {
    "TRON-TRX": "tron",
    "TRON": "tron",
    "TRON-TRON": "tron",
    "TRON-USDT": "usdt"
}

def default_json(json_object: object):
    if isinstance(json_object, decimal.Decimal):
        return float(json_object)
    return str(json_object)

class CoinsHelper(object):
    TRON = "TRX"

    @staticmethod
    def get_native_by_network(network: str) -> str:
        return CoinsHelper.__dict__.get(network.upper())