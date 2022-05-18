from typing import Optional, Dict
from datetime import datetime

from api.utils.types import TG_CHAT_ID, FULL_NETWORK
from api.utils.utils import Utils

class TransactionRepository:
    """
    This time class stores transactions created via the create transaction router.
    """
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
        self.transactions_list: Dict = {}

    def set_transaction(self, chat_id: TG_CHAT_ID, network: FULL_NETWORK, **transaction_data):
        if chat_id in self.transactions_list.keys() and network in self.transactions_list.get(chat_id).keys():
            self.transactions_list[chat_id].pop(network)

        if chat_id in self.transactions_list.keys() and network not in self.transactions_list.get(chat_id).keys():
            self.transactions_list.get(chat_id).update({
                "inputs": transaction_data.get("inputs"),
                "outputs": transaction_data.get("outputs"),
                "fee": transaction_data.get("fee"),
                "timestamp": int(datetime.timestamp(datetime.now()))
            })
        elif chat_id not in self.transactions_list.keys():
            self.transactions_list.update({
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
            chat_id_data: Optional[Dict] = self.transactions_list.get(chat_id)
            if chat_id_data is None:
                return True
            transaction_data: Optional[Dict] = chat_id_data.get(network)
            if transaction_data is None:
                return True
            self.transactions_list[chat_id].pop(network)
            return True
        except Exception:
            return False

    def get_transaction(self, chat_id: TG_CHAT_ID, network: FULL_NETWORK) -> Optional[Dict]:
        chat_id_data: Optional[Dict] = self.transactions_list.get(chat_id)
        if chat_id_data is None:
            return None
        transaction_data: Optional[Dict] = chat_id_data.get(network)
        if transaction_data is None:
            return None
        if not Utils.is_have_time(transaction_data["timestamp"], minute=15):
            self.transactions_list[chat_id].pop(network)
            return None
        return transaction_data