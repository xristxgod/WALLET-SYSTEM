import decimal
from typing import Optional, Dict, List, Tuple

from src.types import CRYPTO_ADDRESS, NETWORK, TG_CHAT_ID
from src.sender import SenderToCryptoNode
from config import decimals

class CryptForUser:
    CHAT_ID: Optional[TG_CHAT_ID]
    BASE_FEE: Optional[decimal.Decimal]

    __NATIVE = {
        "TRON": "TRX"
    }

    def __init__(self, inputs: List[CRYPTO_ADDRESS], network: NETWORK, token: str):
        self.__inputs = inputs
        self.network = network
        self.token = token

    async def get_optimal_fee(self, outputs: List[Dict]) -> decimal.Decimal:
        return decimals.create_decimal(
            (
                await SenderToCryptoNode.get_optimal_fee(
                    inputs=self.__inputs, outputs=outputs,
                    network=self.network, token=self.token
                )
            ).get("fee")
        )

    async def get_balances(self, token: Optional[str] = None) -> Dict[CRYPTO_ADDRESS, decimal.Decimal]:
        balances = {}
        for address in self.__inputs:
            balance = await SenderToCryptoNode.get_balance(
                network=self.network,
                token=self.token if token is None else token,
                address=address
            )
            balances.update({
                address: decimals.create_decimal(balance.get("balance"))
            })
        return balances

    async def create_transaction(self, outputs: List[Dict]) -> Optional[Dict]:
        return await SenderToCryptoNode.create_transaction(
            inputs=self.__inputs,
            outputs=outputs,
            network=self.network,
            token=self.token
        )

    async def send_transaction(self, create_tx_hex: str, private_keys: List[str]) -> bool:
        return await SenderToCryptoNode.send_transaction(
            createTxHex=create_tx_hex,
            privateKeys=private_keys,
            network=self.network,
            token=self.token
        ) is None

    # <<<==========================================>>> Utils <<<=====================================================>>>

    def get_outputs(self, outputs: List[Dict]) -> Tuple[str, str, str]:
        to: str = ""
        amount: decimal.Decimal = decimals.create_decimal(0.0)
        for output in outputs:
            to += f"{output.get('address')} "
            amount += decimals.create_decimal(output.get("amount"))
        return to, "%.8f" % amount, f"{self.network.upper()} {self.token.upper()}"

    @property
    def full_network(self) -> str:
        return f"{self.network.upper()}_{self.token.upper()}"

    @property
    def native(self) -> str:
        return self.__NATIVE.get(self.network.upper()).lower()

    def __str__(self):
        return " ".join(self.__inputs)