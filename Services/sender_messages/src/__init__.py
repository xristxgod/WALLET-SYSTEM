from typing import Union, Optional, List, Tuple, Dict
import asyncpg

from src.utils import Utils
from config import Config

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