import asyncio
import json
from typing import Optional, Dict, List

import aio_pika

from src.__init__ import DB
from src.utils import Utils
from config import Config, logger

class Parser:
    """This class is used to unpack the transaction and send it to the bot"""
    @staticmethod
    async def processing_transaction(
            txs_data: List[Dict], network: str, token: str, user_id: int, address: str
    ) -> List[Dict]:
        """
        Packaging of the transaction
        :param txs_data: Transactions data
        :param network: Node Network
        :param token: Token
        :param user_id: User id
        """
        tx_list = {
            "is_add": [],
            "is_upd": []
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





    @staticmethod
    async def processing_message(data: List[Dict]):
        """
        Unpacking a message
        :param data: Data from the message
        """
        network, token = data[0].get("network").split("-")
        transaction_info: Dict = data[1]
        from_address = transaction_info.get("address")
        transaction: List[Dict] = await Parser.processing_transaction(
            txs_data=transaction_info.get("transactions"),
            token=token,
            network=network,
            user_id=(await DB.get_user_id_by_wallet_address(address=from_address, network=network))
        )


async def processing_message(message):
    """
    Decrypt the message from the queue and send it for forwarding.
    :param message: Message from queue
    """
    async with message.process():
        msg: List[Dict] = json.loads(message.body)
        logger.error(f"MESSAGE: {msg}")
    await Parser.processing_message(data=msg)

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


