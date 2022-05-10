from src.settings import db
from src.models import WalletModel
from src.api.schemas import BodyCreateWallet, ResponseCreateWallet
from src.utils.types import CryptoEndpointType
from src.crypto.client import Client
from config import logger

class Wallet:

    @staticmethod
    def create_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        method, url = CryptoEndpointType.get_create_wallet_url(network=body.network)
        data = {
            "passphrase": body.passphrase,
            "mnemonicWords": body.mnemonic_words,
        }
        result = Client.request(method, url, **data)
        try:
            create_wallet = WalletModel(
                network=body.network.split("_")[0],
                address=result.get("address"),
                private_key=result.get("privateKey"),
                public_key=result.get("publicKey"),
                passphrase=result.get("passphrase"),
                mnemonic_phrase=result.get("mnemonicWords"),
                user_id=body.chatID,
            )
            db.session.add(create_wallet)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logger.error(f"ERROR: {error}")
            raise error
        return ResponseCreateWallet(message=True)