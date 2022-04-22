import os
import json
import uuid
from datetime import datetime
from typing import Dict

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
    def get_request_params(data_for_check: str = None) -> Dict:
        return {'json': data_for_check} if data_for_check is not None else {}

    @staticmethod
    def get_headers(auth: str = None, headers: str = None) -> Dict:
        session_params = {'headers': {'Authorization': auth}} if auth is not None else {}
        if headers is not None:
            if 'headers' in session_params:
                session_params['headers'].update(headers)
            else:
                session_params = {'headers': headers}
        return session_params

    @staticmethod
    async def str_to_coded_type(s: str):
        t, value = s.split('_')
        if t == 'str':
            return value
        elif t == 'int':
            return int(value)
        elif t == 'bool':
            return value.lower() == 'true'
        return value

class Utils:

    @staticmethod
    def get_helper_file_name() -> str:
        return os.path.join(NOT_SEND, f'{int(datetime.timestamp(datetime.now()))}-{uuid.uuid4()}.json')