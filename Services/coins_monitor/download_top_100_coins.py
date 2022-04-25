import asyncio
import json

import aiohttp

from config import Config, COINS_LIST, COINS_LIST_TOP_100, logger

class Top100Coins:
    @staticmethod
    async def download_top_100():
        async with aiohttp.ClientSession() as session:
            params = f'vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
            async with session.get(
                f'{Config.API_COINS}/api/v3/coins/markets?{params}'
            ) as response:
                if not response.ok:
                    logger.error(f'GET RESPONSE ERROR: {response.status}')
                    return None
                result = await response.json()
        used_coins = []
        for_file = []
        with open(COINS_LIST, "r", encoding="utf-8") as file:
            COINS = json.loads(file.read())
        for main_coin in COINS:
            for_file.append({
                "name": main_coin['name'],
                "symbol": main_coin['symbol'],
                "defaultPrice": main_coin['defaultPrice']
            })
            used_coins.append(main_coin['name'])
        for coin in result:
            if coin['id'] in used_coins:
                continue
            for_file.append({
                "name": coin['id'],
                "symbol": coin['symbol'],
                "defaultPrice": None
            })
            used_coins.append(coin['id'])
        with open(COINS_LIST_TOP_100, "w", encoding="utf-8") as file:
            file.write(json.dumps(for_file))

if __name__ == '__main__':
    asyncio.run(Top100Coins.download_top_100())