import aiohttp

from config import Config, logger
class SenderBot:

    @staticmethod
    async def send_to_bot(text: str, chat_id: int) -> bool:
        """
        Send a message to the telegram bot
        :param text: Message text
        :return: The status of the completed work
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Send a request to the bot.
                async with session.get(
                        f"https://api.telegram.org/bot{Config.BOT_TOKEN_ALERT}/sendMessage",
                        params={
                            # You can get it from @username_to_id_bot.
                            "chat_id": chat_id,
                            "text": text,
                            # So that you can customize the text.
                            "parse_mode": "html"
                        }
                ) as response:
                    if not response.ok:
                        logger.error(f'MESSAGE WAS NOT SENT: {text}. {await response.text()}')
                    else:
                        logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR SEND TO BOT: {error}")
            return False