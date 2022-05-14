import aiohttp

from src.__init__ import SenderMethod
from config import logger

class Sender(SenderMethod):

    @staticmethod
    async def send_to_users_method(method: str = "add", **kwargs) -> bool:
        """Send to bot alert by API | ADD/DEC balance"""
        try:
            async with aiohttp.ClientSession(headers=Sender._get_headers()) as session:
                async with session.get(
                        Sender._get_url(Sender.USERS_METHOD, method=method),
                        params={
                            "chatID": kwargs.get("chat_id"),
                            "username": kwargs.get("username"),
                            "network": kwargs.get("network"),
                            "amount": kwargs.get("amount"),
                            "transactionHash": kwargs.get("transactionHash"),
                        }
                ) as response:
                    logger.error(f"SEND TO API: {response.ok}")
            return bool((await response.json()).get("message"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def send_to_transaction_method(method: str = "send", **kwargs) -> bool:
        """Send to bot alert by API | ADD/DEC balance"""
        try:
            async with aiohttp.ClientSession(headers=Sender._get_headers()) as session:
                async with session.get(
                        Sender._get_url(Sender.TRANSACTION_METHOD, method=method),
                        params={**kwargs}
                ) as response:
                    logger.error(f"SEND TO API: {response.ok}")
            return bool((await response.json()).get("message"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False