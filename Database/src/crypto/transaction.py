from typing import List

from src.models import WalletTransactionModel, WalletModel
from src.settings import db

from src.api.schemas import BodyTransaction, ResponseCreateTransaction, ResponseSendTransaction
from src.utils.types import CryptoEndpointType, CRYPTOPrivateKey
from src.crypto.client import Client

from config import logger

class Transaction:

    @staticmethod
    def _create_transaction(body: BodyTransaction) -> str:
        """Create crypto transaction """
        method, url = CryptoEndpointType.get_create_transaction(network=body.network)
        data = {
            "fromAddress": body.inputs,
            "outputs": body.outputs
        }
        result = Client.request(method=method, url=url, **data)
        try:
            body_transaction = result.get("bodyTransaction")
            tx_create = WalletTransactionModel(
                network=body.network.split("_")[0].upper(),
                time=body_transaction.get("time"),
                transaction_hash=body_transaction.get("transactionHash"),
                fee=body_transaction.get("fee"),
                amount=body_transaction.get("amount"),
                senders=body_transaction.get("senders"),
                recipients=body_transaction.get("recipients"),
                token=body_transaction.get("token"),
                status=False,
                user_id=body.chat_id
            )
            db.session.add(tx_create)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logger.error(f"ERROR: {error}")
            raise error
        return result.get("createTxHex")

    @staticmethod
    def _sign_send_transaction(create_tx_hash: str, private_keys: CRYPTOPrivateKey, network: str, chat_id: int) -> bool:
        method, url = CryptoEndpointType.get_send_transaction(network=network)
        data = {
            "createTxHex": create_tx_hash,
            "privateKeys": private_keys
        }
        result = Client.request(method=method, url=url, **data)
        try:
            transaction: WalletTransactionModel = WalletTransactionModel.query.filter_by(
                transaction_hash=result.get("transactionHash"),
                user_id=chat_id,
                network=network.split("_")[0].upper()
            ).first()
            transaction.status = True
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logger.error(f"ERROR: {error}")
            return False
        return True

    @staticmethod
    def create_transaction(body: BodyTransaction) -> ResponseCreateTransaction:
        """Get optimal fee for transaction"""
        method, url = CryptoEndpointType.get_optimal_fee_url(network=body.network, inputs=body.inputs,
                                                             outputs=body.outputs)
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

    @staticmethod
    def send_transaction(body: BodyTransaction) -> ResponseSendTransaction:
        return ResponseSendTransaction(
            message=Transaction._sign_send_transaction(
                create_tx_hash=Transaction._create_transaction(body=body),
                private_keys=WalletModel.query.filter_by(user_id=body.chat_id, network=body.network.split("_")[0]).all(),
                network=body.network,
                chat_id=body.chat_id
            )
        )

