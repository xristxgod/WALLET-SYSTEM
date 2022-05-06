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
    TRON = {"url": Config.TRON_BLOCKCHAIN, "native": "TRX"}

    @staticmethod
    def get_blockchain_url_by_network(network: str) -> str:
        return CoinsURL.__dict__.get(network)["url"]

    @staticmethod
    def get_native_by_network(network: str) -> str:
        return CoinsURL.__dict__.get(network.upper())["native"]