from typing import Dict, Optional

import aiohttp

from src.__init__ import DB
from src.utils.types import TGToken, TGMessage, TGMessageID, TGChatID
from config import logger

class Sender:
    """Send a message to the telegram bot"""
    @staticmethod
    async def send_to_bot_by_admin(text: TGMessage, token: TGToken) -> bool:
        """
        Send a message to the telegram bot for admin
        :param text: Message text
        :param token: Telegram bot token
        """
        try:
            async with aiohttp.ClientSession() as session:
                for chat_id in (await DB.get_all_admin()):
                    async with session.get(
                            f"https://api.telegram.org/bot{token}/sendMessage",
                            params={
                                "chat_id": chat_id,
                                "text": text,
                                "parse_mode": "html"
                            }
                    ) as response:
                        logger.error(f"SEND ({chat_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def send_to_bot_by_chat_id(text: TGMessage, chat_id: TGChatID, token: TGToken) -> bool:
        """
        Send a message to the telegram bot for user
        :param text: Message text
        :param chat_id: User ID for send
        :param token: Telegram bot token
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        params={
                            "chat_id": chat_id,
                            "text": text,
                            "parse_mode": "html"
                        }
                ) as response:
                    logger.error(f"SEND ({chat_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def send_to_bot_by_all(text: TGMessage, token: TGToken) -> bool:
        """
        Send a message to the telegram bot for all users
        :param text: Message text
        :param token: Telegram bot token
        """
        try:
            async with aiohttp.ClientSession() as session:
                for chat_id in (await DB.get_all_users()):
                    async with session.get(
                            f"https://api.telegram.org/bot{token}/sendMessage",
                            params={
                                "chat_id": chat_id,
                                "text": text,
                                "parse_mode": "html"
                            }
                    ) as response:
                        logger.error(f"SEND ({chat_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def send_to_bot_by_chat_id_response(text: TGMessage, chat_id: TGChatID, token: TGToken) -> Optional[Dict]:
        """
        Send a message to the telegram bot for user
        :param text: Message text
        :param chat_id: User ID for send
        :param token: Telegram bot token
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        params={
                            "chat_id": chat_id,
                            "text": text,
                            "parse_mode": "html"
                        }
                ) as response:
                    logger.error(f"SEND ({chat_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return await response.json()
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False

    @staticmethod
    async def update_message_by_message_id(text: TGMessage, chat_id: TGChatID, token: TGToken, message_id: TGMessageID) -> bool:
        """
        Update a message to the telegram bot for user
        :param text: Message text
        :param chat_id: User ID for send
        :param token: Telegram bot token
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.telegram.org/bot{token}/editMessageText",
                        params={
                            "chat_id": chat_id,
                            "text": text,
                            "message_id": message_id,
                            "parse_mode": "html"
                        }
                ) as response:
                    logger.error(f"UPDATE ({chat_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN UPDATE: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False