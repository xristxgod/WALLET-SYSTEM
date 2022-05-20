import unittest
from src.utils import TronUtils
from src.types import Coins

class TestProjectSyncMethods(unittest.TestCase):

    def test_from_sun(self):
        self.assertEqual(TronUtils.from_sun(0), 0)
        self.assertEqual(TronUtils.from_sun(1_000_000), 1)
        self.assertEqual(str(TronUtils.from_sun(1_740_000)), "1.74")
        self.assertEqual(str(TronUtils.from_sun(1_000_090)), "1.00009")
        self.assertEqual(str(TronUtils.from_sun(2_065_070)), "2.06507")

    def test_coins(self):
        self.assertTrue(Coins.is_native("TRX"))
        self.assertTrue(Coins.is_native("TRON"))
        self.assertTrue(Coins.is_native("NATIVE"))
        self.assertTrue(Coins.is_token("USDT"))