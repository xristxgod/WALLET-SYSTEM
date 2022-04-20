import json
from typing import Dict, List, Optional, Union

import asyncpg

from config import Config

TOKENS = [
    {
        "token": "USDT",
        "address": "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA",
        "decimals": 6,
        "token_info": '{"bandwidth": 345, "feeLimit": 1000, "isBalanceNotNullEnergy": 14631, "isBalanceNullEnergy": 29631}',
    }
]

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

    @staticmethod
    async def get_token_info(token: str, network: str = "TRON") -> Union[Dict, None]:
        try:
            if Config.NODE_NETWORK == "TEST":
                data = [t for t in TOKENS if t["token"] == token.upper()][0]
            else:
                data = await DB.__select_method((
                    f"SELECT address, decimals, token_info FROM token_model "
                    f"WHERE token = '{token.upper()}' AND network = '{network.upper()}';"
                ))
            return {
                "token": token,
                "address": data["address"],
                "decimals": data["decimals"],
                "token_info": json.loads(data["token_info"]),
            }
        except Exception:
            return None