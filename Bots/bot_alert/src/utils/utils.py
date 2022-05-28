from typing import List, Tuple, Dict
from src.utils.types import CoinsURL, CryptoAddress, Network

class Utils:

    @staticmethod
    def get_message_id(message: Dict) -> int:
        try:
            return int(message.get("result")["message_id"])
        except Exception as error:
            return -1

    @staticmethod
    def get_correct_tx_data(
            inputs: List[Dict[CryptoAddress, float]],
            outputs: List[Dict[CryptoAddress, float]],
            network: Network
    ) -> Tuple[str, str]:
        from_addresses, to_addresses = "", ""
        for _input in inputs:
            from_addresses += f"<b>{_input.get('address')} == {_input.get('amount')} {network}</b>\n"
        for _output in outputs:
            to_addresses += f"<b>{_output.get('address')} == {_output.get('amount')} {network}</b>\n"
        return from_addresses, to_addresses

    @staticmethod
    def get_blockchain_url(network: Network, transaction_hash: str) -> str:
        try:
            return CoinsURL.get_blockchain_url_by_network(network) + f"/#/transaction/{transaction_hash}"
        except Exception:
            return None