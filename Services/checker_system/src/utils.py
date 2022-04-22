import os
import json
import uuid
from datetime import datetime

import aiofiles

from config import NOT_SEND, ERROR

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

class CheckerUtils:
    @staticmethod
    def get_hello_text() -> str:
        pass

    @staticmethod
    def get_report(text: str) -> str:
        pass

class Utils:

    @staticmethod
    def get_helper_file_name() -> str:
        return os.path.join(NOT_SEND, f'{int(datetime.timestamp(datetime.now()))}-{uuid.uuid4()}.json')