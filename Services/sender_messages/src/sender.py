from config import Config, logger

class Sender:
    """Send a message to the bot alery api"""
    API_URL = Config.BOT_ALERT_API_URL

    @staticmethod
    def send_if_add():
        pass