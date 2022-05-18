from api.services.external.client import Client
from api.utils.types import TG_CHAT_ID, TG_USERNAME, FULL_NETWORK
from config import Config

class Sender:
    """
    This class is used to send telegram messages to bots.
    """
    API_URL = Config.BOT_ALERT_API_URL
    METHODS = {
        "CREATE": "/api/create/transaction",
        "INFO_CHECKER": "/api/checker/info",
        "REG": "/api/user/reg"
    }

    @staticmethod
    def get_url(method: str = 'CREATE'):
        return Sender.API_URL + Sender.METHODS.get(method.upper())

    @staticmethod
    def send_message_to_bot(chat_id: TG_CHAT_ID, network: FULL_NETWORK, status: int = 0, method: str = 'CREATE', **data) -> bool:
        return True if Client.post_request(
            url=Sender.get_url(method=method),
            chatID=chat_id,
            fromAddress=data.get("fromAddress"),
            toAddress=data.get("toAddress"),
            amount=data.get("amount"),
            fee=data.get("fee"),
            network=network,
            status=status,
        ).get("message") else False

    @staticmethod
    def send_message_to_checker(text: str, method: str = 'INFO_CHECKER'):
        return True if Client.post_request(
            url=Sender.get_url(method=method),
            message=text
        ).get("message") else False

    @staticmethod
    def send_message_to_alert_bot(chat_id: TG_CHAT_ID, username: TG_USERNAME, is_admin: bool = False, method: str = "REG") -> bool:
        return True if Client.post_request(
            url=Sender.get_url(method=method),
            chatID=chat_id,
            username=username,
            isAdmin=is_admin
        ).get("message") else False
