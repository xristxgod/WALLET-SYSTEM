import emoji
from typing import Union

from config import Config

# Telegram token
TGToken = str
# Text message for telegram
TGMessage = str
# User id for telegram bot
TGChatID = Union[int, str]

class Symbol(object):
    ADD = emoji.emojize(":green_circle:")
    DEC = emoji.emojize(":red_circle:")
    REG = emoji.emojize(":yellow_circle:")
    ADMIN = emoji.emojize(":globe_with_meridians:")
    INFO = emoji.emojize(":rocket:")

class CoinsURL(object):
    TRON = Config.TRON_BLOCKCHAIN

    @staticmethod
    def get_coins_url(coin: str) -> str:
        pass