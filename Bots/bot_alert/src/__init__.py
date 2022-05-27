from typing import List, Optional, Dict

import asyncpg

from src.types import TGChatID
from config import Config

class DB:
    """This class is used to work with the database"""
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

    @staticmethod
    async def get_all_users() -> List[TGChatID]:
        return [user["id"] for user in (await DB.__select_method((
            "SELECT id FROM user_model"
        )))]

    @staticmethod
    async def get_all_admin() -> List[TGChatID]:
        return [user["id"] for user in (await DB.__select_method((
            "SELECT id FROM user_model WHERE is_admin=true"
        )))]

class MessageRepository:

    def __init__(self):
        self.messages_box: Dict = {}

    def get_message(self, chat_id: TGChatID, transaction_hash: str, network: str) -> Optional[Dict]:
        if self.messages_box.get(chat_id) is not None:
            for message in self.messages_box.get(chat_id):
                if message["transaction_hash"] == transaction_hash and message["network"] == network:
                    return message

    def set_message(self, chat_id: TGChatID, **kwargs) -> bool:
        """Set a message"""
        if self.messages_box.get(chat_id) is not None:
            for message in self.messages_box.get(chat_id):
                message: Dict
                if message["message_id"] == kwargs["message_id"] and message["network"] == kwargs["network"] \
                        and message["transaction_hash"] == kwargs["transaction_hash"]:
                    if message["status"] != kwargs["status"] and kwargs["status"]:
                        return self.del_message(
                            chat_id=chat_id,
                            transaction_hash=kwargs["transaction_hash"],
                            network=kwargs["network"]
                        )
                else:
                    self.messages_box.get(chat_id).append({
                        "transaction_hash": kwargs.get("transaction_hash"),
                        "network": kwargs.get("network"),
                        "status": kwargs.get("status"),
                        "message_id": kwargs.get("message_id")
                    })
        else:
            self.messages_box.update({
                chat_id: [{
                    "transaction_hash": kwargs.get("transaction_hash"),
                    "network": kwargs.get("network"),
                    "status": kwargs.get("status"),
                    "message_id": kwargs.get("message_id")
                }]
            })

    def del_message(self, chat_id: TGChatID, transaction_hash: str, network: str) -> bool:
        """Delete a message"""
        if self.messages_box.get(chat_id) is not None:
            for message in self.messages_box.get(chat_id):
                if message["transaction_hash"] == transaction_hash and message["network"] == network:
                    del message
                    return True
            else:
                return False
        else:
            return False

    @property
    def messages(self) -> Dict:
        return self.messages_box

    def remove_all_messages(self) -> bool:
        self.messages_box = []
        return True

message_repository = MessageRepository()