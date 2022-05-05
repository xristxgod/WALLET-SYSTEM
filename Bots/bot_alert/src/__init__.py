from typing import List, Optional, Dict

import asyncpg

from config import Config

class DB:
    DATABASE_URL = Config.DATABASE_URL

    @staticmethod
    async def __select_method(sql) -> Dict:
        connection: Optional[asyncpg.Connection] = None
        try:
            connection = await asyncpg.connect(DB.DATABASE_URL)
            return dict(await connection.fetch(sql))
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

class MessageRepository:

    def __init__(self):
        self.messages_box: List = []