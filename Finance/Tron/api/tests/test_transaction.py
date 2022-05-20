import unittest
from typing import Optional

from src.services.schemas import (
    BodyCreateTransaction,
    BodySignAndSendTransaction,
    BodyInputsOrOutputs,
    ResponseCreateTransaction,
    ResponseSignAndSendTransaction
)
from src.services.wallet import wallet
from config import Config, decimals

TEST_FROM_ADDRESS = "TWCQvcJ2JkWamoXWs7rAf7PiWTYaiB8WHx"
TEST_FROM_PRIVATE_KEY = "53054a7ebbda440df4f15b225def00dc8abc62a4a5a269a7c6023223a31d7032"

TEST_TO_ADDRESS = "THadHjK1UhZvnHaVPYNTsTDCR3mPd8XXDK"

NATIVE_AMOUNT = decimals.create_decimal(0.00001)
USDT_AMOUNT = decimals.create_decimal(0.00001)

IS_TOKEN = False

CREATE_TRANSACTION: Optional[ResponseCreateTransaction] = None

class TestTransaction(unittest.IsolatedAsyncioTestCase):

    async def test_create_transaction(self):
        if Config.NETWORK != "TESTNET":
            raise "This is a mainnet bro! don't cry and rename: MAINNET -> TESTNET"
        global CREATE_TRANSACTION
        CREATE_TRANSACTION = await wallet.create_transaction(
            body=BodyCreateTransaction(
                inputs=[TEST_FROM_ADDRESS],
                outputs=[BodyInputsOrOutputs(address=TEST_TO_ADDRESS, amount=NATIVE_AMOUNT)]
            ),
            token="USDT" if IS_TOKEN else "TRX"
        )
        self.assertEqual(ResponseCreateTransaction, type(CREATE_TRANSACTION))
        self.assertEqual(3, len(CREATE_TRANSACTION.__dict__.keys()))
        self.assertIn("createTxHex", CREATE_TRANSACTION.__dict__.keys())
        self.assertIn("bodyTransaction", CREATE_TRANSACTION.__dict__.keys())
        self.assertIn("fee", CREATE_TRANSACTION.__dict__.keys())
        self.assertEqual(TEST_FROM_ADDRESS, CREATE_TRANSACTION.bodyTransaction.inputs[0].address)
        self.assertEqual(NATIVE_AMOUNT, CREATE_TRANSACTION.bodyTransaction.inputs[0].amount)
        self.assertEqual(TEST_TO_ADDRESS, CREATE_TRANSACTION.bodyTransaction.outputs[0].address)
        self.assertEqual(NATIVE_AMOUNT, CREATE_TRANSACTION.bodyTransaction.outputs[0].amount)

    async def test_send_transaction(self):
        if CREATE_TRANSACTION is None:
            raise Exception("This test only works in conjunction with 'TestTransaction.test_create_transaction'")
        SUCCESSFULLY_TRANSACTION: Optional[ResponseSignAndSendTransaction] = await wallet.sign_and_send_transaction(
            body=BodySignAndSendTransaction(
                createTxHex=CREATE_TRANSACTION.createTxHex,
                privateKeys=[TEST_FROM_PRIVATE_KEY]
            )
        )
        self.assertEqual(ResponseSignAndSendTransaction, type(SUCCESSFULLY_TRANSACTION))
        self.assertEqual(7 if IS_TOKEN else 6, len(SUCCESSFULLY_TRANSACTION.__dict__.keys()))
        self.assertEqual(SUCCESSFULLY_TRANSACTION.transactionHash, CREATE_TRANSACTION.bodyTransaction.transactionHash)
        self.assertEqual(NATIVE_AMOUNT, SUCCESSFULLY_TRANSACTION.amount)
        self.assertEqual(TEST_FROM_ADDRESS, SUCCESSFULLY_TRANSACTION.inputs[0].address)
        self.assertEqual(NATIVE_AMOUNT, SUCCESSFULLY_TRANSACTION.inputs[0].amount)
        self.assertEqual(TEST_TO_ADDRESS, SUCCESSFULLY_TRANSACTION.outputs[0].address)
        self.assertEqual(NATIVE_AMOUNT, SUCCESSFULLY_TRANSACTION.outputs[0].amount)