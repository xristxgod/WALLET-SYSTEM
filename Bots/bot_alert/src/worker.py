from src.schemas import BodyRegUser, BodyBalance, BodyInfo
from src.sender import Sender
from src.types import Symbol

class WorkerUser:
    """This module forms the text for the message"""
    @staticmethod
    async def reg_user_text(body: BodyRegUser) -> bool:
        """Message at registration"""
        if body.is_admin:
            text = f"{Symbol.ADMIN} New admin!\n"
        else:
            text = f"{Symbol.REG} New user!\n"
        text += (
            f"ChatID: {body.chat_id}\n"
            f"Username: {body.username}"
        )
        return await Sender.send_to_bot_by_admin(text=text)

    @staticmethod
    async def balance_text(body: BodyBalance, is_add: bool = False) -> bool:
        if is_add:
            text = f"{Symbol.ADD} There was a replenishment: {body.amount} {body.network}\n"
        else:
            text = f"{Symbol.DEC} Funds were debited: {body.amount} {body.network}\n"
        text += (
            f"ChatID: {body.chat_id}\n"
            f"Username: {body.username}"
        )
        return (await Sender.send_to_bot_by_admin(text=text)) and \
               (await Sender.send_to_bot_by_chat_id(text=text, chat_id=int(body.chat_id)))

    @staticmethod
    async def info_text(body: BodyInfo) -> bool:
        text = (
            f"{Symbol.INFO} Urgent information!\n"
            f"{body.message}"
        )
        if body.chat_id is not None:
            return await Sender.send_to_bot_by_chat_id(text=text, chat_id=int(body.chat_id))
        else:
            return await Sender.send_to_bot_by_all(text=text)