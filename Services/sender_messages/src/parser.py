import asyncio
import json
from typing import Optional, Dict, List

import aio_pika

from config import Config, logger

class Parser:

    @staticmethod
    async def processing_transaction(txs_data: List[Dict]):
        tx_list = []
        for tx_data in txs_data:
            pass

    @staticmethod
    async def processing_message(data: List[Dict]):
        network, token = data[0].get("network").split("-")
        transaction_info: Dict = data[1]
        from_address = transaction_info.get("address")
        transaction = await Parser.processing_transaction(txs_data=transaction_info.get("transactions"))


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


