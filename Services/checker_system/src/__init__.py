import json
from typing import Optional

import asyncpg
import aio_pika

from src.utils import Errors, Utils
from config import Config, logger

class DB:
    @staticmethod
    async def __select_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            return await connection.fetch(sql)
        except Exception as error:
            await RabbitMQ.send_to_checker(
                error=error, msg="ERROR 'DB' STEP 56", title="DEMON", func=DB.__select_method.__name__
            ),
            raise error
        finally:
            if connection is not None:
                await connection.close()

class RabbitMQ:

    RABBITMQ_URL = Config.RABBITMQ_URL
    RABBITMQ_QUEUE_SENDER = Config.RABBITMQ_QUEUE_SENDER
    RABBITMQ_ROUTING_KEY_SENDER = Config.RABBITMQ_ROUTING_KEY_SENDER

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