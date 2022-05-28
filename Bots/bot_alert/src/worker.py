from src.__init__ import message_repository
from src.parser.messager import MessageTransaction, MessageChecker, MessageUser
from src.schemas import BodyRegUser, BodyBalance, BodyInfo
from src.schemas import BodyNews
from src.schemas import BodyTransaction
from src.sender import Sender
from src.utils.types import TGToken
from src.utils.utils import Utils
from config import Config

class WorkerUser:
    """This class forms the text for the message"""
    BOT_ALERT: TGToken = Config.BOT_ALERT_TOKEN
    BOT_MAIN: TGToken = Config.BOT_MAIN_TOKEN

    @staticmethod
    async def reg_user_text(body: BodyRegUser) -> bool:
        """Message at registration"""
        return await Sender.send_to_bot_by_admin(
            text=MessageUser(chat_id=body.chatID, username=body.username).generate_text(
                status="REG_ADMIN" if body.isAdmin else "REG_USER"
            ),
            token=WorkerUser.BOT_ALERT
        )

    @staticmethod
    async def balance_text(body: BodyBalance, is_add: bool = False) -> bool:
        """Message at the deposit/debit"""
        text = MessageUser(
            chat_id=body.chatID, username=body.username, amount=body.amount, network=body.network,
            transaction_hash=body.transactionHash
        ).generate_text(status="ADD" if is_add else "DEC")
        return (await Sender.send_to_bot_by_admin(
            text=text,
            token=WorkerUser.BOT_ALERT
        )) and (await Sender.send_to_bot_by_chat_id(
            text=text,
            chat_id=int(body.chatID),
            token=WorkerUser.BOT_ALERT
        ))

    @staticmethod
    async def info_text(body: BodyInfo) -> bool:
        """Message at the information"""
        text = MessageUser(text=body.message).generate_text(status="INFO")
        token = WorkerUser.BOT_MAIN if body.toMain else WorkerUser.BOT_ALERT
        if body.chatIDs is not None:
            for chat_id in body.chatIDs:
                await Sender.send_to_bot_by_chat_id(
                    text=text,
                    chat_id=int(chat_id),
                    token=token
                )
            return True
        else:
            return await Sender.send_to_bot_by_all(
                text=text,
                token=token
            )

class WorkerChecker:
    """This class generate checker message"""
    BOT_CHECKER: TGToken = Config.BOT_CHECKER_TOKEN

    @staticmethod
    async def news_text(body: BodyNews, is_good: bool = False) -> bool:
        """Sends a message to the bot with the system status"""
        return await Sender.send_to_bot_by_admin(
            text=MessageChecker(text=body.message).generate_text(status="GOOD" if is_good else "BAD"),
            token=WorkerChecker.BOT_CHECKER
        )

    @staticmethod
    async def info_text(body: BodyNews) -> bool:
        """Send info to the bot with the system status"""
        return await Sender.send_to_bot_by_admin(
            text=MessageChecker(text=body.message).generate_text(status="INFO"),
            token=WorkerChecker.BOT_CHECKER
        )

class WorkerTransaction:
    """This class generates transaction messages."""
    BOT_MAIN: TGToken = Config.BOT_MAIN_TOKEN

    @staticmethod
    async def create_text(body: BodyTransaction) -> bool:
        """Create transaction"""
        # Create and send message to main bot
        message = await Sender.send_to_bot_by_chat_id_response(
            chat_id=body.chatID, token=WorkerTransaction.BOT_MAIN, text=MessageTransaction(
                network=body.network, transaction_hash=body.transactionHash, amount=body.amount, fee=body.fee,
                inputs=body.inputs,  outputs=body.outputs
            ).generate_text(status="PROCESSING")
        )
        # Save transaction in repository
        message_repository.set_message(
            chat_id=body.chatID, transaction_hash=body.transactionHash, network=body.network, status=body.status,
            message_id=Utils.get_message_id(message=message)
        )
        return True

    @staticmethod
    async def update_text(body: BodyTransaction) -> bool:
        """Update transaction"""
        # Create and send message to main bot
        message = MessageTransaction(
            network=body.network, transaction_hash=body.transactionHash, amount=body.amount, fee=body.fee,
            inputs=body.inputs, outputs=body.outputs
        ).generate_text(status="CREATE" if body.status == 1 else "ERROR")
        # Get message in transaction repository
        message_id = message_repository.get_message(
            chat_id=body.chatID, transaction_hash=body.transactionHash, network=body.network
        ).get("message_id")
        # If message not in repository, that send to new transaction message to main bot
        if message_id is None:
            return await Sender.send_to_bot_by_chat_id(
                chat_id=body.chatID,
                token=WorkerTransaction.BOT_MAIN,
                text=message
            )
        # Else message has in repository, that update transaction message in main bot
        return await Sender.update_message_by_message_id(
            text=message, token=body.network.split("-")[1], chat_id=body.chatID, message_id=message_id
        )

    @staticmethod
    async def send_text(body: BodyTransaction) -> bool:
        """Sent transaction"""
        # Create and send message to main bot
        message = MessageTransaction(
            network=body.network, transaction_hash=body.transactionHash, amount=body.amount, fee=body.fee,
            inputs=body.inputs, outputs=body.outputs
        ).generate_text(status="SENT")
        # Get message in transaction repository
        message_id = message_repository.get_message(
            chat_id=body.chatID, transaction_hash=body.transactionHash, network=body.network
        ).get("message_id")
        # If message not in repository, that send to new transaction message to main bot
        if message_id is None:
            return await Sender.send_to_bot_by_chat_id(
                chat_id=body.chatID, token=WorkerTransaction.BOT_MAIN, text=message
            )
        # If message has in repository, that delete message in repository!
        message_repository.del_message(
            chat_id=body.chatID,
            transaction_hash=body.transactionHash,
            network=body.network
        )
        # Send message to main bot
        return await Sender.update_message_by_message_id(
            text=message, token=body.network.split("-")[1], chat_id=body.chatID, message_id=message_id
        )