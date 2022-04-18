import typing

TransactionHash = typing.Union[str, bytes]  # Transaction Hash
TAddress = str                              # Wallet address
TPrivateKey = typing.Union[str, bytes]      # Private key for account
TPublicKey = typing.Union[str, bytes]       # Public key for account

class Coins:

    TRX = "trx"
    TOKEN_USDT = "usdt"

    @staticmethod
    def is_native(coin: str):
        return coin.lower() == Coins.TRX

    @staticmethod
    def is_token(coin: str):
        return coin.lower() in [value for key, value in Coins.__dict__.items() if key.startswith('TOKEN_')]