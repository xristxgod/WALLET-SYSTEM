from typing import Dict

from src.services.crypto import CryptForUser

class Parser:


    @staticmethod
    async def processing_message(data: Dict):
        user = CryptForUser(
            network=data["network"],
            token=data["token"],
            inputs=["inputs"]
        )