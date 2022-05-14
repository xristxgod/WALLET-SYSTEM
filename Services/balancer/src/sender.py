from typing import Optional, Dict

from src.external.client import Client
from config import Config

class SenderCrypto:
    API_URLs: Dict = {"TRON": Config.TRON_NODE_API_URL}
    CREATE_TRANSACTION_URL = "/api/<network>/create/transaction"
    SEND_TRANSACTION_URL = "/api/<network>/send/transaction"

    @staticmethod
    def __get_correct_path(url: str, **kwargs):
        url = url
        for key, value in kwargs:
            url.replace(f"<{key}>", value)
        return url

    @staticmethod
    def _get_correct_url(api_url: str, url: str, **kwargs):
        return api_url + SenderCrypto.__get_correct_path(url=url, **kwargs)

    @staticmethod
    async def create_transaction(network: str, **kwargs) -> Optional[Dict]:
        """Create transaction"""
        return await Client.post_request(
            url=SenderCrypto._get_correct_url(
                api_url=SenderCrypto.API_URLs.get(network),
                url=SenderCrypto.CREATE_TRANSACTION_URL,
                network=kwargs.get("token").lower()
            ),
            fromAddress=kwargs.get("inputs"),
            outputs=kwargs.get("outputs")
        )

    @staticmethod
    async def send_transaction(network: str, **kwargs) -> Optional[Dict]:
        """Send transaction"""
        return await Client.post_request(
            url=SenderCrypto._get_correct_url(
                api_url=SenderCrypto.API_URLs.get(network),
                url=SenderCrypto.SEND_TRANSACTION_URL,
                network=kwargs.get("token").lower()
            ),
            createTxHex=kwargs.get("createTxHex"),
            privateKeys=kwargs.get("privateKeys")
        )

class SenderBot:
    pass