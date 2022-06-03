from typing import Optional, Union

# <<<=====================================>>> Crypro data <<<========================================================>>>

CRYPTO_TRANSACTION_HASH = str               # Crypto transaction hash
CRYPTO_NETWORK = str                        # Crypto network
CRYPTO_ADDRESS = str                        # Crypto wallet address
CRYPTO_MNEMONIC = str                       # Crypto wallet mnemonic phrase

# <<<=====================================>>> Telegram data <<<======================================================>>>

TELEGRAM_USER_ID = Union[int, bytes]        # Telegram user chat id


class CoinHelper:
    TRON = "TRX"

    @staticmethod
    def get_native_coin(network: CRYPTO_NETWORK) -> Optional[str]:
        return CoinHelper.__dict__.get(network)