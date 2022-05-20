import unittest
from src.services.wallet import BodyCreateWallet, wallet

class TestProjectMethods(unittest.TestCase):

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
        self.assertTrue(wallet_info.address.startswith("T"))

    def test_get_balance(self):
        active_address = ""
        not_active_address = "TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH"