import json
from datetime import datetime

import asyncio
import aiohttp
import aiofiles

from src.sender import Sender
from config import ENDPOINTS_URL_PATH

class Checker:

    @staticmethod
    async def check_all():
        async with aiofiles.open(ENDPOINTS_URL_PATH, 'r') as file:
            tests = json.loads(await file.read())
        await Sender.send_info('The bot for checking the system is running!')
        await asyncio.gather(*[check_endpoint(**url_params) for url_params in check_urls
        ])
