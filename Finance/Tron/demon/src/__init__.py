import json
from typing import Dict, List, Optional, Union

import asyncpg
import aio_pika

from src.utils import Errors
from src.types import TAddress
from config import Config, logger

TOKENS = [
    {
        "token": "USDT",
        "address": "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA",
        "decimals": 6,
        "token_info": '{"bandwidth": 345, "feeLimit": 1000, "isBalanceNotNullEnergy": 14631, "isBalanceNullEnergy": 29631}',
    }
]

class DB:
    """
    <<<--------------------------------------------------->>>
    table = token_model
        id: Integer Primary Key
        network: String(256) NOT NULL UNIQUE = TRUE
        token: String(256) NOT NULL
        address: String(256) NOT NULL
        decimals: String(256) NOT NULL UNIQUE = TRUE
        token_info: JSON NOT NULL
    <<<--------------------------------------------------->>>
    tabel = tron_wallet
        id: Integer Primary Key
        address: String(256) NOT NULL UNIQUE = TRUE
        private_key: String(256) NOT NULL UNIQUE = TRUE
        public_key: String(256) NOT NULL UNIQUE = TRUE
        passphrase: String(256) NOT NULL UNIQUE = TRUE
        mnemonic_phrase: String(256) NOT NULL UNIQUE = TRUE
        accounts: JSON NOT NULL
    <<<--------------------------------------------------->>>
    table = tron_transaction
        id: Integer Primary Key
        time: INTEGER NOT NULL
        transaction_hash: String(256) NOT NULL UNIQUE = TRUE
        fee: DECIMAL NOT NULL
        amount: DECIMAL NOT NULL
        senders: JSON NOT NULL
        recipients: JSON NOT NULL
        token: String(256) NOT NULL
        status: BOOL NOT NULL DEFAULT = FALSE
    <<<--------------------------------------------------->>>
    """
    @staticmethod
    async def __select_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            return await connection.fetch(sql)
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_addresses() -> List:
        data = await DB.__select_method(sql="SELECT address FROM tron_wallet")
        return [address[0] for address in data]

    @staticmethod
    async def get_all_transactions_hash() -> List:
        data = await DB.__select_method(sql="SELECT transaction_hash FROM tron_transaction WHERE status=0")
        return [tx_hash[0] for tx_hash in data]

    @staticmethod
    async def get_all_tokens() -> List[Dict]:
        if Config.NODE_NETWORK == "TEST":
            return TOKENS
        else:
            return await DB.__select_method(
                sql="SELECT address, decimals, token_info FROM token_model WHERE network='TRON'"
            )

    @staticmethod
    async def get_transaction_hash(transaction_hash: str) -> Dict:
        return dict(
            await DB.__select_method(
                sql=f"SELECT * FROM tron_transaction WHERE status=0 and transaction_id='{transaction_hash}';"
            )
        )

    @staticmethod
    async def get_token_info(address: TAddress, network: str = "TRON") -> Union[Dict, None]:
        try:
            if Config.NODE_NETWORK == "TEST":
                data = [t for t in TOKENS if t["address"] == address][0]
            else:
                data = await DB.__select_method((
                    f"SELECT token, address, decimals, token_info FROM token_model "
                    f"WHERE address = '{address}' AND network = '{network.upper()}';"
                ))
            return {
                "token": data["token"],
                "address": data["address"],
                "decimals": data["decimals"],
                "token_info": json.loads(data["token_info"]),
            }
        except Exception:
            return None

class RabbitMQ:

    @staticmethod
    async def send_message(msg: aio_pika.Message, queue_name: str, routing_key: str) -> None:
        connection: Optional[aio_pika.Connection] = None
        channel: Optional[aio_pika.Channel] = None
        try:
            connection = await aio_pika.connect_robust(url=Config.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(queue_name)
            await channel.default_exchange.publish(message=msg, routing_key=routing_key)
        except Exception as error:
            logger.error(f'ERROR RABBIT MQ SEND STEP 96: {error}')
            await Errors.write_to_error(error=error, msg="RABBIT MQ NOT SEND | STEP 96")
            await Errors.write_to_helper_file(json.dumps(msg))
        finally:
            if connection is not None:
                await connection.close()