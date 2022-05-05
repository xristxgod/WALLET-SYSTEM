import psycopg2
from typing import List

from src.models import TokenModel

from config import Config, logger

class Helper:

    @staticmethod
    def get_all_tokens(tokens: List[TokenModel]) -> List[str]:
        return [f"{token.network}-{token.token}" for token in tokens]

    @staticmethod
    def delete_all_wallets_by_user_id(user_id: int) -> bool:
        connection = None
        try:
            connection = psycopg2.connect(Config.DATABASE_URL)
            cursor = connection.cursor()
            cursor.execute((
                f"DELETE FROM wallet_model WHERE user_id={user_id};"
                f"DELETE FROM wallet_transaction_model WHERE user_id={user_id};"
            ))
            connection.commit()
            return True
        except Exception as error:
            connection.rollback()
            logger.error(f"ERROR: {error}")
            return False
        finally:
            if connection is not None:
                connection.close()