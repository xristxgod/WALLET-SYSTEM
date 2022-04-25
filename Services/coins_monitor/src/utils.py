import json
from typing import Union
from datetime import datetime

import aiofiles

from config import ERROR

class Errors:

    @staticmethod
    async def write_to_error(error: Exception, msg: str):
        async with aiofiles.open(ERROR, 'a', encoding='utf-8') as file:
            # If an error occurred on the RabbitMQ side, write about it.
            await file.write(f"Error: {error} | {msg} \n")

    @staticmethod
    async def write_to_send(error: Exception, msg: str, title: str, func: str) -> json:
        return json.dumps({
            "status": "ERROR",
            "time": Utils.get_datetime(),
            "title": title,
            "func": func,
            "error": f"{error}",
            "message": msg,
        })

class Utils:

    @staticmethod
    def get_datetime(is_timestamp: bool = True) -> Union[int, str]:
        date = datetime.now()
        if is_timestamp:
            return int(datetime.timestamp(date))
        return date.strftime('%Y-%m-%d %H:%M:%S')