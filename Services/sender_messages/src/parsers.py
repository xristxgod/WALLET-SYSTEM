import asyncio
import json
from typing import Optional, Dict

import aio_pika

from src.sender import SenderBot
from src.__init__ import RabbitMQ, DB
from src.utils import Errors, BotUtils, ParserDemonUtils
from config import Config, logger

class ParserDemon:


    @staticmethod
    async def packed_message(network: str, txn: Dict, user_ids: Dict, address: str):
        if await DB.get_transaction(transaction_hash=txn["transactionHash"]):
            await DB.update_transaction(
                transaction_hash=txn["transactionHash"], user_id=user_ids["user_id"], network=network
            )
        else:
            await DB.insert_transaction(
                transaction_info=txn, user_id=user_ids["user_id"], network=network
            )
        if address == txn[0]["recipients"]:
            status = "add"      # Add balance
        else:
            status = "del"      # Del balance
        coin = ParserDemonUtils.get_coin(network=network)
        text = BotUtils.generate_report_add(
            tx_info=txn,
            network=network,
            status=status,
            coin=coin["amount"],
            fee_coin=coin["fee"]
        )
        await SenderBot.send_to_bot(text=text, chat_id=user_ids["chat_id"])



    @staticmethod
    async def processing_message_by_demons(message: aio_pika.IncomingMessage):
        """
        Decrypt the message from the queue and send it for forwarding.
        :param message: Message from queue
        """
        async with message.process():
            msg: Dict = json.loads(message.body)
            logger.error(f"GET INIT MSG: {msg}")
            network = msg[0]["network"].upper()
            await ParserDemon.packed_message(
                network=network,
                txn=msg[1]["transactions"][0],
                user_ids=(await DB.get_chat_id_by_wallet_address(wallet_address=msg[1]["address"], network=network)),
                address=msg[1]["address"]
            )



    @staticmethod
    async def get_message_from_demons(loop):
        while True:
            connection: Optional[aio_pika.RobustConnection] = None
            try:
                while connection is None or connection.is_closed:
                    try:
                        # Connect to RabbitMQ by url
                        connection: aio_pika.RobustConnection = await aio_pika.connect_robust(Config.RABBITMQ_URL, loop=loop)
                    finally:
                        logger.error("WAIT CONNECT TO RABBITMQ")
                    await asyncio.sleep(2)
                async with connection:
                    # Connect to the RabbitMQ channel
                    channel: aio_pika.Channel = await connection.channel()
                    # Connections to the queue in RabbitMQ by name.
                    queue = await channel.declare_queue(Config.DEMONS_QUEUE_SENDER, durable=True)
                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            await ParserDemon.processing_message_by_demons(message=message)
            except Exception as error:
                logger.error("ERROR SENDER DEMON STEP 17")
                await Errors.write_to_error(error=error, msg="ERROR SENDER DEMON STEP 17")
                await RabbitMQ.send_to_checker(
                    error=error,
                    msg="ERROR 'SenderDemon' STEP 17",
                    title="SENDER",
                    func=ParserDemon.get_message_from_demons.__name__
                )