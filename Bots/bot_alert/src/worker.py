from src.schemas import BodyRegUser
from src.sender import Sender

class WorkerUser:

    @staticmethod
    async def reg_user_text(body: BodyRegUser) -> bool:

        text = ""

        return await Sender.send_to_bot_by_admin(text=text)
