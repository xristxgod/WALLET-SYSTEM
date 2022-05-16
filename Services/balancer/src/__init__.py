import asyncio
from datetime import datetime, timedelta
from typing import Optional, Union, List, Tuple, Dict

import asyncpg
import aio_pika

from src.types import NETWORK
from src.utils import Utils
from config import Config, logger

lock = asyncio.Lock()

class DB:
    DATABASE_URL = Config.DATABASE_URL

    @staticmethod
    async def __insert_method(sql: str, data: Optional[Union[List, Tuple]] = ()):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(DB.DATABASE_URL)
            await connection.execute(sql, data)
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def update_transaction(chat_id: int, network: NETWORK, status: int = 2, last_status: str = 1, **data) -> bool:
        return await DB.__insert_method(
            sql=(
                "UPDATE transaction_model "
                "SET status = $1 AND transaction_hash = $2 "
                "WHERE user_id = $3 AND network = $4 AND status = $5;"
            ),
            data=(status, data.get("transaction_hash"), chat_id, network, last_status)
        )

class RabbitMQ:

    RABBITMQ_URL = Config.RABBITMQ_URL
    QUEUE_BALANCER = Config.RABBITMQ_QUEUE_FOR_BALANCER

    @staticmethod
    async def resend_message(message) -> bool:
        connection = None
        try:
            connection = await aio_pika.connect_robust(RabbitMQ.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(RabbitMQ.QUEUE_BALANCER, durable=True)
            await channel.default_exchange.publish(
                message=message,
                routing_key=RabbitMQ.QUEUE_BALANCER
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            await Utils.write_to_file(value=message)
        finally:
            if connection is not None and not connection.is_closed:
                await connection.close()

class Observer:
    def __init__(self):
        # self._chat_ids = {chat_id: [datetime, data]}
        self._chat_ids = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Observer, cls).__new__(cls)
        return cls.instance

    async def can_go(self, chat_id: int, data: List[Dict]) -> (bool, int):
        async with lock:
            if chat_id not in self._chat_ids.keys():
                self._chat_ids.update({chat_id: [datetime.now(), data]})
                return True, 0
            seconds = (datetime.now() - self._chat_ids[chat_id][0]).seconds
            if seconds > 60:
                self._chat_ids.update({chat_id: [datetime.now(), data]})
                return True, 0
            else:
                self._chat_ids.update({chat_id: [self._chat_ids[chat_id][0] + timedelta(seconds=60 - seconds), data]})
                return False, 60 - seconds

observer = Observer()