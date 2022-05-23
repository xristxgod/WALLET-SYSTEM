from typing import Optional, Dict
from datetime import datetime

from api.utils.types import TG_CHAT_ID, FULL_NETWORK
from api.utils.utils import Utils

class BaseApiModel:

    @staticmethod
    def get_url(base_url: str, url: str, **params) -> str:
        """Generates the correct url"""
        for key, value in params.items():
            url = url.replace(f"<{key.lower()}>", value.lower())
        return base_url + url

    @staticmethod
    def get_headers(jwt_token: str = None, **kwargs) -> Dict:
        if jwt_token:
            return {
                "Authorization": jwt_token,
                **kwargs
            }
        return kwargs


    @staticmethod
    def encode(data: object) -> object:
        pass

    @staticmethod
    def decode(data) -> Optional:
        pass

class TransactionRepository:
    """
    This time class stores transactions created via the create transaction router.
    """
    WAIT_MINUTES = 15
    WAIT_SECONDS = 30

    def __init__(self):
        """
        {
            "chatID": {
                "network": {tx_data},
            }
            "1241515": {
                "TRON_USDT": {
                    "inputs": [
                        "TXkoKX6pBtkyThsJWR6RHT2zpWMQAdompk"
                    ],
                    "outputs": [
                        {
                            "address": "TVA8KhsXvMbKgZQNNMuvAEYkam55y9ZJWj",
                            "amount": 10.331
                        }
                    ],
                    "fee": 5.0032
                    "timestamp": 242475751823
                }
            }
        }
        """
        self.__transactions_list: Dict = {}

    def set_transaction(self, chat_id: TG_CHAT_ID, network: FULL_NETWORK, **transaction_data):
        if chat_id in self.__transactions_list.keys() and network in self.__transactions_list.get(chat_id).keys():
            self.__transactions_list[chat_id].pop(network)

        if chat_id in self.__transactions_list.keys() and network not in self.__transactions_list.get(chat_id).keys():
            self.__transactions_list[chat_id].update({
                network: {
                    "inputs": transaction_data.get("inputs"),
                    "outputs": transaction_data.get("outputs"),
                    "fee": transaction_data.get("fee"),
                    "timestamp": int(datetime.timestamp(datetime.now()))
                }
            })
        elif chat_id not in self.__transactions_list.keys():
            self.__transactions_list.update({
                chat_id: {
                    network: {
                        "inputs": transaction_data.get("inputs"),
                        "outputs": transaction_data.get("outputs"),
                        "fee": transaction_data.get("fee"),
                        "timestamp": int(datetime.timestamp(datetime.now()))
                    }
                }
            })

    def remove_transaction(self, chat_id: TG_CHAT_ID, network: FULL_NETWORK) -> bool:
        try:
            chat_id_data: Optional[Dict] = self.__transactions_list.get(chat_id)
            if chat_id_data is None:
                return True
            transaction_data: Optional[Dict] = chat_id_data.get(network)
            if transaction_data is None:
                return True
            if len(chat_id_data) == 1:
                self.__transactions_list.pop(chat_id)
            else:
                self.__transactions_list[chat_id].pop(network)
            return True
        except Exception:
            return False

    def get_transaction(self, chat_id: TG_CHAT_ID, network: FULL_NETWORK) -> Optional[Dict]:
        chat_id_data: Optional[Dict] = self.__transactions_list.get(chat_id)
        if chat_id_data is None:
            return None
        transaction_data: Optional[Dict] = chat_id_data.get(network)
        if transaction_data is None:
            return None
        if not Utils.is_have_time(transaction_data["timestamp"], minutes=self.WAIT_MINUTES, seconds=self.WAIT_SECONDS):
            self.__transactions_list[chat_id].pop(network)
            return None
        return transaction_data

    @property
    def transactions(self):
        return self.__transactions_list

    def remove_all_transactions(self) -> bool:
        self.__transactions_list = []
        return True

transaction_repository = TransactionRepository()