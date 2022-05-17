import json
from typing import Dict
from datetime import datetime

import asyncio
import aiohttp
import aiofiles

from src.sender import Sender
from src.utils import Utils
from config import ENDPOINTS_URL_PATH

class Checker:

    @staticmethod
    def get_url(url: str):
        return [u.format() for u in [url]]


    @staticmethod
    async def check_endpoint(**params):
        session_params: Dict = Utils.get_headers(auth=params.get("auth"), headers=params.get("headers"))
        request_params = {"json": params.get("data_for_check")} if params.get("data_for_check") is not None else {}
        urls = params.get()


    @staticmethod
    async def check_all():
        async with aiofiles.open(ENDPOINTS_URL_PATH, 'r') as file:
            endpoints_url = json.loads(await file.read())
        await Sender.send_info(text='The bot for checking the system is running!')
        await asyncio.gather(*[Checker.check_endpoint(**url_params) for url_params in endpoints_url
        ])
