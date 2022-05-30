import aiohttp

from src.__init__ import SenderMethod
from src.utils.schemas import BodyApiBalance, BodyApiTransaction
from config import logger

class Sender(SenderMethod):

    @staticmethod
    async def send_to_users_method(data: BodyApiBalance) -> bool:
        """Send to bot alert by API | ADD/DEC balance"""
        try:
            async with aiohttp.ClientSession(headers=Sender._get_headers()) as session:
                async with session.post(
                        Sender._get_url(Sender.USERS_METHOD, method=data.method),
                        data={
                            "chatID": data.chatID,
                            "username": data.username,
                            "network": data.network,
                            "amount": data.amount,
                            "transactionHash": data.transactionHash,
                        }
                ) as response:
                    logger.error(f"SEND TO API: {response.ok}")
            return bool((await response.json()).get("message"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def send_to_transaction_method(data: BodyApiTransaction) -> bool:
        """Send to bot alert by API | ADD/DEC balance"""
        try:
            async with aiohttp.ClientSession(headers=Sender._get_headers()) as session:
                async with session.post(
                        Sender._get_url(Sender.TRANSACTION_METHOD, method=data.method),
                        data={
                            "chatID": data.chatID,
                            "network": data.network,
                            "transactionHash": data.transactionHash,
                            "inputs": data.inputs,
                            "outputs": data.outputs,
                            "amount": data.amount,
                            "fee": data.fee,
                            "status": data.status
                        }
                ) as response:
                    logger.error(f"SEND TO API: {response.ok}")
            return bool((await response.json()).get("message"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False