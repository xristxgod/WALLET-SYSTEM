from typing import Optional, Dict

import aiohttp

from config import logger

class Client:
    @staticmethod
    async def post_request(url: str, **data) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response = await response.json()
            return response
        except Exception as error:
            logger.error(f"ERROR: {error}")

    @staticmethod
    async def get_request(url: str) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json()
            return response
        except Exception as error:
            logger.error(f"ERROR: {error}")

    @staticmethod
    async def put_request(url: str, **data) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, json=data) as response:
                    response = await response.json()
            return response
        except Exception as error:
            logger.error(f"ERROR: {error}")