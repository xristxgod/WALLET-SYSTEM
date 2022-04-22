import json

import aiohttp


from src.services.storage import storage, lock
from src.__init__ import DB
from src.utils import Errors
from config import Config, logger

class Bot:

    @staticmethod
    async def send_to_bot(text: str):
        """
        Send a message to the telegram bot
        :param text: Message text
        :return: The status of the completed work
        """
        try:
            async with aiohttp.ClientSession() as session:
                for user_id in await DB.get_admin_ids():
                    # Send a request to the bot.
                    async with session.get(
                            f"https://api.telegram.org/bot{Config.BOT_TOKEN_CHECKER}/sendMessage",
                            params={
                                # You can get it from @username_to_id_bot.
                                "chat_id": user_id,
                                "text": text,
                                # So that you can customize the text.
                                "parse_mode": "html"
                            }
                    ) as response:
                        if not response.ok:
                            logger.error(f'MESSAGE WAS NOT SENT: {text}. {await response.text()}')
                            raise Exception
                        else:
                            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR SEND TO BOT: {error}")
            await Errors.write_to_error(error=error, msg="ERROR FUNC SEND TO BOT STEP 14")
            await Errors.write_to_helper_file(values=json.dumps({"message": text}))
            return False

    @staticmethod
    async def send_report(title: str, url: str, message: str, tag: str, is_error: bool):
        async with lock:
            if is_error:
                await storage.add_error(title)
            else:
                await storage.remove_error(title)
            statuses = await storage.get_text()
            symbol = '🟢' if len(statuses) == 0 else '🔴'
            text = (
                f'{symbol} (#{tag}) {title}\n'
                f'{message}\n'
                f'URL: {url}\n'
                f'\n'
                f'{statuses}'
            )
        await Bot.send_to_bot(text)