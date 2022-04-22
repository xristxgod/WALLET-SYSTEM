import asyncio
from typing import Optional

import aio_pika

from src.__init__ import RabbitMQ
from src.utils import Errors
from config import Config, logger

class ParserDemon:

    @staticmethod
    async def processing_message_by_demons(message: aio_pika.IncomingMessage):
        pass

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