from typing import Dict, List, Tuple, Union

from config import Config

TGChatID = Union[int, bytes]

CRYPTONetwork = str
CRYPTOAddress = str
CRYPTOPrivateKey = str
CRYPTOMnemonicWords = str

class CryptoEndpointType(object):
    _CREATE_WALLET = "<domain>/api/<network>/create/wallet"
    _BALANCE = "<domain>/api/<network>/balance/<address>"

    _OPTIMAL_FEE = "<domain>/api/<network>/fee/<inputs>&<outputs>"

    _CREATE_TRANSACTION = "<domain>/api/<network>/create/transaction"
    _SEND_TRANSACTION = "<domain>/api/<network>/create/transaction"

    _NETWORKS = {
        "TRON": Config.DOMAIN_TRON_API
    }

    @staticmethod
    def get_create_wallet_url(network: str) -> str:
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        """
        return CryptoEndpointType._CREATE_WALLET.replace(
            "<domain>", CryptoEndpointType._NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        )

    @staticmethod
    def get_balance_url(network: str, address: CRYPTOAddress) -> str:
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        :type address: ADDRESS = TMq8sLT864CUjy2owCocftJZSDP6qmzeDy
        """
        return CryptoEndpointType._BALANCE.replace(
            "<domain>", CryptoEndpointType._NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        ).replace(
            "<address>", address
        )

    @staticmethod
    def get_optimal_fee_url(network: str, inputs: List[CRYPTOAddress], outputs: List[Dict[CRYPTOAddress, str]]) -> Tuple:
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        :type inputs: [{ADDRESS,AMOUNT}] = [{"address": "TMq8sLT864CUjy2owCocftJZSDP6qmzeDy", "amount": "12.33"}]
        :type outputs: [{ADDRESS,AMOUNT}] = [{"address": "TPH76FSoh54JsNeR6sgohMN2NLKaobJCL6", "amount": "12.33"}]
        """
        return "GET", CryptoEndpointType._OPTIMAL_FEE.replace(
            "<domain>", CryptoEndpointType._NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        ).replace(
            "<inputs>", "".join([f"{_input}$" for _input in inputs])[:-1]
        ).replace(
            "<outputs>", "".join([f"{_output['address']}$" for _output in outputs])[:-1]
        )

    @staticmethod
    def get_create_transaction(network: str):
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        """
        return "POST", CryptoEndpointType._CREATE_TRANSACTION.replace(
            "<domain>", CryptoEndpointType._NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        )

    @staticmethod
    def get_send_transaction(network: str):
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        """
        return CryptoEndpointType._SEND_TRANSACTION.replace(
            "<domain>", CryptoEndpointType._NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        )