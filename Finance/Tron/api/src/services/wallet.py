import typing
import json

import tronpy.exceptions
import tronpy.async_tron
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import TronMainnet

from src.services.transactions import transaction_parser
from src.services.schemas import (
    ResponseCreateWallet, BodyCreateWallet, ResponseGetBalance,
    ResponseGetOptimalFee, BodyCreateTransaction, BodySignAndSendTransaction,
    ResponseCreateTransaction, ResponseSignAndSendTransaction
)
from src.services import NodeTron
from src.utils import TransactionUtils
from src.types import TAddress
from src import DB
from config import logger, decimals

class TronMethods(NodeTron):
    """This class creates and use a Tron account"""
    @staticmethod
    def create_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        """Create a tron wallet"""
        hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=TronMainnet)
        hdwallet.from_mnemonic(mnemonic=body.mnemonic_words, language="english", passphrase=body.passphrase)
        return ResponseCreateWallet(
            passphrase=body.passphrase,
            mnemonic_words=body.mnemonic_words,
            privateKey=hdwallet.private_key(),
            publicKey=hdwallet.public_key(),
            address=hdwallet.address()
        )

    async def get_balance(self, address: TAddress, token: typing.Optional[str] = None) -> ResponseGetBalance:
        if token is None:
            try:
                balance = await self.node.get_account_balance(addr=address)
            except Exception as error:
                logger.error(f"ERROR STEP 29: {error}")
                balance = 0
        else:
            token_info = await DB.get_token_info(token=token.upper())
            contract = await self.node.get_contract(token_info["address"])
            if int(await contract.functions.balanceOf(address)) > 0:
                balance = int(await contract.functions.balanceOf(address)) / 10 ** token_info["decimals"]
            else:
                balance = 0
        return ResponseGetBalance(
            balance="%.8f" % decimals.create_decimal(balance) if balance > 0 else 0
        )

    async def get_optimal_fee(self, from_address: TAddress, to_address: TAddress, token: str) -> ResponseGetOptimalFee:
        fee = 0
        if token == "TRX":
            try:
                _ = await self.node.get_account(to_address)
            except tronpy.exceptions.AddressNotFound:
                fee += 1.0
            bd = 267
        else:
            token_info = await DB.get_token_info(token=token.upper())
            contract = await self.node.get_contract(token_info["address"])
            if int(await contract.functions.balanceOf(to_address)) > 0:
                energy = token_info["token_info"]["isBalanceNotNullEnergy"]
            else:
                energy = token_info["token_info"]["isBalanceNullEnergy"]
            fee = await self.get_energy(address=from_address, energy=energy) / await self.calculate_burn_energy(1)
            bd = token_info["token_info"]["bandwidth"]
        if int((await self.get_account_bandwidth(address=from_address))["totalBandwidth"]) <= bd:
            fee += decimals.create_decimal(267) / 1_000
        return ResponseGetOptimalFee(fee="%.8f" % fee if fee > 0 else fee)

    async def create_transaction(
            self, body: BodyCreateTransaction, token: typing.Optional[str] = None
    ) -> ResponseCreateTransaction:
        if token == "TRX":
            to_address, to_amount = list(body.outputs[0].items())[0]
            # Checks the correctness of the data entered by users
            amount = NodeTron.toSun(float(to_amount))
            # Resources that will go to the transaction
            fee = await self.get_optimal_fee(
                from_address=body.fromAddress,
                to_address=to_address,
                token=token
            )
            # Creates and build a transaction
            txn = self.node.trx.transfer(from_=body.fromAddress, to=to_address, amount=amount)
            txn = await txn.build()
            body_transaction = TransactionUtils.get_transaction_body(txn=txn.to_json())
        else:
            to_address, to_amount = list(body.outputs[0].items())[0]
            # Token information
            token_info = await DB.get_token_info(token=token)
            # Connecting to a smart contract
            contract = await self.node.get_contract(addr=token_info["address"])
            # Let's get the amount for the offspring in decimal
            amount = int(float(to_amount) * 10 ** int(token_info["decimals"]))
            # Checks whether the user has a tokens balance to transfer
            if int(await contract.functions.balanceOf(to_address)) * 10 ** int(token_info["decimals"]) < amount:
                raise Exception("You do not have enough funds on your balance to make a transaction!!!")
            fee = await self.get_optimal_fee(from_address=body.fromAddress, to_address=to_address, token=token)
            # Creating a transaction
            txn = await contract.functions.transfer(to_address, amount).with_owner(body.fromAddress)
            txn = await txn.build()
            body_transaction = TransactionUtils.get_transaction_body(txn=txn.to_json())
        return ResponseCreateTransaction(
            # The original transaction data for signing and sending the transaction
            createTxHex=json.dumps(txn.to_json()["raw_data"]).encode("utf-8").hex(),
            # The body of the transaction, you can find out all the details from it
            bodyTransaction=body_transaction,
            # Transaction fee
            fee=fee.fee,
        )

    @staticmethod
    async def sign_and_send_transaction(body: BodySignAndSendTransaction) -> ResponseSignAndSendTransaction:
        """Sign and Send a transaction"""
        # Verification of the private key
        private_key = tronpy.async_tron.PrivateKey(private_key_bytes=bytes.fromhex(body.privateKeys[0]))
        # Unpacking the original transaction data.
        raw_data = json.loads(bytes.fromhex(body.createTxHex).decode("utf-8"))
        # Signing the transaction with a private key.
        sign_transaction = tronpy.async_tron.AsyncTransaction(
            client=NodeTron().node, raw_data=raw_data
        ).sign(priv_key=private_key)
        # Sending a transaction
        send_transaction = await sign_transaction.broadcast()
        # After sending, we receive the full body of the transaction (checklist)
        return ResponseSignAndSendTransaction(
            **(await transaction_parser.get_transaction(transaction_hash=send_transaction["id"])[0])
        )

wallet = TronMethods()