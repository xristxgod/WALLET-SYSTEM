from src.__init__ import MessageRepository
from src.schemas import BodyRegUser, BodyBalance, BodyInfo
from src.schemas import BodyNews
from src.schemas import BodyTransaction
from src.sender import Sender
from src.utils import Utils
from src.types import Symbol, CoinsURL, TGToken
from config import Config

message_repository = MessageRepository()

class WorkerUser:
    """This class forms the text for the message"""
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
        network, token = body.network.split('-')
        if is_add:
            text = f"{Symbol.ADD} There was a replenishment: {body.amount} {body.network}\n"
        else:
            text = f"{Symbol.DEC} Funds were debited: {body.amount} {body.network}\n"
        url = CoinsURL.get_blockchain_url_by_network(network) + f'/#/transaction/{body.transactionHash}'
        text += (
            f"ChatID: {body.chat_id}\n"
            f"Username: {body.username}",
            f"<b><a href='{url}'>Check transaction:</a></b>\n"
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

    @staticmethod
    async def info_text(body: BodyNews) -> bool:
        return await Sender.send_to_bot_by_admin(
            text=f"{Symbol.ADD} {body.message}",
            token=WorkerChecker.BOT_CHECKER
        )

class WorkerTransaction:
    """This class generates transaction messages."""
    BOT_MAIN: TGToken = Config.BOT_MAIN_TOKEN

    @staticmethod
    async def create_text(body: BodyTransaction) -> bool:
        """Transaction creation message"""
        network, token = body.network.split('-')
        url = CoinsURL.get_blockchain_url_by_network(network) + f"/#/transaction/{body.transactionHash}"
        text = (
            f"{Symbol.DEC} The transaction on <b>{network}</b> network has been created!\n"
            f"The sender/s: <b>{body.fromAddress}</b>\n"
            f"The Recipient/s: <b>{body.toAddress}</b>\n"
            f"For the amount of: <b>{body.amount} {body.network}</b>\n"
            f"Commission: <b>{body.fee} {CoinsURL.get_native_by_network(network)}</b>\n"
            f"                                          <b><a href='{url}'>Check transaction:</a></b>\n"
        )
        message = await Sender.send_to_bot_by_chat_id_response(
            chat_id=body.chatId,
            token=WorkerTransaction.BOT_MAIN,
            text=text
        )
        message_repository.set_message(
            chat_id=body.chatId,
            transaction_hash=body.transactionHash,
            network=body.network,
            status=body.status,
            message_id=Utils.get_message_id(message=message)
        )
        return True

    @staticmethod
    async def update_text(body: BodyTransaction) -> bool:
        pass

    @staticmethod
    async def send_text(body: BodyTransaction) -> bool:
        """Transaction sending message"""
        network, token = body.network.split('-')
        url = CoinsURL.get_blockchain_url_by_network(network) + f"/#/transaction/{body.transactionHash}"
        text = (
            f"{Symbol.ADD} The transaction on <b>{network}</b> network has been sent!\n"
            f"The sender/s: <b>{body.fromAddress}</b>\n"
            f"The Recipient/s: <b>{body.toAddress}</b>\n"
            f"For the amount of: <b>{body.amount} {body.network}</b>\n"
            f"Commission: <b>{body.fee} {CoinsURL.get_native_by_network(network)}</b>\n"
            f"                                          <b><a href='{url}'>Check transaction:</a></b>\n"
        )

        message_id = message_repository.get_message(
            chat_id=body.chatId,
            transaction_hash=body.transactionHash,
            network=body.network
        ).get("message_id")
        if message_id is None:
            return await Sender.send_to_bot_by_chat_id(
                chat_id=body.chatId,
                token=WorkerTransaction.BOT_MAIN,
                text=text
            )
        else:
            message_repository.del_message(
                chat_id=body.chatId,
                transaction_hash=body.transactionHash,
                network=body.network
            )
            return await Sender.update_message_by_message_id(
                text=text,
                token=token,
                chat_id=body.chatId,
                message_id=message_id
            )
