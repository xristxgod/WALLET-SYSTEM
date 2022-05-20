import unittest

from src.services.wallet import BodyCreateWallet, wallet

class TestWalletMethodSync(unittest.TestCase):

    def test_create_wallet(self):
        passphrase = "8LzSu11vhSOwnHMpV14wTnECbcn6gsp5"
        mnemonic_words = "loud assume agree illegal brain slight vicious bulb kite decorate blade educate"
        wallet_info = wallet.create_wallet(BodyCreateWallet(
            passphrase=passphrase,
            mnemonicWords=mnemonic_words
        ))
        self.assertEqual(passphrase, wallet_info.passphrase)
        self.assertEqual(mnemonic_words, wallet_info.mnemonicWords)
        self.assertEqual(len(wallet_info.__dict__), 5)
        self.assertEqual("TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH", wallet_info.address)
        self.assertEqual("e3ce95e69da6d6aa843800c4c3be636fffaba32952e066a534098663cc9d7fb5", wallet_info.privateKey)
        self.assertEqual("02d79f9e95151c998f7e91df1fdf58eeff0ded8fd93dd2af153464ec075298e25c", wallet_info.publicKey)
        self.assertTrue(wallet_info.address.startswith("T"))

class TestWalletMethodAsync(unittest.IsolatedAsyncioTestCase):

    async def test_get_balance(self):
        active_address = "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx"
        not_active_address = "TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH"
        balance_usdt_active = await wallet.get_balance(address=active_address, token="usdt")
        balance_usdt_not_active = await wallet.get_balance(address=not_active_address, token="usdt")
        balance_trx_not_active = await wallet.get_balance(address=not_active_address)
        self.assertEqual("0", balance_trx_not_active.balance)
        self.assertEqual("0", balance_usdt_not_active.balance)
        self.assertEqual("USDT", balance_usdt_active.token)
        # await wallet.node.close()

    async def test_get_optimal_fee(self):
        active_address = "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx"
        not_active_address = "TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH"
        self.assertEqual("1.00000000", (await wallet.get_optimal_fee(
            from_address=active_address,
            to_address=not_active_address,
        )).fee)
        await wallet.node.close()