import decimal

from src.settings import db
from src.models import WalletModel

from src.api.schemas import BodyCreateWallet, BodyCheckBalance
from src.api.schemas import ResponseCreateWallet, ResponseCheckBalance

from src.services.coin_to_coin import coin
from src.utils.types import CryptoEndpointType
from src.crypto.client import Client
from config import logger, decimals

class Wallet:

    @staticmethod
    def create_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        """Create crypto wallet"""
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

    @staticmethod
    def check_balance(body: BodyCheckBalance) -> ResponseCheckBalance:
        """Check crypto wallet balance"""
        method, url = CryptoEndpointType.get_balance_url(network=body.network, address=body.address)
        result = Client.request(method=method, url=url)
        if body.convert is None:
            return ResponseCheckBalance(
                balance=decimals.create_decimal(result.get("balance")),
                network=body.network
            )
        convert_list = []
        for to_coin in body.convert:
            price: decimal.Decimal = coin.get_current_price(
                coin=coin.get_correct_token(result.get("token")),
                to_coin=to_coin
            )
            convert_list.append({
                f"balance{to_coin.upper()}": price * decimals.create_decimal(result.get("balance"))
            })
        return ResponseCheckBalance(
            balance=decimals.create_decimal(result.get("balance")),
            network=body.network,
            convert=convert_list
        )