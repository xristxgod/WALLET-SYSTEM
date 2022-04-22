import emoji
from config import Config

class TelegramSmailsAndSymbols:
    GREEN_CIRCLE = emoji.emojize(":green_circle:")
    YELLOW_CIRCLE = emoji.emojize(":yellow_circle:")
    RED_CIRCLE = emoji.emojize(":red_circle:")

    @staticmethod
    def get_network_emoji(network: str, coin: str) -> str:
        pass

    @staticmethod
    def get_blockchain_url(network: str, tx_hash: str) -> str:
        pass

emojis = TelegramSmailsAndSymbols