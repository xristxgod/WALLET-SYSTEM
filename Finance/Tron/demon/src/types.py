import decimal
import typing

TPath: str = "m/44'/195'/0'/0/0"            # Tron path


FullNetwork = str                           # TRON-USDT, TRON-TRX
TransactionHash = typing.Union[str, bytes]  # Transaction Hash
TAddress = str                              # Wallet address
TPrivateKey = typing.Union[str, bytes]      # Private key for account
TPublicKey = typing.Union[str, bytes]       # Public key for account

TRON_NETWORK_INDEX = 1
CREATE_TRANSACTION_STATUS_NUMBER = 1

class Coins:

    TRX = ["trx", "tron", "native"]
    TOKEN_USDT = "usdt"

    @staticmethod
    def is_native(coin: str) -> bool:
        return coin.lower() in Coins.TRX

    @staticmethod
    def is_token(coin: str) -> typing.Union[bool, str]:
        for key, value in Coins.__dict__.items():
            if key.startswith('TOKEN_') and coin.lower() in value:
                return value[0].upper()
        else:
            return False

def default_json(json_object: object):
    if isinstance(json_object, decimal.Decimal):
        return float(json_object)
    return str(json_object)