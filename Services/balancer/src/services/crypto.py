import decimal
from typing import Optional, Dict, List

from src.types import CRYPTO_ADDRESS, NETWORK
from src.sender import SenderToCryptoNode
from config import decimals

class CryptForUser:

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

    async def get_balances(self, token: Optional[str] = None):
        balances = {}
        for address in self.__inputs:
            balance = await SenderToCryptoNode.get_balance(
                network=self.network,
                token=self.token,
                address=address
            )
            balances.update({
                address: decimals.create_decimal(balance.get("balance"))
            })
        return balances

    async def create_transaction(self, outputs: List[Dict]) -> Dict:
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