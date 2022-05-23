from typing import Optional, Union, Tuple, List, Dict

import asyncpg

from config import Config
from api.utils.types import TG_CHAT_ID

class DB:
    DATABASE_URL = Config.DATABASE_URL

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
    async def get_all_transactions_time(status: Tuple[int, int] = (0, 1)) -> List[Dict]:
        return await DB.__select_method(
            sql="SELECT user_id, transaction_hash, time, status FROM transaction_model WHERE status IN ($1, $2);",
            data=status
        )

    @staticmethod
    async def delete_transaction(user_id: TG_CHAT_ID, transaction_hash: str, status: int = 0) -> bool:
        return await DB.__insert_method(
            sql="DELETE FROM transaction_model WHERE user_id = $1 AND transaction_hash = $2 AND status = $3;",
            data=(user_id, transaction_hash, status)
        )

if __name__ == '__main__':
    import asyncio
    print(asyncio.run(DB.get_all_transactions_time()))