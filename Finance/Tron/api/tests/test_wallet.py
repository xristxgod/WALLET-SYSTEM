import unittest

from tests.__init__ import *
from src.services.wallet import BodyCreateWallet, wallet
from src.services.transactions import TransactionParser

class TestWalletMethodSync(unittest.TestCase):

    def test_create_wallet(self):
        wallet_info = wallet.create_wallet(BodyCreateWallet(
            passphrase=TEST_PASSPHRASE,
            mnemonicWords=TEST_MNEMONIC_WORDS
        ))
        self.assertEqual(TEST_PASSPHRASE, wallet_info.passphrase)
        self.assertEqual(TEST_MNEMONIC_WORDS, wallet_info.mnemonicWords)
        self.assertEqual(len(wallet_info.__dict__), 5)
        self.assertEqual(TEST_NOT_ACTIVE_ADDRESS, wallet_info.address)
        self.assertEqual(TEST_PRIVATE_KEY, wallet_info.privateKey)
        self.assertEqual(TEST_PUBLIC_KEY, wallet_info.publicKey)
        self.assertTrue(wallet_info.address.startswith("T"))

class TestWalletMethodAsync(unittest.IsolatedAsyncioTestCase):

    async def test_get_balance(self):
        balance_usdt_active = await wallet.get_balance(address=TEST_ACTIVE_ADDRESS, token="usdt")
        balance_usdt_not_active = await wallet.get_balance(address=TEST_NOT_ACTIVE_ADDRESS, token="usdt")
        balance_trx_not_active = await wallet.get_balance(address=TEST_NOT_ACTIVE_ADDRESS)
        self.assertEqual("0", balance_trx_not_active.balance)
        self.assertEqual("0", balance_usdt_not_active.balance)
        self.assertEqual("USDT", balance_usdt_active.token)

    async def test_get_optimal_fee(self):
        self.assertEqual("1.00000000", (await wallet.get_optimal_fee(
            from_address=TEST_ACTIVE_ADDRESS,
            to_address=TEST_NOT_ACTIVE_ADDRESS,
        )).fee)
        await wallet.node.close()

    async def test_get_transaction_by_tx_hash(self):
        trx_tx_data = await TransactionParser().get_transaction(transaction_hash=TEST_TX_HASH_TRX)
        usdt_tx_data = await TransactionParser().get_transaction(transaction_hash=TEST_TX_HASH_USDT)
        print(usdt_tx_data)
        self.assertEqual(TX_DATA_TRX, trx_tx_data)
        self.assertEqual(TX_DATA_USDT, usdt_tx_data)