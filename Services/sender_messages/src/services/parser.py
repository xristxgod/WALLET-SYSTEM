from typing import Dict, List, Tuple

from src.__init__ import DB
from src.utils.utils import Utils
from src.utils.types import NETWORK, TGChatID, CryptAddress
from src.utils.schemas import HeadMessage, BodyMessage, BodyTransaction
from src.utils.schemas import BodyApiBalance, BodyApiTransaction, ReturnedData
from src.services.sender import Sender

class Parser:
    """This class is used to unpack the transaction and send it to the bot"""
    @staticmethod
    async def processing_transaction(
            txs_data: List[BodyTransaction],
            network: NETWORK,
            token: str,
            user_id: TGChatID,
            address: CryptAddress
    ) -> ReturnedData:
        """
        Packaging of the transaction
        :param txs_data: Transactions data
        :param network: Node Network
        :param token: Token
        :param user_id: User id
        """
        returned_data = {"forApiBalance": [], "forApiTransaction": []}
        for tx_data in txs_data:
            if await DB.get_transaction_status(tx_hash=tx_data.transactionHash, network=network) is not None:
                # If the transaction was found in the database
                result = await DB.update_transaction(
                    tx_hash=tx_data.transactionHash, network=network, user_id=user_id, status=2
                )
                is_new = False
            else:
                # If the transaction was new and was not found in the database
                result = await DB.add_new_transaction(
                    network=network, time=tx_data.time, transaction_hash=tx_data.transactionHash,
                    fee=tx_data.fee, amount=tx_data.amount, inputs=tx_data.inputs,
                    outputs=tx_data.outputs, token=token, status=2, user_id=user_id
                )
                is_new = True
            if not result:
                raise Exception("The transaction was not recorded in the database!")

            is_sender = False
            if Utils.is_address(address=address, data=tx_data.inputs):
                is_sender = True
            returned_data["forApiBalance"].append(BodyApiBalance(
                chatID=user_id, username=await DB.get_username_by_user_id(user_id=user_id),
                network=f"{network.upper()}-{token.upper()}", amount=tx_data.amount,
                transactionHash=tx_data.transactionHash, method="dec" if is_sender else "add"
            ))

            if not is_new:
                returned_data["forApiTransaction"].append(BodyApiTransaction(
                    chatID=user_id, transactionHash=tx_data.transactionHash, inputs=tx_data.inputs,
                    outputs=tx_data.outputs, amount=tx_data.amount, fee=tx_data.fee,
                    network=f"{network.upper()}-{token.upper()}", status=2, method="send"

                ))
        return ReturnedData(
            forApiBalance=returned_data.get("forApiBalance"), forApiTransaction=returned_data.get("forApiTransaction")
        )

    @staticmethod
    async def processing_message(data: Tuple[HeadMessage, BodyMessage]) -> None:
        """
        Unpacking a message
        :param data: Data from the message
        """
        network, token = data[0].network.split("-")
        transaction_info: BodyMessage = data[1]
        from_address = transaction_info.address
        transactions_for_send: ReturnedData = await Parser.processing_transaction(
            txs_data=transaction_info.transactions, token=token, network=network, address=from_address,
            user_id=(await DB.get_user_id_by_wallet_address(address=from_address, network=network))
        )
        if len(transactions_for_send.forApiBalance) > 0:
            for tx_data in transactions_for_send.forApiBalance:
                await Sender.send_to_users_method(**tx_data)
        if len(transactions_for_send.forApiTransaction) > 0:
            for tx_data in transactions_for_send.forApiTransaction:
                await Sender.send_to_transaction_method(**tx_data)