import typing

TRON_GRID_API_KEY: str = "16c3b7ca-d498-4314-aa1d-a224135faa26"

TPath: str = "m/44'/195'/0'/0/0"            # Tron path

TransactionHash = typing.Union[str, bytes]  # Transaction Hash
TAddress = str                              # Wallet address
TPrivateKey = typing.Union[str, bytes]      # Private key for account
TPublicKey = typing.Union[str, bytes]       # Public key for account

class Coins:

    TRX = ["trx", "tron", "native"]
    TOKEN_USDT = ["usdt"]

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
