from typing import Dict

class Utils:

    @staticmethod
    def get_message_id(message: Dict) -> int:
        try:
            return int(message.get("result")["message_id"])
        except Exception as error:
            return -1