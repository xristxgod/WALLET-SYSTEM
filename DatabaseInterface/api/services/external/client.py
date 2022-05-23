from typing import Optional, Union, Dict, List

import requests

from config import logger

class Client:
    @staticmethod
    def get_request(url: str, headers: Optional[Dict] = None) -> Optional[Union[Dict, List]]:
        try:
            data = requests.request('GET', url, headers=headers)
            return data.json()
        except Exception as error:
            logger.error(f"ERROR: {error}")

    @staticmethod
    def post_request(url: str, headers: Optional[Dict] = None, **data) -> Optional[Union[Dict, List]]:
        try:
            data = requests.request("POST", url, headers=headers, json=data)
            return data.json()
        except Exception as error:
            logger.error(f"ERROR: {error}")