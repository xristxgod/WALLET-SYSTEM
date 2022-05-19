from typing import Optional, Dict

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel
from api.serializers import BodyCreateWalletSerializer, ResponserCreateWalletSerializer
from api.services.__init__ import BaseApiModel
from api.services.external.client import Client
from api.services.external.sender import Sender
from api.utils.types import CRYPTO_MNEMONIC_WORDS, NETWORK, TG_CHAT_ID, TG_USERNAME
from config import Config, logger

# Body
class BodyCreateWalletModel:
    """Type of input data"""
    def __init__(
            self,
            chatID: TG_CHAT_ID,
            username: Optional[TG_USERNAME],
            network: NETWORK,
            passphrase: str = None,
            mnemonicWords: CRYPTO_MNEMONIC_WORDS = None
    ):
        self.chatID: TG_CHAT_ID = chatID
        self.username: Optional[TG_USERNAME] = username
        self.network: NETWORK = network
        self.passphrase: str = passphrase
        self.mnemonicWords: CRYPTO_MNEMONIC_WORDS = mnemonicWords
        self.is_valid()

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_network()
        self.__correct_username()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if not UserModel.objects.get(self.chatID):
            raise ValidationError('This chatID is not in the database!')

    def __correct_username(self):
        if self.username.find("@") == -1:
            self.username = "@" + self.username


    def __correct_network(self):
        if not NetworkModel.objects.filter(network=self.network)[0]:
            raise ValidationError('This network is not in the database!')

# Response
class ResponseCreateWalletModel:
    """Type of output data"""
    def __init__(self, message: bool = True):
        self.message: bool = message

# <<<========================================>>> Create transaction <<<==============================================>>>

class CreateWallet(BaseApiModel):
    """
    This class creates wallets in a certain crypto network.
    """
    APIs_URL: Dict[NETWORK] = Config.CRYPTO_NETWORKS_APIS
    CREATE_WALLET_URL = "/api/<network>/create/wallet"

    @staticmethod
    def send_to_bot_alert(body: BodyCreateWalletModel, is_admin: bool = False):
        try:
            Sender.send_message_to_alert_bot(
                chat_id=body.chatID,
                username=body.username,
                is_admin=is_admin
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            Sender.send_message_to_checker(
                text=f"{error}",
                method="INFO_CHECKER"
            )

    @staticmethod
    def create_wallet(body: BodyCreateWalletModel) -> ResponseCreateWalletModel:
        data = Client.post_request(
            url=CreateWallet.get_url(
                base_url=CreateWallet.APIs_URL.get(body.network),
                url=CreateWallet.CREATE_WALLET_URL,
                network=body.network
            ),
            passphrase=body.passphrase,
            mnemonicWords=body.mnemonicWords
        )
        try:
            if not UserModel.objects.get(body.chatID):
                UserModel.objects.create(
                    id=body.chatID,
                    username=body.username,
                    is_admin=False
                )
                # Send to bot if this new user
                CreateWallet.send_to_bot_alert(body=body, is_admin=False)
            WalletModel.objects.create(
                network=body.network,
                address=data.get("address"),
                private_key=data.get("privateKey"),
                public_key=data.get("publicKey"),
                passphrase=data.get("passphrase"),
                mnemonic_phrase=data.get("mnemonicWords"),
                last_balance=0,
                user_id=body.chatID
            )
            return ResponseCreateWalletModel(message=True)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            Sender.send_message_to_checker(
                text=f"{error}",
                method="INFO_CHECKER"
            )
            return ResponseCreateWalletModel(message=False)

    @staticmethod
    def encode(data: ResponseCreateWalletModel) -> ResponserCreateWalletSerializer:
        """Generates data for the response"""
        return ResponserCreateWalletSerializer(data).data

    @staticmethod
    def decode(data) -> Optional:
        """Checks the input data"""
        serializer = BodyCreateWalletSerializer(data=data)
        serializer.is_valid(raise_exception=True)

create_wallet = CreateWallet