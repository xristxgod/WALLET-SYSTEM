import asyncio
from typing import List, Dict
from datetime import datetime

from src.__init__ import DB, RabbitMQ
from src.utils import Errors
from src.client import Client
from config import logger

class ParserCoins:

    @staticmethod
    async def get_currency_of_coins(coins: List[Dict]) -> None:
        await asyncio.sleep(5)
        for coin in coins:
            await DB.create_coin_tabel(coin["symbol"])

        currents = {}
        last_times = {}

        while True:
            all_results = await Client.get_current_prices(','.join([coin["name"] for coin in coins]))

            for coin in coins:
                try:
                    if coin['defaultPrice'] is not None:
                        is_without_gecko = True
                    else:
                        is_without_gecko = False
                    coin_name = coin["name"]
                    if is_without_gecko:
                        currents.update({
                            coin_name: {'time': int(round(datetime.now().timestamp())), 'value': coin['defaultPrice']}
                        })
                        last_times.update({coin_name: currents[coin_name]['time']})
                        is_update = True
                    else:
                        currents.update({coin_name: all_results[coin_name]})
                        is_update = currents[coin_name] is not None and (
                                (coin_name not in last_times.keys()) or (
                                    last_times[coin_name] != currents[coin_name]['time'])
                        )
                    if is_update:
                        last_times.update({coin_name: currents[coin_name]['time']})
                        await DB.insert_coin_currency(coin['symbol'], currents[coin_name]['time'],
                                                      currents[coin_name]['value'])
                except Exception as error:
                    logger.error(f'ERROR PARSING {coin["name"]}: {error}')
                    await Errors.write_to_error(error=error, msg="ERROR 'ParserCoins' STEP 26")
                    await RabbitMQ.send_to_checker(
                        error=error,
                        msg="ERROR 'ParserCoins' STEP 26",
                        title="COINS",
                        func=ParserCoins.get_currency_of_coins.__name__
                    ),
            await asyncio.sleep(5)