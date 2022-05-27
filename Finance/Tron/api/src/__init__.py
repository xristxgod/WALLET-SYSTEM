import json
from typing import Dict, Optional, Union

import asyncpg

from config import Config, TRON_NETWORK_INDEX

class DB:
    DATABASE_URL = Config.DATABASE_URL
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
    """
    @staticmethod
    async def __select_method(sql) -> asyncpg.Record:
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
    async def get_token_info(token: str) -> Union[Dict, None]:
        try:
            data = (await DB.__select_method((
                f"SELECT address, decimals, token_info FROM token_model "
                f"WHERE token = '{token.upper()}' AND network = {TRON_NETWORK_INDEX};"
            )))[0]
            return {
                "token": token,
                "address": data["address"],
                "decimals": data["decimals"],
                "token_info": json.loads(data["token_info"]),
            }
        except Exception:
            return None