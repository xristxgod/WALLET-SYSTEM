import decimal
from typing import Optional, Dict, List

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel
from api.serializers import BodyGetBalanceSerializer, ResponserGetBalanceSerializer
from api.services.__init__ import BaseApiModel
from api.services.external.client import Client
from api.utils.types import CRYPRO_ADDRESS, FULL_NETWORK, NETWORK, DOMAIN, TG_CHAT_ID, COINS
from config import Config, decimals

APIs_URL: Dict[NETWORK, DOMAIN] = Config.CRYPTO_NETWORKS_APIS
GET_BALANCE_URL = "/api/<network>/balance/<address>"
COIN_TO_COIN_API_URL = Config.COIN_TO_COIN_API
GET_PRICE_URL = "/api/v3/simple/price?ids=<coin>&vs_currencies=<to_coin>"

# Body
class BodyGetBalanaceModel:
    """Type of input data"""
    NETWORK_OBJECT: object

    def __init__(
            self,
            chatID: TG_CHAT_ID,
            network: FULL_NETWORK,
            address: CRYPRO_ADDRESS = None,
            convert: Optional[List[str]] = None
    ):
        self.chatID: TG_CHAT_ID = chatID
        self.network: FULL_NETWORK = self.get_network(network.upper())
        self.address: CRYPRO_ADDRESS = address
        self.convert: Optional[List[str]] = convert
        self.is_valid()

    def get_network(self, network: str) -> FULL_NETWORK:
        try:
            self.NETWORK_OBJECT = NetworkModel.objects.get(network=network.split("-")[0])
        except Exception:
            raise ValidationError('This network is not in the database!')
        return network

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_address()
        self.__correct_convert()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if len(UserModel.objects.filter(pk=self.chatID)) == 0:
            raise ValidationError('This chatID is not in the database!')

    def __correct_address(self):
        if self.address is None:
            self.address = WalletModel.objects.get(network=self.NETWORK_OBJECT, user_id=self.chatID).address
        if not WalletModel.objects.filter(network=self.NETWORK_OBJECT, user_id=self.chatID, address=self.address)[0]:
            raise ValidationError('This address was not found in the database, or does not belong to this chatID!')

    def __correct_convert(self):
        if self.convert is not None and isinstance(self.convert, list) and len(self.convert) == 0:
            self.convert = None
        if self.convert is not None and not isinstance(self.convert, list):
            raise ValidationError('Convert must be a list: []!')

# Response
class ResponseGetBalanaceModel:
    """Type of output data"""
    def __init__(
            self,
            balance: decimal.Decimal,
            network: FULL_NETWORK,
            convert: Optional[Dict[str, decimal.Decimal]] = {}
    ):
        self.balance: decimal.Decimal = balance
        self.network: FULL_NETWORK = network
        self.convert: Optional[Dict[str, decimal.Decimal]] = convert

        self.is_valid()

    def is_valid(self):
        if self.convert is None:
            del self.convert


# <<<========================================>>> Create transaction <<<==============================================>>>

class GetBalance(BaseApiModel):
    """
    This class creates wallets in a certain crypto network.
    """
    @staticmethod
    def get_convert(balance: decimal.Decimal, network: FULL_NETWORK, toConvert: List[str]) -> Dict:
        balances = {}
        coin = COINS.get(network)
        for to_coin in toConvert:
            data = Client.get_request(GetBalance.get_url(
                base_url=COIN_TO_COIN_API_URL,
                url=GET_PRICE_URL,
                coin=coin,
                to_coin=to_coin
            ))
            if data[coin] != {} and data[coin] is not None:
                balances.update({
                    f"balance{to_coin.upper()}": balance * decimals.create_decimal(data[coin].get(to_coin))
                })
        return balances

    @staticmethod
    def get_balance(body: BodyGetBalanaceModel) -> ResponseGetBalanaceModel:
        network, token = body.network.split("-")
        data = Client.get_request(
            url=GetBalance.get_url(
                base_url=APIs_URL.get(network),
                url=GET_BALANCE_URL,
                network=COINS.get(body.network),
                address=body.address.encode("utf-8").hex().lower()
            )
        )
        if data.get("balance") is not None:
            balance = data.get("balance")
            wallet_object = WalletModel.objects.get(
                network=NetworkModel.objects.get(network=network.split("-")[0]),
                user_id=UserModel.objects.get(pk=body.chatID),
                address=body.address
            )
            wallet_object.last_balance = balance
            wallet_object.save()

        balance = WalletModel.objects.get(
            network=NetworkModel.objects.get(network=network.split("-")[0]),
            user_id=UserModel.objects.get(pk=body.chatID),
            address=body.address
        ).last_balance
        if body.convert is not None:
            convert = GetBalance.get_convert(balance=balance, network=body.network, toConvert=body.convert)
        else:
            convert = None
        return ResponseGetBalanaceModel(
            balance=decimals.create_decimal(balance),
            network=body.network,
            convert=convert
        )

    @staticmethod
    def encode(data: ResponseGetBalanaceModel) -> ResponserGetBalanceSerializer:
        """Generates data for the response"""
        return ResponserGetBalanceSerializer(data).data

    @staticmethod
    def decode(data) -> Optional:
        """Checks the input data"""
        serializer = BodyGetBalanceSerializer(data=data)
        serializer.is_valid(raise_exception=True)

get_balance = GetBalance