import decimal
from typing import Optional

from api.serializers import BodyCoinToCoinSerializer, ResponseCoinToCoinSerializer
from api.services.external.client import Client
from config import Config, decimals

# Body
class BodyCoinToCoinModel:
    """Type of input data"""
    def __init__(self, coin: str, toCoin: str = 'usd'):
        self.coin: str = coin
        self.toCoin: str = toCoin
        self.is_valid()

    def is_valid(self):
        if isinstance(self.coin, list):
            self.coin, = self.coin
        if isinstance(self.toCoin, list):
            self.toCoin, = self.toCoin

# Response
class ResponseCoinToCoinModel:
    """Type of output data"""
    def __init__(self, price: decimal.Decimal):
        self.price: decimal.Decimal = price

# <<<========================================>>> Coin to coin <<<====================================================>>>

class CoinToCoin:
    """
    This class is used to work with the coingecko api.
    To get the exact exchange rates.
    """
    API_URL = Config.COIN_TO_COIN_API
    GET_PRICE = "/api/v3/simple/price?ids=<coin>&vs_currencies=<to_coin>"

    @staticmethod
    def _get_url(url: str, **params) -> str:
        """Generates the correct url"""
        for key, value in params.items():
            url = url.replace(f"<{key}>", value)
        return CoinToCoin.API_URL + url

    @staticmethod
    def get_price(body: BodyCoinToCoinModel) -> ResponseCoinToCoinModel:
        """Get the price of the selected currency in the selected currency"""
        data = Client.get_request(CoinToCoin._get_url(
            url=CoinToCoin.GET_PRICE,
            coin=body.coin,
            to_coin=body.toCoin
        ))
        return ResponseCoinToCoinModel(price=decimals.create_decimal(data[body.coin].get(body.toCoin)))

    @staticmethod
    def encode(data: ResponseCoinToCoinModel) -> ResponseCoinToCoinSerializer:
        """Generates data for the response"""
        return ResponseCoinToCoinSerializer(data).data

    @staticmethod
    def decode(data) -> Optional:
        """Checks the input data"""
        serializer = BodyCoinToCoinSerializer(data=data)
        serializer.is_valid(raise_exception=True)

coin_to_coin = CoinToCoin
