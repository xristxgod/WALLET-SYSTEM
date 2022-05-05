from typing import Optional, Dict, List
import asyncpg

from config import Config

class DB:
    """
    <<<--------------------------------------------------->>>
    tabel = wallet
        id: Integer Primary Key
        network: String(256) NOT NULL
        address: String(256) NOT NULL UNIQUE = TRUE
        private_key: String(256) NOT NULL UNIQUE = TRUE
        public_key: String(256) NOT NULL UNIQUE = TRUE
        passphrase: String(256) NOT NULL UNIQUE = TRUE
        mnemonic_phrase: String(256) NOT NULL UNIQUE = TRUE
        accounts: JSON NOT NULL
        user_id: Integer Foreign Key To user_model
    <<<--------------------------------------------------->>>
    table = wallet_transaction
        id: Integer Primary Key
        network: String(256) NOT NULL
        time: INTEGER NOT NULL
        transaction_hash: String(256) NOT NULL UNIQUE = TRUE
        fee: DECIMAL NOT NULL
        amount: DECIMAL NOT NULL
        senders: JSON NOT NULL
        recipients: JSON NOT NULL
        token: String(256) NOT NULL
        status: BOOL NOT NULL DEFAULT = FALSE
        user_id: Integer Foreign Key To user_model
    <<<--------------------------------------------------->>>
    """

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