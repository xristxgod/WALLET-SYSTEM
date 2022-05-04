import typing

from src.models import TokenModel, WalletModel, WalletTransactionModel, UserModel
from src.settings import db

class Helper:

    MODELS = {
        "token_page": TokenModel,
        "wallet_page": WalletModel,
        "user_page": UserModel,
        "transaction_page": WalletTransactionModel
    }

    @staticmethod
    def get_all_tokens(tokens: typing.List[TokenModel]) -> typing.List[str]:
        return [f"{token.network}-{token.token}" for token in tokens]