import aiohttp

from src.storage import storage, lock
from config import Config, logger

class Sender:
    API_URL = Config.BOT_ALERT_API_URL
    API_METHOD = "/api/checker/<method>"

    @staticmethod
    def __get_url(method: str = "info"):
        return Sender.API_URL + Sender.API_METHOD.replace("<method>", method)

    @staticmethod
    async def _send_to_bot(text: str, method: str = "info"):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                Sender.__get_url(method=method),
                params={
                   "message": text
                }
            ) as response:
                if not response.ok:
                    logger.error(f'MESSAGE NOT WAS SENT: {text}. {await response.text()}')


    @staticmethod
    async def send_info(text: str):
        await Sender._send_to_bot(text=text)

    @staticmethod
    async def send_news(title: str, url: str, message: str, tag: str, is_error: bool):
        pass