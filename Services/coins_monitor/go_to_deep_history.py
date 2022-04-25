import asyncio
import json
import sys
import argparse
from asyncio import run, sleep as async_sleep
from datetime import datetime
from typing import List

from aiohttp import ClientSession

from src.__init__ import DB
from config import COINS_LIST_TOP_100, logger, decimals

def create_parser():
    """:return: Getting script params"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", default=0)
    parser.add_argument("-e", "--end", default=None)
    return parser

async def get_history_in_range(coin: str, start: int, end: str) -> List[dict]:
    while True:
        try:
            logger.error(f'        REQUEST {coin}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            async with ClientSession() as session:
                params = f'vs_currency=usd&from={start}&to={end}'
                async with session.get(
                    f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?{params}'
                ) as resp:
                    if not resp.ok:
                        logger.error(f'GET RESPONSE ERROR: {resp.status}. WAIT 30 seconds.')
                        await async_sleep(30)
                        continue
                    json = await resp.json()
                    result = []
                    for record in json['prices']:
                        result.append({
                            'value': decimals.create_decimal(record[1]),
                            'time': record[0]
                        })
            return result
        except Exception as e:
            logger.error(f'GET PRICE ERROR ({coin}): {e}')
            await async_sleep(30)
            continue

async def save_history_for_coin(coin: dict, start: int, end: int):
    db = DB()

    if coin['defaultPrice'] is not None:
        step = 300       # 5 minutes
        for _start in range(start, end, step):
            try:
                await db.insert_coin_currency(coin['symbol'], _start, coin['defaultPrice'])
            except Exception as e:
                logger.error(f'SAVE DEFAULT ERROR: {coin["name"]}: {e}')
                continue
    else:
        try:
            result = await get_history_in_range(coin=coin['name'], start=start, end=end)
            for record in result:
                try:
                    await db.insert_coin_currency(coin['symbol'], record['time'] // 1000, record['value'])
                except Exception as e:
                    if str(e).find('duplicate key value') != -1:
                        continue
                    else:
                        logger.error(f'SAVE DEFAULT ERROR: {coin["name"]}: {e}')
        except Exception as e:
            logger.error(f'SAVE DEFAULT ERROR: {coin["name"]}: {e}')


async def get_currency_of_coins(coins: List[dict], start: int, end: int) -> None:
    for coin in coins:
        await DB.create_coin_tabel(coin["symbol"])

    patch_size = 86399
    for _end in range(end, start, -patch_size):
        try:
            logger.error(
                f'{datetime.fromtimestamp(_end - patch_size).strftime("%Y-%m-%d %H:%M:%S")} -> {datetime.fromtimestamp(_end).strftime("%Y-%m-%d %H:%M:%S")}'
            )
            coins_for_iteration = 5
            for start_index in range(len(coins) // coins_for_iteration + 1):
                current_coins = coins[start_index * coins_for_iteration: (start_index + 1) * coins_for_iteration]
                str_coins = ', '.join([x['name'] for x in current_coins])
                logger.error(f'    + {str_coins}')
                await asyncio.gather(*[
                    save_history_for_coin(coin, start=_end - patch_size, end=_end)
                    for coin in current_coins
                ])
                await async_sleep(2)
        except Exception as e:
            logger.error(f'ERROR PARSING {_end - patch_size} - {_end} | {e}')


async def async_run(start, end):
    with open(COINS_LIST_TOP_100, "r", encoding="utf-8") as file:
        coins_top_100 = json.loads(file.read())
    await get_currency_of_coins(coins_top_100, start, end)


if __name__ == '__main__':
    namespace = create_parser().parse_args(sys.argv[1:])
    run(async_run(
        int(namespace.start) if namespace.start is not None else None,
        int(namespace.end) if namespace.end is not None else None,
    ))
