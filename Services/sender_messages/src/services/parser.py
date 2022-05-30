from typing import Dict, List

from src.__init__ import DB
from src.utils.utils import Utils
from src.services.sender import Sender

class Parser:
    """This class is used to unpack the transaction and send it to the bot"""
    @staticmethod
    async def processing_transaction(txs_data: List[Dict], network: str, token: str, user_id: int, address: str) -> Dict:
        """
        Packaging of the transaction
        :param txs_data: Transactions data
        :param network: Node Network
        :param token: Token
        :param user_id: User id
        """
        returned_data = {
            "forApiBalanceAddOrDec": [],
            "forApiTransactionSend": []
        }
        for tx_data in txs_data:
            if await DB.get_transaction_status(tx_hash=tx_data.get("transactionHash"), network=network) is not None:
                # If the transaction was found in the database
                result = await DB.update_transaction(
                    tx_hash=tx_data.get("transactionHash"), network=network, user_id=user_id, status=2
                )
                is_new = False
            else:
                # If the transaction was new and was not found in the database
                result = await DB.add_new_transaction(
                    network=network, time=tx_data.get("time"), transaction_hash=tx_data.get("transactionHash"),
                    fee=tx_data.get("fee"), amount=tx_data.get("amount"), senders=tx_data.get("senders"),
                    recipients=tx_data.get("recipients"), token=token, status=2, user_id=user_id
                )
                is_new = True
            if not result:
                raise Exception("The transaction was not recorded in the database!")

            is_sender = False
            if Utils.is_address(address=address, data=tx_data.get("senders")):
                is_sender = True

            returned_data["forApiBalanceAddOrDec"].append({
                "chatID": user_id,
                "username": await DB.get_username_by_user_id(user_id=user_id),
                "network": f"{network.upper()}-{token.upper()}",
                "amount": tx_data.get("amount"),
                "transactionHash": tx_data.get("transactionHash"),
                "method": "dec" if is_sender else "add"
            })

            if not is_new:
                returned_data["forApiTransactionSend"].append({
                    "chatID": user_id,
                    "transactionHash": tx_data.get("transactionHash"),
                    "fromAddress": address,
                    "toAddress": Utils.get_addresses_for_send(addresses_data=tx_data.get("recipients")),
                    "amount": tx_data.get("amount"),
                    "fee": tx_data.get("fee"),
                    "network": f"{network.upper()}-{token.upper()}",
                    "status": True,
                    "method": "send"
                })
        return returned_data

    @staticmethod
    async def processing_message(data: List[Dict]) -> None:
        """
        Unpacking a message
        :param data: Data from the message
        """
        network, token = data[0].get("network").split("-")
        transaction_info: Dict = data[1]
        from_address = transaction_info.get("address")
        transactions_for_send: Dict = await Parser.processing_transaction(
            txs_data=transaction_info.get("transactions"), token=token, network=network, address=from_address,
            user_id=(await DB.get_user_id_by_wallet_address(address=from_address, network=network))
        )
        if len(transactions_for_send.get("forApiBalanceAddOrDec")) > 0:
            for tx_data in transactions_for_send.get("forApiBalanceAddOrDec"):
                await Sender.send_to_users_method(**tx_data)
        if len(transactions_for_send.get("forApiTransactionSend")) > 0:
            for tx_data in transactions_for_send.get("forApiTransactionSend"):
                await Sender.send_to_transaction_method(**tx_data)