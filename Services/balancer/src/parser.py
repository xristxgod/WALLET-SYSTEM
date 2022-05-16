from typing import Optional, Dict, List

from src.utils import Utils
from src.services.crypto import CryptForUser
from config import logger

class Parser:

    @staticmethod
    async def start_sending(user: CryptForUser, outputs: List[Dict]) -> Optional:
        for _, balance in (await user.get_balances()).items():
            if not Utils.is_have_amount(outputs=outputs, balance=balance):
                return "Not have balance"

    @staticmethod
    async def processing_message(data: Dict):
        try:
            user = CryptForUser(
                network=data["network"],
                token=data["token"],
                inputs=["inputs"]
            )
            user.CHAT_ID = data.get("chatID")
            user.BASE_FEE = data.get("fee")
            status = await Parser.start_sending(user=user, outputs=data.get("outputs"))
            if status is not None:
                pass
        except Exception as error:
            logger.error("ERROR: error")
            pass