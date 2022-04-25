import json
import asyncio

from src.parser import ParserCoins
from config import COINS_LIST

async def main():
    with open(COINS_LIST, "r", encoding="utf-8") as file:
        coins = json.loads(file.read())
    await ParserCoins.get_currency_of_coins(coins)

if __name__ == '__main__':
    asyncio.run(main())