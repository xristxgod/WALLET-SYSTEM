import asyncio
from src.service import run

async def main(loop):
    await asyncio.gather(*[
        run(loop)
    ])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()