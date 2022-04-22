import os
import uuid
import json
from typing import Union
from datetime import datetime

import aiofiles

from config import ERROR, NOT_SEND

class Errors:

    @staticmethod
    async def write_to_error(error: Exception, msg: str):
        async with aiofiles.open(ERROR, 'a', encoding='utf-8') as file:
            # If an error occurred on the RabbitMQ side, write about it.
            await file.write(f"Error: {error} | {msg} \n")

    @staticmethod
    async def write_to_helper_file(values: json):
        async with aiofiles.open(Utils.get_helper_file_name(), 'w') as file:
            # Write all the verified data to a json file, and do not praise the work
            await file.write(values)

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
    def get_helper_file_name() -> str:
        return os.path.join(NOT_SEND, f'{int(datetime.timestamp(datetime.now()))}-{uuid.uuid4()}.json')

    @staticmethod
    def get_datetime(is_timestamp: bool = True) -> Union[int, str]:
        date = datetime.now()
        if is_timestamp:
            return int(datetime.timestamp(date))
        return date.strftime('%Y-%m-%d %H:%M:%S')
