import asyncio
from datetime import datetime, timedelta
from typing import Union, Optional, List, Tuple, Dict

import aio_pika
import asyncpg

from src.utils import Utils
from config import Config, logger

lock = asyncio.Lock()

class DB:
    @staticmethod
    async def __select_method(sql: str, data: Optional[Union[List, Tuple]] = ()) -> List:
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            return await connection.fetch(sql, *data)
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def __insert_method(sql: str, data: Optional[Union[List, Tuple]] = ()):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            await connection.execute(sql, data)
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_user_id_by_wallet_address(address: str, network: str) -> Optional[int]:
        data = await DB.__select_method(
            sql="SELECT user_id FROM wallet_model WHERE address = $1 AND network = $2;",
            data=(address, network.upper()))
        return data[0] if data == 1 else None

    @staticmethod
    async def get_transaction_status(tx_hash: str, network: str) -> Optional[bool]:
        data = await DB.__select_method(
            sql="SELECT status FROM wallet_transaction_model WHERE transaction_hash = $1 AND network = $2;",
            data=(tx_hash, network.upper())
        )
        return data[0] if data == 1 else None

    @staticmethod
    async def add_new_transaction(**data) -> bool:
        """Add a new transaction"""
        return await DB.__insert_method(
            sql=(
                "INSERT INTO wallet_transaction_model "
                "(network, time, transaction_hash, fee, amount, senders, recipients, token, status, user_id)"
                "VALUES"
                "($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);"
            ),
            data=(
                data.get("network"), data.get("time"), data.get("transaction_hash"), data.get("fee"),
                data.get("amount"), data.get("senders"), data.get("recipients"), data.get("token"),
                data.get("status"), data.get("user_id")
            )
        )

    @staticmethod
    async def update_transaction(tx_hash: str, network: str, user_id: int, status: int = 2) -> bool:
        """Update the transaction status"""
        return await DB.__insert_method(
            sql=(
                "UPDATE wallet_transaction_model "
                "SET status = $1 "
                "WHERE transaction_hash = $2 AND network = $3 AND user_id = $4;"
            ),
            data=(status, tx_hash, network, user_id)
        )

    @staticmethod
    async def get_username_by_user_id(user_id: int) -> Optional[str]:
        data = await DB.__select_method(
            sql="SELECT username FROM user_model WHERE id = $1",
            data=(user_id,)
        )
        return data[0] if data == 1 else None

class RabbitMQ:

    @staticmethod
    async def resend_message(message) -> bool:
        connection = None
        try:
            connection = await aio_pika.connect_robust(Config.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(Config.RABBITMQ_QUEUE_FOR_SENDER, durable=True)
            await channel.default_exchange.publish(
                message=message,
                routing_key=Config.RABBITMQ_QUEUE_FOR_SENDER
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            await Utils.write_to_file(value=message)
        finally:
            if connection is not None and not connection.is_closed:
                await connection.close()

class SenderMethod:
    """Send a message to the bot alert api"""
    API_URL = Config.BOT_ALERT_API_URL
    USERS_METHOD = API_URL + "/api/user/<method>"
    TRANSACTION_METHOD = API_URL + "/api/transaction/<method>"

    @staticmethod
    def _get_url(api: str, method: str = None):
        return api.replace("<method>", method)

    @staticmethod
    def _get_headers() -> Optional[Dict]:
        """There should be an AUTH API and other things that are needed for the head."""
        pass

class Observer:
    def __init__(self):
        self._addresses = {}
        # self._addresses = {"WALLET_ADDRESS": data}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Observer, cls).__new__(cls)
        return cls.instance

    async def can_go(self, address: str, data: List[Dict]) -> (bool, int):
        async with lock:
            if address not in self._addresses.keys():
                self._addresses.update({address: [datetime.now(), data]})
                return True, 0
            seconds = (datetime.now() - self._addresses[address][0]).seconds
            if seconds > 60:
                self._addresses.update({address: [datetime.now(), data]})
                return True, 0
            else:
                self._addresses.update({address: [self._addresses[address][0] + timedelta(seconds=60 - seconds), data]})
                return False, 60 - seconds


observer = Observer()