from typing import Optional, Dict

import requests

from config import logger

class Client:

    @staticmethod
    def request(method: str, url: str) -> Optional[Dict]:
        try:
            response = requests.request(method, url)
            return response.json()
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return None