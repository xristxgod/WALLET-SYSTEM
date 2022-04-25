import json
from typing import Optional, Dict, List

import aio_pika
import asyncpg

from src.utils import Errors
from config import logger, Config

class DB:
    """
    <<<--------------------------------------------------->>>
    tabel = {coin} << coins.json >>
        time: BIGINT Primary Key
        address: DECIMAL
    <<<--------------------------------------------------->>>
    """
    @staticmethod
    async def __insert_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            await connection.execute(sql)
            return True
        except Exception as error:
            logger.error(f'ERROR DB STEP 22: {error}')
            await Errors.write_to_error(error=error, msg="ERROR 'DB' STEP 22")
            await RabbitMQ.send_to_checker(
                error=error, msg="ERROR 'DB' STEP 22", title="COINS", func=DB.__insert_method.__name__
            ),
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def create_coin_tabel(coin: str):
        return await DB.__insert_method(
            """
                CREATE TABLE IF NOT EXISTS {coin}(
                    "time" bigint primary key,
                    "price" decimal
                );
            """
        )

    @staticmethod
    async def insert_coin_currency(coin: str, time: int, value: float):
        return await DB.__insert_method((
            f"INSERT INTO {coin} (time, price) VALUES ({time}, {value})"
        ))


class RabbitMQ:

    RABBITMQ_URL = Config.RABBITMQ_URL

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
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def send_to_checker(error: Exception, msg: str, title: str, func: str):
        await RabbitMQ.__send_message(
            msg=aio_pika.Message(await Errors.write_to_send(error=error, msg=msg, title=title, func=func)),
            queue_name=RabbitMQ.RABBITMQ_QUEUE_CHECKER,
            routing_key=RabbitMQ.RABBITMQ_ROUTING_KEY_CHECKER
        )