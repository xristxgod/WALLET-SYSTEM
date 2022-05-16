from typing import Dict

from src.services.crypto import CryptForUser

class Parser:

    @staticmethod
    async def start_sending(user: CryptForUser):
        pass

    @staticmethod
    async def processing_message(data: Dict):
        user = CryptForUser(
            network=data["network"],
            token=data["token"],
            inputs=["inputs"]
        )
        user.CHAT_ID = data.get("chatID")
        user.BASE_FEE = data.get("fee")

