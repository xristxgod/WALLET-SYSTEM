from typing import Optional, Dict, List

from src.external.client import Client
from src.types import FULL_NETWORK, CRYPTO_ADDRESS, NETWORK, TG_CHAT_ID
from config import Config

class SenderToCryptoNode:
    API_URLs: Dict = {"TRON": Config.TRON_NODE_API_URL}
    CREATE_TRANSACTION_URL = "/api/<network>/create/transaction"
    SEND_TRANSACTION_URL = "/api/<network>/send/transaction"
    GET_OPTIMAL_FEE_URL = "/api/<network>/fee/<fromAddress>&<toAddress>"
    GET_BALANCE = "/api/<network>/fee/<address>"

    @staticmethod
    def __get_correct_path(url: str, **kwargs):
        url = url
        for key, value in kwargs:
            url.replace(f"<{key}>", value)
        return url

    @staticmethod
    def _get_correct_url(api_url: str, url: str, **kwargs):
        return api_url + SenderToCryptoNode.__get_correct_path(url=url, **kwargs)

    # <<<=============================================>>> SENDER <<<=================================================>>>

    @staticmethod
    async def get_optimal_fee(network: NETWORK, **kwargs) -> Optional[Dict]:
        """Get optimal fee"""
        from_, to_ = "", ""
        for _input in kwargs.get("inputs"):
            from_ = _input + "+"
        for _output in kwargs.get("outputs"):
            to_ = _output['address'] + "+"

        if to_[-1] == "+":
            to_ = to_[:-1]
        if from_[-1] == "+":
            from_ = from_[:-1]

        return await Client.get_request(
            url=SenderToCryptoNode._get_correct_url(
                api_url=SenderToCryptoNode.API_URLs.get(network),
                url=SenderToCryptoNode.GET_OPTIMAL_FEE_URL,
                network=kwargs.get("token"),
                fromAddress=from_,
                toAddress=to_
            )
        )

    @staticmethod
    async def create_transaction(network: NETWORK, **kwargs) -> Optional[Dict]:
        """Create transaction"""
        return await Client.post_request(
            url=SenderToCryptoNode._get_correct_url(
                api_url=SenderToCryptoNode.API_URLs.get(network),
                url=SenderToCryptoNode.CREATE_TRANSACTION_URL,
                network=kwargs.get("token").lower()
            ),
            fromAddress=kwargs.get("inputs"),
            outputs=kwargs.get("outputs")
        )

    @staticmethod
    async def send_transaction(network: NETWORK, **kwargs) -> Optional:
        """Send transaction"""
        await Client.post_request(
            url=SenderToCryptoNode._get_correct_url(
                api_url=SenderToCryptoNode.API_URLs.get(network),
                url=SenderToCryptoNode.SEND_TRANSACTION_URL,
                network=kwargs.get("token").lower()
            ),
            createTxHex=kwargs.get("createTxHex"),
            privateKeys=kwargs.get("privateKeys")
        )

    @staticmethod
    async def get_balance(network: NETWORK, address: CRYPTO_ADDRESS, token: str) -> Dict:
        return await Client.get_request(
            url=SenderToCryptoNode._get_correct_url(
                api_url=SenderToCryptoNode.API_URLs.get(network),
                url=SenderToCryptoNode.GET_BALANCE,
                network=token.lower(),
                address=address
            ),
        )

class SenderToBotAlert:
    API_URL: str = Config.BOT_ALERT_API_URL
    UPDATE_TRANSACTION = "/api/create/transaction"

    @staticmethod
    def _get_inputs(inputs: List[CRYPTO_ADDRESS]) -> str:
        from_address = ""
        for _input in inputs:
            from_address += f"{_input} | "
        return from_address[:-3]

    @staticmethod
    def _get_outputs(outputs: List[Dict]):
        to_address = ""
        for _output in outputs:
            to_address += f"{_output.get('address')} | "
        return to_address[:-3]

    # <<<=============================================>>> SENDER <<<=================================================>>>

    @staticmethod
    async def update_transaction(chat_id: TG_CHAT_ID, network: FULL_NETWORK, status: int = 1, **tx_data) -> bool:
        return bool((await Client.put_request(
            url=SenderToBotAlert.API_URL + SenderToBotAlert.UPDATE_TRANSACTION,
            chatID=chat_id,
            transactionHash=tx_data.get("transaction_hash"),
            fromAddress=SenderToBotAlert._get_inputs(tx_data.get("inputs")),
            toAddress=SenderToBotAlert._get_outputs(tx_data.get("outputs")),
            amount=tx_data.get("amount"),
            fee=tx_data.get("fee"),
            network=network,
            status=status
        )).get("message"))