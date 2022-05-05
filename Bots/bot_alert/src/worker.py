from src.schemas import BodyRegUser
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
