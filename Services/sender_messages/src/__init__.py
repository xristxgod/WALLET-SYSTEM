import json
from typing import Optional, Dict

import aio_pika
import asyncpg

from src.utils import Errors, Utils
from config import Config, logger, decimals

class DB:
    """
    <<<--------------------------------------------------->>>
    tabel = wallet
        id: Integer Primary Key
        network: String(256) NOT NULL
        address: String(256) NOT NULL UNIQUE = TRUE
        private_key: String(256) NOT NULL UNIQUE = TRUE
        public_key: String(256) NOT NULL UNIQUE = TRUE
        passphrase: String(256) NOT NULL UNIQUE = TRUE
        mnemonic_phrase: String(256) NOT NULL UNIQUE = TRUE
        accounts: JSON NOT NULL
        user_id: Integer Foreign Key To user_model
    <<<--------------------------------------------------->>>
    table = wallet_transaction
        id: Integer Primary Key
        network: String(256) NOT NULL
        time: INTEGER NOT NULL
        transaction_hash: String(256) NOT NULL UNIQUE = TRUE
        fee: DECIMAL NOT NULL
        amount: DECIMAL NOT NULL
        senders: JSON NOT NULL
        recipients: JSON NOT NULL
        token: String(256) NOT NULL
        status: BOOL NOT NULL DEFAULT = FALSE
        user_id: Integer Foreign Key To user_model
    <<<--------------------------------------------------->>>
    """
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

    @staticmethod
    async def __insert_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            await connection.execute(sql)
            return True
        except Exception as error:
            await RabbitMQ.send_to_checker(
                error=error, msg="ERROR 'DB' STEP 56", title="DEMON", func=DB.__select_method.__name__
            ),
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def update_transaction(transaction_hash: str, user_id: int) -> bool:
        return await DB.__insert_method(
            "UPDATE wallet_transaction "
            "SET status = 1 "
            f"WHERE transaction_hash = '{transaction_hash}' AND user_id = {user_id}"
        )

    @staticmethod
    async def insert_transaction(transaction_info: Dict, user_id: int, network: str):
        return await DB.__insert_method(
            "INSERT INTO wallet_transaction "
            "(network, time, transaction_hash, fee, amount, senders, recipients, token, status, user_id) VALUES "
            f"('{network}', {transaction_info['time']}, '{transaction_info['transaction_hash']}', "
            f"{decimals.create_decimal(transaction_info['fee'])}, {decimals.create_decimal(transaction_info['amount'])} "
            f"'{transaction_info['senders']}', '{transaction_info['recipients']}', '{transaction_info['token']}', 1,"
            f" {user_id});"
        )

    @staticmethod
    async def get_chat_id_by_wallet_address(wallet_address: str, network: str) -> int:
        data = await DB.__select_method(
            "SELECT chat_id FORM user_model "
            "WHERE id = ("
            f"SELECT user_id FROM wallet WHERE network = '{network}' AND address = '{wallet_address}');"
        )
        return [chat_id[0] for chat_id in data][0]

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