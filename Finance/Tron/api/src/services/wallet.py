import typing
import json

import tronpy.exceptions
import tronpy.tron
from hdwallet import BIP44HDWallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import TronMainnet

from src.services.transactions import get_transaction_by_tx_hash
from src.services.schemas import (
    ResponseCreateWallet, BodyCreateWallet, ResponseGetBalance,
    ResponseGetOptimalFee, BodyCreateTransaction, BodySignAndSendTransaction,
    ResponseCreateTransaction, ResponseSignAndSendTransaction, BodyGenerateAddress,
    BodyInputsOrOutputs
)
from src.services import NodeTron
from src.utils import TransactionUtils, TronUtils
from src.types import TAddress
from src import DB
from config import Config, logger, decimals

class TronMethods(NodeTron):
    """This class creates and use a Tron account"""
    @staticmethod
    def create_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        """Create a tron wallet"""
        hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=TronMainnet)
        hdwallet.from_mnemonic(mnemonic=body.mnemonicWords, language="english", passphrase=body.passphrase)
        return ResponseCreateWallet(
            passphrase=body.passphrase,
            mnemonicWords=body.mnemonicWords,
            privateKey=hdwallet.private_key(),
            publicKey=hdwallet.public_key(),
            address=hdwallet.address()
        )

    @staticmethod
    def generate_acc_by_mnemonic(body: BodyGenerateAddress) -> ResponseCreateWallet:
        """Generate a tron wallet by mnemonic"""
        hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=TronMainnet)
        hdwallet.from_mnemonic(mnemonic=body.mnemonicWords, language="english", passphrase=body.passphrase)
        hdwallet.clean_derivation()
        derivation = BIP44Derivation(cryptocurrency=TronMainnet, account=body.account, change=False, address=body.index)
        hdwallet.from_path(path=derivation)
        return ResponseCreateWallet(
            passphrase=body.passphrase,
            mnemonicWords=body.mnemonicWords,
            privateKey=hdwallet.private_key(),
            publicKey=hdwallet.public_key(),
            address=hdwallet.address()
        )

    async def get_balance(self, address: TAddress, token: typing.Optional[str] = None) -> ResponseGetBalance:
        balance = 0
        address = TronUtils.is_hex_address(address=address)
        if token is None:
            try:
                balance = await self.node.get_account_balance(addr=address)
            except Exception as error:
                logger.error(f"ERROR STEP 29: {error}")
        else:
            token_info = await DB.get_token_info(token=token.upper())
            contract = await self.node.get_contract(token_info["address"])
            if int(await contract.functions.balanceOf(address)) > 0:
                balance = int(await contract.functions.balanceOf(address)) / 10 ** token_info["decimals"]
        return ResponseGetBalance(
            balance=balance,
            token=None if token is None else token.upper()
        )

    async def get_optimal_fee(self, from_address: TAddress, to_address: TAddress, token: str = "TRX") -> ResponseGetOptimalFee:
        fee = 0
        from_address = TronUtils.is_hex_address(address=from_address)
        to_address = TronUtils.is_hex_address(address=to_address)
        if from_address == to_address:
            raise tronpy.exceptions.AddressNotFound('The transaction cannot be executed to the same address.')
        if token.upper() in ["TRX", "TRON"]:
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
        return ResponseGetOptimalFee(fee=fee)

    async def create_transaction(
            self, body: BodyCreateTransaction, token: typing.Optional[str] = "TRX"
    ) -> ResponseCreateTransaction:
        outputs: BodyInputsOrOutputs = body.outputs[0]
        if token == "TRX":
            # Checks the correctness of the data entered by users
            amount = NodeTron.toSun(float(outputs.amount))
            # Resources that will go to the transaction
            fee = await self.get_optimal_fee(
                from_address=body.inputs[0],
                to_address=outputs.address,
                token=token
            )
            # Creates and build a transaction
            txn = self.node.trx.transfer(from_=body.inputs[0], to=outputs.address, amount=amount)
            txn = await txn.build()
            body_transaction = TransactionUtils.get_transaction_body(
                txn=txn.to_json(), fee=fee.fee, amount=NodeTron.fromSun(amount),
                from_address=body.inputs[0], to_address=outputs.address
            )
        else:
            # Token information
            token_info = await DB.get_token_info(token=token)
            # Connecting to a smart contract
            contract = await self.node.get_contract(addr=token_info["address"])
            # Let's get the amount for the offspring in decimal
            amount = int(float(outputs.amount) * 10 ** int(token_info["decimals"]))
            # Checks whether the user has a tokens balance to transfer
            if int(await contract.functions.balanceOf(body.inputs[0])) * 10 ** int(token_info["decimals"]) < amount:
                raise Exception("You do not have enough funds on your balance to make a transaction!!!")
            fee = await self.get_optimal_fee(from_address=body.inputs[0], to_address=outputs.address, token=token)
            # Creating a transaction
            txn = await contract.functions.transfer(outputs.address, amount)
            txn = txn.with_owner(body.inputs[0])
            txn = await txn.build()
            body_transaction = TransactionUtils.get_transaction_body(
                txn=txn.to_json(), fee=fee.fee, amount=float(amount / 10 ** int(token_info["decimals"])), token=token,
                from_address=body.inputs[0], to_address=outputs.address
            )
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
        return await get_transaction_by_tx_hash(
            tx_hash=tronpy.tron.Transaction(
                client=tronpy.tron.Tron(
                    provider=tronpy.tron.HTTPProvider(Config.NODE_URL) if NodeTron.NETWORK == "mainnet" else None,
                    network=NodeTron.NETWORK
                ),
                raw_data=json.loads(bytes.fromhex(body.createTxHex).decode("utf-8"))
            ).sign(
                priv_key=tronpy.tron.PrivateKey(
                    private_key_bytes=bytes.fromhex(
                        body.privateKeys[0]
                    )
                )
            ).broadcast().txid
        )

wallet = TronMethods()