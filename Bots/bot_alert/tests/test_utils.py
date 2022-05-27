import unittest
from src.utils import Utils
from src.types import CoinsURL

class TestUtils(unittest.TestCase):

    def test_get_message_id(self):
        message_id = Utils.get_message_id({"result": {"message_id": 1}})
        self.assertEqual(1, message_id)

    def test_get_blockchain_url(self):
        url = CoinsURL.get_blockchain_url_by_network("TRON")
        self.assertIn(url, ["https://shasta.tronscan.org/", "https://tronscan.org/"])

    def test_get_native(self):
        native = CoinsURL.get_native_by_network(network="TRON")
        self.assertEqual("TRX", native)