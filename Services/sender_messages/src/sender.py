from typing import Optional, Dict

import aiohttp

from config import Config, logger

class Sender:
    """Send a message to the bot alery api"""
    API_URL = Config.BOT_ALERT_API_URL
    API_BALANCE = "/bot/api/user/<method>"


    @staticmethod
    def _get_headers() -> Optional[Dict]:
        """There should be an AUTH API and other things that are needed for the head."""
        pass

    @staticmethod
    def send_to_balance_method(method: str = "add", **kwargs):
        """Send to bot alert by API | ADD/DEC balance"""
        try:
            async with aiohttp.ClientSession(headers=Sender._get_headers()) as session:
                async with session.get(
                    Sender.API_URL + ""
                )