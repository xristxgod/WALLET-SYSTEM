import asyncio
from typing import List, Callable

from src.parsers import ParserDemon

async def run(loop):
    try:
        funcs: List[Callable] = [
            ParserDemon.get_message_from_demons,        # Check message for crypto demon
        ]
        await asyncio.gather(*[
            func(loop)
            for func in funcs
        ])
    except Exception as error:
        pass
