import unittest

from config import Config

TEST_FROM_ADDRESS = "TWCQvcJ2JkWamoXWs7rAf7PiWTYaiB8WHx"
TEST_FROM_PRIVATE_KEY = ["53054a7ebbda440df4f15b225def00dc8abc62a4a5a269a7c6023223a31d7032"]

TEST_TO_ADDRESS = "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA"

TRX_AMOUNT = 0.00001
USDT_AMOUNT = 0.00001

class TestTransaction(unittest.IsolatedAsyncioTestCase):
    pass