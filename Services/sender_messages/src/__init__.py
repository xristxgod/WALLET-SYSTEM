from typing import Optional, Dict, List
import asyncpg

from config import Config

class DB:
    @staticmethod
    async def __select_method(sql) -> List:
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
    async def __insert_method(sql):
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(Config.DATABASE_URL)
            await connection.execute(sql)
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()