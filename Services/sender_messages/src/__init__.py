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

    @staticmethod
    async def get_user_id_by_wallet_address(address: str, network: str) -> int:
        return [data[0] for data in (await DB.__select_method(f"SELECT user_id FROM wallet_model WHERE address='{address}' AND network='{network.upper()}';"))][0]