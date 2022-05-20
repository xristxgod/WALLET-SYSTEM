import unittest
from typing import Optional

from src.services.schemas import BodyCreateTransaction, BodyInputsOrOutputs, ResponseCreateTransaction
from src.services.wallet import wallet
from config import Config, decimals

TEST_FROM_ADDRESS = "TWCQvcJ2JkWamoXWs7rAf7PiWTYaiB8WHx"
TEST_FROM_PRIVATE_KEY = "53054a7ebbda440df4f15b225def00dc8abc62a4a5a269a7c6023223a31d7032"

TEST_TO_ADDRESS = "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA"

TRX_AMOUNT = decimals.create_decimal(0.00001)
USDT_AMOUNT = decimals.create_decimal(0.00001)

CREATE_TX_DATA: Optional[ResponseCreateTransaction] = None

class TestTransaction(unittest.IsolatedAsyncioTestCase):

    async def test_create_transaction(self):
        if Config.NETWORK != "TESTNET":
            raise "This is a mainnet bro! don't cry and rename: MAINNET -> TESTNET"
        global CREATE_TX_DATA
        create_transaction_trx = await wallet.create_transaction(BodyCreateTransaction(
            inputs=[TEST_FROM_ADDRESS],
            outputs=[BodyInputsOrOutputs(address=TEST_TO_ADDRESS, amount=TRX_AMOUNT)]
        ))
        CREATE_TX_DATA = create_transaction_trx
        self.assertEqual(3, len(CREATE_TX_DATA.__dict__.keys()))
        self.assertIn("createTxHex", CREATE_TX_DATA.__dict__.keys())
        self.assertIn("bodyTransaction", CREATE_TX_DATA.__dict__.keys())
        self.assertIn("fee", CREATE_TX_DATA.__dict__.keys())
        self.assertEqual(TEST_FROM_ADDRESS, CREATE_TX_DATA.bodyTransaction.inputs[0].address)
        self.assertEqual(TRX_AMOUNT, CREATE_TX_DATA.bodyTransaction.inputs[0].amount)
        self.assertEqual(TEST_TO_ADDRESS, CREATE_TX_DATA.bodyTransaction.outputs[0].address)
        self.assertEqual(TRX_AMOUNT, CREATE_TX_DATA.bodyTransaction.outputs[0].amount)

    async def test_send_transaction(self):
        pass

