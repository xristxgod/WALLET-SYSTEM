from typing import Optional, Dict

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel
from api.serializers import BodyCreateWalletSerializer, ResponserCreateWalletSerializer
from api.services.__init__ import BaseApiModel
from api.services.external.client import Client
from api.services.external.sender import Sender
from api.utils.types import CRYPTO_MNEMONIC_WORDS, NETWORK, DOMAIN, JWT_TOKEN_BEARER, TG_CHAT_ID, TG_USERNAME
from config import Config, logger

APIs_URL: Dict[NETWORK, DOMAIN] = Config.CRYPTO_NETWORKS_APIS
CREATE_WALLET_URL = "/api/<network>/create/wallet"
JWT_TOKENS_BEARER: Dict[NETWORK, JWT_TOKEN_BEARER] = Config.CRYPTO_NETWORKS_JWT_TOKENS

# Body
class BodyCreateWalletModel:
    """Type of input data"""
    NETWORK_OBJECT: object

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
        self.network: NETWORK = self.get_network(network.upper())
        self.passphrase: str = passphrase
        self.mnemonicWords: CRYPTO_MNEMONIC_WORDS = mnemonicWords
        self.is_valid()

    def get_network(self, network: str) -> NETWORK:
        try:
            self.NETWORK_OBJECT = NetworkModel.objects.get(network=network)
        except Exception:
            raise ValidationError('This network is not in the database!')
        return network

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_username()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')

    def __correct_username(self):
        if self.username.find("@") == -1:
            self.username = "@" + self.username

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
                base_url=APIs_URL.get(body.network),
                url=CREATE_WALLET_URL,
                network=body.network
            ),
            headers=CreateWallet.get_headers(
                jwt_token=JWT_TOKENS_BEARER.get(body.network)
            ),
            passphrase=body.passphrase,
            mnemonicWords=body.mnemonicWords
        )
        if len(WalletModel.objects.filter(user_id=body.chatID)) >= 1:
            return ResponseCreateWalletModel(message=True)
        try:
            if len(UserModel.objects.filter(pk=body.chatID)) == 0:
                user = UserModel(
                    id=body.chatID,
                    username=body.username,
                    is_admin=False
                )
                user.save()
                # Send to bot if this new user
                CreateWallet.send_to_bot_alert(body=body, is_admin=False)
            wallet = WalletModel(
                network=NetworkModel.objects.get(network=body.network),
                address=data.get("address"),
                private_key=data.get("privateKey"),
                public_key=data.get("publicKey"),
                passphrase=data.get("passphrase"),
                mnemonic_phrase=data.get("mnemonicWords"),
                last_balance=0,
                user_id=UserModel.objects.get(pk=body.chatID)
            )
            wallet.save()
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