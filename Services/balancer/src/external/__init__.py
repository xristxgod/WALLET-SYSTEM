from typing import Optional, Union, List, Tuple

import asyncpg

from src.types import NETWORK
from config import Config

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