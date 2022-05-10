from src.api.schemas import BodyCreateTransaction, ResponseCreateTransaction
from src.utils.types import CryptoEndpointType
from src.crypto.client import Client

class Transaction:
    @staticmethod
    def create_transaction(body: BodyCreateTransaction) -> ResponseCreateTransaction:
        method, url = CryptoEndpointType.get_optimal_fee_url(network=body.network, inputs=body.inputs, outputs=body.outputs)
        fee = Client.request(method, url).get("fee")
        return ResponseCreateTransaction(
            fee=fee,
            bodyTransaction={
                "chat_id": body.chat_id,
                "network": body.network,
                "inputs": body.inputs,
                "outputs": body.outputs,
            }
        )