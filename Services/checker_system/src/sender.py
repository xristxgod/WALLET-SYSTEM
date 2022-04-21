import json

import aiohttp

from src.utils import Errors
from src.__init__ import DB
from config import Config, logger

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