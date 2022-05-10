from typing import Optional
import decimal

import requests

from config import Config, decimals, logger

class CoinToCoin:

    STATUS_URL = Config.COIN_TO_COIN_API + "/api/v3/ping"
    COIN_TO_COIN_URL = Config.COIN_TO_COIN_API + "/api/v3/simple/price?<params>"

    @staticmethod
    def status_api() -> bool:
        try:
            return requests.request("GET", CoinToCoin.STATUS_URL).ok is not None
        except Exception as error:
            return False

    @staticmethod
    def get_current_price(coin: str, to_coin: str = "usd") -> Optional[decimal.Decimal]:
        try:
            params = f"ids={coin}&vs_currencies={to_coin}"
            response = requests.request("GET", CoinToCoin.COIN_TO_COIN_URL.replace("<params>", params))
            coin_price = response.json().get(coin).get(to_coin)
            return decimals.create_decimal(coin_price)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return None

coin = CoinToCoin