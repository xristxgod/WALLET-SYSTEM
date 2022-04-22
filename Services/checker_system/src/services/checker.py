import asyncio

from src.services.sender import send_to_bot
from src.services.__init__ import Endpoint
from src.utils import CheckerUtils
from config import logger

async def check_endpoint(is_send: bool = True, **params):
    pass

async def check_all(is_all: bool = True, is_send: bool = True, sub: str = None, mod: str = None,):
    if is_all:
        endpoints = await Endpoint.get_all_endpoints()
    else:
        endpoints = await Endpoint.get_endpoints(sub_name=sub, mod_name=mod)

    logger.error("::::CHECKER BOT HAS STARTED WORKING::::")
    if is_send:
        await send_to_bot(CheckerUtils.get_hello_text())
    await asyncio.gather(*[
        check_endpoint(is_send=is_send, **endpoint_params)
        for endpoint_params in endpoints
    ])

async def run():
    await check_all()

if __name__ == '__main__':
    asyncio.run(run())