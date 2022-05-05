import aiohttp

from config import Config

class Sender:

    BOT_ALERT = Config.BOT_ALERT_TOKEN
    BOT_CHECKER = Config.BOT_CHECKER_TOKEN

    @staticmethod
    async def send_to_bot_by_admin(text: str) -> bool:
        pass

    @staticmethod
    async def send_to_bot_by_chat_id(text: str, chat_id: int) -> bool:
        pass

    @staticmethod
    async def send_to_bot_by_all(text: str) -> bool:
        pass