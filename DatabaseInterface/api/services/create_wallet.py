import decimal
from typing import Optional, List, Dict

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel
from api.serializers import BodyCreateWalletSerializer, ResponserCreateWalletSerializer
from api.services.__init__ import BaseApiModel
from api.utils.types import CRYPRO_ADDRESS, CRYPTO_MNEMONIC_WORDS, FULL_NETWORK, NETWORK, TG_CHAT_ID

# Body
class ResponseBodyWalletModel:
    """Type of input data"""
    def __init__(
            self,
            chatID: TG_CHAT_ID,
            network: NETWORK,
            passphrase: str = None,
            mnemonicWords: CRYPTO_MNEMONIC_WORDS = None
    ):
        self.chatID = chatID
        self.network = network
        self.passphrase = passphrase
        self.mnemonicWords = mnemonicWords
        self.is_valid()

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_network()


    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if not UserModel.objects.get(self.chatID):
            raise ValidationError('This chatID is not in the database!')

    def __correct_network(self):
        if not NetworkModel.objects.filter(network=self.network.split("_")[0])[0]:
            raise ValidationError('This network is not in the database!')
        
# Response
class ResponseCreateWalletModel:
    """Type of output data"""
    def __init__(self, chatID: TG_CHAT_ID):
        self.chatID: decimal.Decimal = chatID

# <<<========================================>>> Create transaction <<<==============================================>>>

class CreateTransaction(BaseApiModel):
    """

    """
    pass