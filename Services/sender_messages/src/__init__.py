import json
from typing import Optional

import aio_pika

from src.utils import Errors, Utils
from config import Config, logger

class RabbitMQ:

    RABBITMQ_URL = Config.RABBITMQ_URL
    DEMONS_QUEUE_SENDER = Config.DEMONS_QUEUE_SENDER
    DEMONS_ROUTING_KEY_SENDER = Config.DEMONS_ROUTING_KEY_SENDER

    RABBITMQ_QUEUE_CHECKER = Config.RABBITMQ_QUEUE_CHECKER
    RABBITMQ_ROUTING_KEY_CHECKER = Config.RABBITMQ_ROUTING_KEY_CHECKER

    @staticmethod
    async def __send_message(msg: aio_pika.Message, queue_name: str, routing_key: str) -> None:
        connection: Optional[aio_pika.Connection] = None
        try:
            connection = await aio_pika.connect_robust(url=RabbitMQ.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(queue_name)
            await channel.default_exchange.publish(message=msg, routing_key=routing_key)
        except Exception as error:
            logger.error(f'ERROR RABBIT MQ SEND STEP 96: {error}')
            await Errors.write_to_error(error=error, msg="ERROR 'RABBITMQ' STEP 96")
            await Errors.write_to_helper_file(json.dumps(msg))
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def send_to_sender_demons(values: json):
        await RabbitMQ.__send_message(
            msg=aio_pika.Message(values),
            queue_name=RabbitMQ.DEMONS_QUEUE_SENDER,
            routing_key=RabbitMQ.RABBITMQ_ROUTING_KEY_CHECKER
        )

    @staticmethod
    async def send_to_checker(error: Exception, msg: str, title: str, func: str):
        await RabbitMQ.__send_message(
            msg=aio_pika.Message(await Errors.write_to_send(error=error, msg=msg, title=title, func=func)),
            queue_name=RabbitMQ.RABBITMQ_QUEUE_CHECKER,
            routing_key=RabbitMQ.RABBITMQ_ROUTING_KEY_CHECKER
        )