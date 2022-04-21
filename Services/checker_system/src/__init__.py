import json
from typing import Optional, List

import asyncpg
import aio_pika

from src.utils import Errors, Utils
from config import Config, logger

class DB:
    """
    <<<--------------------------------------------------->>>
    table = user_model
        id: Integer Primary Key
        username: String(256) NOT NULL
        chat_id: INTEGER NOT NULL UNIQUE = TRUE
        is_admin BOOL NOT NULL DEFAULT = FALSE
    <<<--------------------------------------------------->>>
    """
    DATABASE_URL = Config.DATABASE_URL

    @staticmethod
    async def __select_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(DB.DATABASE_URL)
            return await connection.fetch(sql)
        except Exception as error:
            await Errors.write_to_error(error=error, msg="ERROR DB STEP 17")
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_admin_ids() -> List:
        return [_id[0] for _id in await DB.__select_method("SELECT chat_id FROM user_model WHERE is_admin=1;")]


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