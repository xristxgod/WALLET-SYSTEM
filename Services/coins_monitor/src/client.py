from typing import Optional, Dict

import aiohttp

from src.__init__ import RabbitMQ
from src.utils import Errors
from config import logger, decimals, Config

class Client:

    @staticmethod
    async def get_current_prices(coins: str) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                params = f"ids={coins}&vs_currencies=usd&include_last_updated_at=true"
                async with session.get(f"'{Config.API_COINS}/api/v3/simple/price?{params}") as response:
                    if not response.ok:
                        logger.error(f"GET RESPONSE ERROR: {response.status}")
                        return None
                    response_json = await response.json()
                    result = {}
                    for coin_name in response_json.keys():
                        result.update({
                            coin_name: {
                                "value": decimals.create_decimal(response_json[coin_name]["usd"]),
                                "time": response_json[coin_name]["last_updated_at"]
                            }
                        })
            return result
        except Exception as error:
            logger.error(f"ERROR CLIENT STEP 12: {error}")
            await Errors.write_to_error(error=error, msg="ERROR CLIENT STEP 12")
            await RabbitMQ.send_to_checker(
                error=error,
                msg="ERROR 'Client' STEP 12",
                title="COINS",
                func=Client.get_current_prices.__name__
            )