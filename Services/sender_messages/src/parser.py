import asyncio
import json
from typing import Optional, Dict, List

import aio_pika

from src.__init__ import DB
from src.utils import Utils
from src.sender import Sender
from config import Config, logger

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
                    tx_hash=tx_data.get("transactionHash"), network=network, user_id=user_id, status=True
                )
                is_new = False
            else:
                # If the transaction was new and was not found in the database
                result = await DB.add_new_transaction(
                    network=network, time=tx_data.get("time"), transaction_hash=tx_data.get("transactionHash"),
                    fee=tx_data.get("fee"), amount=tx_data.get("amount"), senders=tx_data.get("senders"),
                    recipients=tx_data.get("recipients"), token=token, status=True, user_id=user_id
                )
                is_new = True
            if not result:
                raise Exception("The transaction was not recorded in the database!")

            is_sender = False
            if Utils.is_address(address=address, data=tx_data.get("senders")):
                is_sender = True

            returned_data["forApiBalanceAddOrDec"].append({
                "chat_id": user_id,
                "username": await DB.get_username_by_user_id(user_id=user_id),
                "network": f"{network.upper()}-{token.upper()}",
                "amount": tx_data.get("amount"),
                "transactionHash": tx_data.get("transactionHash"),
                "method": "dec" if is_sender else "add"
            })

            if not is_new:
                returned_data["forApiTransactionSend"].append({
                    "chat_id": user_id,
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

async def processing_message(message) -> None:
    """
    Decrypt the message from the queue and send it for forwarding.
    :param message: Message from queue
    """
    try:
        async with message.process():
            msg: List[Dict] = json.loads(message.body)
            logger.error(f"MESSAGE: {msg}")
        await Parser.processing_message(data=msg)
    except Exception as error:
        # Resend method
        pass

async def run(loop):
    """Infinitely included script"""
    while True:
        try:
            connection = None
            while connection is None or connection.is_closed:
                try:
                    # Connect to RabbitMQ
                    connection = await aio_pika.connect_robust(Config.RABBITMQ_URL, loop=loop)
                finally:
                    logger.error(f'WAIT CONNECT TO RABBITMQ')
                await asyncio.sleep(2)
            async with connection:
                # Connect to the RabbitMQ channel
                channel = await connection.channel()
                # Connections to the queue in RabbitMQ by name
                queue = await channel.declare_queue(Config.RABBITMQ_QUEUE_FOR_SENDER, durable=True)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        await processing_message(message=message)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            await asyncio.sleep(10)
            continue


