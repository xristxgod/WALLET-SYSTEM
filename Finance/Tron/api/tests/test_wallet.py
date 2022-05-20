import unittest

from src.services.wallet import BodyCreateWallet, wallet

TEST_ACTIVE_ADDRESS = "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx"
TEST_NOT_ACTIVE_ADDRESS = "TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH"
TEST_PRIVATE_KEY = "e3ce95e69da6d6aa843800c4c3be636fffaba32952e066a534098663cc9d7fb5"
TEST_PUBLIC_KEY = "02d79f9e95151c998f7e91df1fdf58eeff0ded8fd93dd2af153464ec075298e25c"
TEST_PASSPHRASE = "loud assume agree illegal brain slight vicious bulb kite decorate blade educate"
TEST_MNEMONIC_WORDS = "loud assume agree illegal brain slight vicious bulb kite decorate blade educate"

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