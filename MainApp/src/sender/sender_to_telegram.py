from typing import Optional

from src.utils.types import TELEGRAM_USER_ID


class SenderToTelegram:

    @staticmethod
    def auth_info(chat_id: TELEGRAM_USER_ID) -> Optional[bool]:
        pass

    @staticmethod
    def auto_code(chat_id: TELEGRAM_USER_ID) -> str:
        pass