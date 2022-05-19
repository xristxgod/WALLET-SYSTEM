import decimal
from typing import Optional, Dict, List

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel
from api.serializers import BodyGetBalanceSerializer, ResponserGetBalanceSerializer
from api.services.__init__ import BaseApiModel
from api.services.external.client import Client
from api.services.external.sender import Sender
from api.utils.types import CRYPRO_ADDRESS, FULL_NETWORK, TG_CHAT_ID, TG_USERNAME
from config import Config, logger

# Body
class BodyGetBalanaceModel:
    """Type of input data"""
    def __init__(
            self,
            chatID: TG_CHAT_ID,
            network: FULL_NETWORK,
            address: CRYPRO_ADDRESS = None,
            convert: Optional[List[str]] = None
    ):
        self.chatID: TG_CHAT_ID = chatID
        self.network: FULL_NETWORK = network
        self.address: CRYPRO_ADDRESS = address
        self.convert: Optional[List[str]] = convert
        self.is_valid()

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_network()
        self.__correct_address()
        self.__correct_convert()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if not UserModel.objects.get(self.chatID):
            raise ValidationError('This chatID is not in the database!')

    def __correct_network(self):
        if not NetworkModel.objects.filter(network=self.network.split("_")[0])[0]:
            raise ValidationError('This network is not in the database!')

    def __correct_address(self):
        if self.address is None:
            self.address = WalletModel.objects.filter(network=self.network.split("_")[0], user_id=self.chatID)[0]
        if not WalletModel.objects.filter(network=self.network.split("_")[0], user_id=self.chatID, address=self.address)[0]:
            raise ValidationError('This address was not found in the database, or does not belong to this chatID!')

    def __correct_convert(self):
        if self.convert is not None and isinstance(self.convert, list) and len(self.convert) == 0:
            self.convert = None
        if self.convert is not None and not isinstance(self.convert, list):
            raise ValidationError('Convert must be a list: []!')

# Response
class ResponseGetBalanaceModel:
    """Type of output data"""
    def __init__(self, balance: decimal.Decimal, network: FULL_NETWORK, convert: Optional[List[str]] = []):
        self.balance: decimal.Decimal = balance
        self.network: FULL_NETWORK = network
        self.convert: Optional[List[str]] = convert

# <<<========================================>>> Create transaction <<<==============================================>>>

class GetBalance(BaseApiModel):
    @staticmethod
    def get_balance(body: BodyGetBalanaceModel) -> ResponseGetBalanaceModel:
        pass

get_balance = GetBalance