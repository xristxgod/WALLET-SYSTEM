import decimal
import typing
import aiohttp

from config import decimals, logger

class Client:
    @staticmethod
    async def get_current_price(coin: str, to_coin: str = "usd") -> typing.Union[decimal.Decimal, None]:
        try:
            async with aiohttp.ClientSession() as session:
                params = f"id={coin}&vs_currencies={to_coin}&include_last_updated_at=true"
                async with session.get(
                    f"https://api.coingecko.com/api/v3/simple/price?{params}"
                ) as resp:
                    if not resp.ok:
                        logger.error(f'GET RESPONSE ERROR: {resp.status}')
                        return None
                    response = await resp.json()
                    coin = response.get(coin)
                return decimals.create_decimal(coin.get(to_coin))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return None

