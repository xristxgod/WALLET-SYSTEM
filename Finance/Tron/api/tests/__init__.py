from config import Config

__NETWORK = Config.NETWORK

TEST_ACTIVE_ADDRESS = "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx"
TEST_NOT_ACTIVE_ADDRESS = "TR3aMFx8mYZEcbno6nJAnparYYp8ZgGrLH"
TEST_PRIVATE_KEY = "e3ce95e69da6d6aa843800c4c3be636fffaba32952e066a534098663cc9d7fb5"
TEST_PUBLIC_KEY = "02d79f9e95151c998f7e91df1fdf58eeff0ded8fd93dd2af153464ec075298e25c"
TEST_PASSPHRASE = "loud assume agree illegal brain slight vicious bulb kite decorate blade educate"
TEST_MNEMONIC_WORDS = "loud assume agree illegal brain slight vicious bulb kite decorate blade educate"

TEST_TX_HASH_TRX_TESTNET = "814cdea067b52b2d718690bce0948aa6aa6f4e0fac55aa00dfca88981e457a65"
TEST_TX_HASH_TRX_MAINNET = "4d9bf6dc1af8c2786c37841f95ea7a0125b8dc6c7fb0c941105168a247ab2f02"

TEST_TX_HASH_USDT_TESTNET = "0e6040350685e40c1a56f54484a79d2b062c31f39307aecf8f728254dfea697e"
TEST_TX_HASH_USDT_MAINNET = "217465af653081e204382e845c31f717fa7b67a76ae773b0847d37d46fb91c23"

TEST_TX_HASH_TRX = TEST_TX_HASH_TRX_TESTNET if __NETWORK == "TESTNET" else TEST_TX_HASH_TRX_MAINNET
TEST_TX_HASH_USDT = TEST_TX_HASH_USDT_TESTNET if __NETWORK == "TESTNET" else TEST_TX_HASH_USDT_MAINNET

TX_DATA_TRX = [{
    "time": 1650391958848 if __NETWORK == "TESTNET" else 1643978763710,
    "transactionHash": TEST_TX_HASH_TRX_TESTNET if __NETWORK == "TESTNET" else TEST_TX_HASH_TRX_MAINNET,
    "fee": 0,
    "amount": "4.83168000" if __NETWORK == "TESTNET" else "2.13128700",
    "senders": [
        {
            "address": "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx",
            "amount": "4.83168000" if __NETWORK == "TESTNET" else "2.13128700"
        }
    ],
    "recipients": [
        {
            "address": "TUtHbnkPe5j9XoV8bLpWBTHv8FycxXvn3h" if __NETWORK == "TESTNET" else "TSUMnKToM3F31cxLWqW94rJJQ8WZHDLYat",
            "amount": "4.83168000" if __NETWORK == "TESTNET" else "2.13128700"
        }
    ],
}]
TX_DATA_USDT = [{
    "time": 1650894664361 if __NETWORK == "TESTNET" else 1643974612928,
    "transactionHash": TEST_TX_HASH_USDT_TESTNET if __NETWORK == "TESTNET" else TEST_TX_HASH_USDT_MAINNET,
    "fee": 0 if __NETWORK == "TESTNET" else "4.09668000",
    "amount": "5.00000000" if __NETWORK == "TESTNET" else "20.00000000",
    "senders": [
        {
            "address": "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx" if __NETWORK == "TESTNET" else "TCbZxFBERYu2jfmg3jKMZN1f6i5KEGnkFi",
            "amount": "5.00000000" if __NETWORK == "TESTNET" else "20.00000000"
        }
    ],
    "recipients": [
        {
            "address": "TJsaD5WvpzrYF2XN3DaiUjqjnJkZAzZUwC" if __NETWORK == "TESTNET" else "TPvxLpLeC1Rd13CymBVWnXJiURjWk3SfRx",
            "amount": "5.00000000" if __NETWORK == "TESTNET" else "20.00000000"
        }
    ],
    "token": "USDT"
}]