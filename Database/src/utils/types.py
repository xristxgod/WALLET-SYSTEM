from config import Config

CRYPTOAddress = str

class CryptoEndpointType(object):
    CREATE_WALLET = "<domain>/api/<network>/create/wallet"
    BALANCE = "<domain>/api/<network>/balance/<address>"

    OPTIMAL_FEE = "<domain>/api/<network>/fee/<inputs>&<outputs>"

    CREATE_TRANSACTION = "<domain>/api/<network>/create/transaction"
    SEND_TRANSACTION = "<domain>/api/<network>/create/transaction"

    NETWORKS = {
        "TRON": Config.DOMAIN_TRON_API
    }

    @staticmethod
    def get_create_wallet_url(network: str) -> str:
        """
        :type network: NETWORK_TOKEN = TRON_USDT, TRON_TRX
        :return:
        """
        return CryptoEndpointType.CREATE_WALLET.replace(
            "<domain>", CryptoEndpointType.NETWORKS.get(network.split("_")[0])
        ).replace(
            "<network>", network.split("_")[1].lower()
        )