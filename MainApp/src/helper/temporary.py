import datetime
from typing import Optional, Dict, Tuple

from src.utils.types import TELEGRAM_USER_ID
from src.utils.utils import Utils


class TemporaryCodeRepository:
    """Temporary Code Repository"""
    TEMPORARY_TIME = 10                 # Minutes

    def __init__(self):
        """
        {
            "chatID": {
                "time": REGISTER_CODE_TIME,
                "code": CODE
            }
        }
        """
        self.temporary_codes: Dict = {}

    def set_temporary_code(self, chat_id: TELEGRAM_USER_ID, code: str) -> Tuple[bool, str]:
        self.temporary_codes[chat_id] = {
            "time": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "code": code
        }
        return True, code

    def delete_temporary_code(self, chat_id: TELEGRAM_USER_ID) -> bool:
        if chat_id in self.temporary_codes.keys():
            self.temporary_codes.pop(chat_id)
        return True

    def get_temporary_code(self, chat_id: TELEGRAM_USER_ID) -> Optional[str]:
        code_data: Dict = self.temporary_codes.get(chat_id)
        if code_data is not None and Utils.is_have_time(code_data.get("time"), minutes=self.TEMPORARY_TIME):
            return code_data.get("code")
        elif code_data is not None and not Utils.is_have_time(code_data.get("time"), minutes=self.TEMPORARY_TIME):
            self.temporary_codes.pop(chat_id)
        return None


temporary_code = TemporaryCodeRepository()
