from src.__init__ import MessageRepository
from src.schemas import BodyRegUser, BodyBalance, BodyInfo
from src.schemas import BodyNews
from src.schemas import BodyTransaction
from src.sender import Sender
from src.types import Symbol, TGToken
from config import Config

message_repository = MessageRepository()

class WorkerUser:
    """This module forms the text for the message"""
    BOT_ALERT: TGToken = Config.BOT_ALERT_TOKEN

    @staticmethod
    async def reg_user_text(body: BodyRegUser) -> bool:
        """Message at registration"""
        if body.isAdmin:
            text = f"{Symbol.ADMIN} New admin!\n"
        else:
            text = f"{Symbol.REG} New user!\n"
        text += (
            f"ChatID: {body.chat_id}\n"
            f"Username: {body.username}"
        )
        return await Sender.send_to_bot_by_admin(
            text=text,
            token=WorkerUser.BOT_ALERT
        )

    @staticmethod
    async def balance_text(body: BodyBalance, is_add: bool = False) -> bool:
        """Message at the deposit/debit"""
        if is_add:
            text = f"{Symbol.ADD} There was a replenishment: {body.amount} {body.network}\n"
        else:
            text = f"{Symbol.DEC} Funds were debited: {body.amount} {body.network}\n"
        text += (
            f"ChatID: {body.chat_id}\n"
            f"Username: {body.username}"
        )
        return (await Sender.send_to_bot_by_admin(
            text=text,
            token=WorkerUser.BOT_ALERT
        )) and (await Sender.send_to_bot_by_chat_id(
            text=text,
            chat_id=int(body.chat_id),
            token=WorkerUser.BOT_ALERT
        ))

    @staticmethod
    async def info_text(body: BodyInfo) -> bool:
        """Message at the information"""
        text = (
            f"{Symbol.INFO} Urgent information!\n"
            f"{body.message}"
        )
        if body.chatIds is not None:
            for chat_id in body.chatIds:
                await Sender.send_to_bot_by_chat_id(
                    text=text,
                    chat_id=int(chat_id),
                    token=WorkerUser.BOT_ALERT
                )
            return True
        else:
            return await Sender.send_to_bot_by_all(
                text=text,
                token=WorkerUser.BOT_ALERT
            )

class WorkerChecker:
    BOT_CHECKER: TGToken = Config.BOT_CHECKER_TOKEN

    @staticmethod
    async def news_text(body: BodyNews, is_good: bool = False) -> bool:
        """Sends a message to the bot with the system status"""
        if is_good:
            text = f"{Symbol.ADD} Good news:\n"
        else:
            text = f"{Symbol.DEC} Bad news:\n"

        text += body.message
        return await Sender.send_to_bot_by_admin(
            text=text,
            token=WorkerChecker.BOT_CHECKER
        )

class WorkerTransaction:

    @staticmethod
    async def create_text(body: BodyTransaction) -> bool:
        text = (
            ""
        )


        message_repository.set_message(
            chat_id=body.chatId,
            transaction_hash=body.transactionHash,
            network=body.network,
            status=False,
            message_id=""
        )
