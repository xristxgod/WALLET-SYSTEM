from typing import List, Dict

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
    def get_all_tokens(tokens: List[TokenModel]) -> List[str]:
        return [f"{token.network}-{token.token}" for token in tokens]

    @staticmethod
    def get_all_users(users: List[UserModel]) -> List[Dict]:
        return [{"id": user.id, "username": user.username, "is_admin": user.is_admin} for user in users]