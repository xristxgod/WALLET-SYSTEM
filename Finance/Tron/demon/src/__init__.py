import json
from typing import Dict, List, Optional, Union

import asyncpg
import aio_pika

from src.utils import Errors, Utils
from src.types import TAddress, TRON_NETWORK_INDEX, CREATE_TRANSACTION_STATUS_NUMBER
from config import Config, logger

TOKENS = [
    {
        "token": "USDT",
        "address": "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA",
        "decimals": 6,
        "token_info": {"bandwidth": 345, "feeLimit": 1000, "isBalanceNotNullEnergy": 14631, "isBalanceNullEnergy": 29631},
    }
]

class DB:
    DATABASE_URL = Config.DATABASE_URL

    @staticmethod
    async def __select_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(DB.DATABASE_URL)
            return await connection.fetch(sql)
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_addresses() -> List:
        data = await DB.__select_method(sql=F"SELECT address FROM wallet_model WHERE network = {TRON_NETWORK_INDEX};")
        return [address[0] for address in data]

    @staticmethod
    async def get_all_transactions_hash() -> List:
        data = await DB.__select_method(
            sql=f"SELECT transaction_hash FROM transaction_model WHERE status={CREATE_TRANSACTION_STATUS_NUMBER};"
        )
        return [tx_hash[0] for tx_hash in data]

    @staticmethod
    async def get_transaction_hash(transaction_hash: str) -> Dict:
        return dict(
            await DB.__select_method(
                sql=(
                    f"SELECT transaction_hash FROM transaction_model WHERE status={CREATE_TRANSACTION_STATUS_NUMBER} "
                    f"AND transaction_hash='{transaction_hash}';")
            )
        )

    @staticmethod
    async def get_all_tokens() -> List[Dict]:
        if Config.NETWORK == "TESTNET":
            return TOKENS
        else:
            return await DB.__select_method(
                sql=f"SELECT address, decimals, token_info FROM token_model WHERE network={TRON_NETWORK_INDEX}"
            )

    @staticmethod
    async def get_token_info(address: TAddress) -> Union[Dict, None]:
        try:
            if Config.NETWORK == "TESTNET":
                data = [t for t in TOKENS if t["address"] == address][0]
            else:
                data = await DB.__select_method((
                    f"SELECT token, address, decimals, token_info FROM token_model "
                    f"WHERE address = '{address}' AND network = {TRON_NETWORK_INDEX};"
                ))
            return {
                "token": data["token"],
                "address": data["address"],
                "decimals": data["decimals"],
                "token_info": data["token_info"],
            }
        except Exception:
            return None

    @staticmethod
    async def get_all_token_address() -> List[TAddress]:
        if Config.NETWORK == "TESTNET":
            return [symbol["address"] for symbol in TOKENS]
        else:
            return [
                symbol["address"]
                for symbol in dict(await DB.__select_method(
                    sql=f"SELECT address FROM token_model WHERE network={TRON_NETWORK_INDEX};"
                ))
            ]

class RabbitMQ:
    RABBITMQ_URL = Config.RABBITMQ_URL
    RABBITMQ_QUEUE_FOR_SENDER = Config.RABBITMQ_QUEUE_FOR_SENDER

    @staticmethod
    async def __send_message(msg: aio_pika.Message, queue_name: str) -> None:
        connection = None
        try:
            connection = await aio_pika.connect_robust(url=RabbitMQ.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(queue_name)
            await channel.default_exchange.publish(
                routing_key=queue_name,
                message=msg
            )
        except Exception as error:
            logger.error(f'ERROR RABBIT MQ SEND STEP 96: {error}')
            await Errors.write_to_error(error=error, msg="ERROR 'RABBITMQ' STEP 96")
            await Errors.write_to_helper_file(json.dumps(msg))
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def send_to_sender(values: json):
        await RabbitMQ.__send_message(
            msg=aio_pika.Message(values),
            queue_name=RabbitMQ.RABBITMQ_QUEUE_FOR_SENDER,
        )