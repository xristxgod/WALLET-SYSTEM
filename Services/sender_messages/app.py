import asyncio
import typing

from src.services.runer import run

async def main(loop: typing.Any):
    await asyncio.gather(*[
        run(loop=loop)
    ])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()