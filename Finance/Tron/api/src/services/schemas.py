import decimal
import json
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, Field
from hdwallet.utils import generate_mnemonic, generate_passphrase

from src.types import TPrivateKey, TPublicKey, TAddress

# <<<===================================>>> Helper <<<===============================================================>>>

class BodyInputsOrOutputs(BaseModel):
    """Body for create transaction in outputs"""
    address: TAddress = Field(description="The recipient's wallet address.")
    amount: decimal.Decimal = Field(description="Amount")

# <<<===================================>>> Body <<<=================================================================>>>

class BodyCreateWallet(BaseModel):
    """Body for create wallet"""
    passphrase: Optional[str] = Field(default=None, description="Secret word for account recovery")
    mnemonicWords: Optional[str] = Field(default=None, description="Mnemonic phrase")

    def __init__(self, **kwargs):
        super(BodyCreateWallet, self).__init__(**kwargs)
        if self.passphrase is None or self.passphrase == "string":
            self.passphrase = generate_passphrase(length=32)
        if self.mnemonicWords is None or self.mnemonicWords == "string":
            self.mnemonicWords = generate_mnemonic(language="english", strength=128)

class BodyGenerateAddress(BaseModel):
    mnemonicWords: str = Field(description="Mnemonic phrase")
    passphrase: Optional[str] = Field(default=None, description="Secret word for account recovery")
    account: Optional[int]
    index: Optional[int]

    def __init__(self, **kwargs):
        super(BodyGenerateAddress, self).__init__(**kwargs)
        if self.account is None or self.account == "string":
            self.account = 0
        if self.mnemonicWords is None or self.mnemonicWords == "string":
            self.index = 1

class BodyCreateTransaction(BaseModel):
    """Create a transaction TRX or Tokens TRC20"""
    inputs: List[TAddress] = Field(description="Sender addresses")
    outputs: List[BodyInputsOrOutputs] = Field(description="Recipient addresses")

    def __init__(self, **kwargs):
        super(BodyCreateTransaction, self).__init__(**kwargs)
        if isinstance(self.outputs, str):
            self.outputs = json.loads(self.outputs)
        if isinstance(self.inputs, list):
            self.fromAddress = self.inputs[0]

class BodySignAndSendTransaction(BaseModel):
    """Sign and send transaction"""
    createTxHex: str = Field(description="The hex of the unsigned transaction")
    privateKeys: List[TPrivateKey] = Field(description="The private key of the sender")

    def __init__(self, **kwargs):
        super(BodySignAndSendTransaction, self).__init__(**kwargs)
        if isinstance(self.privateKeys, str):
            self.privateKeys = json.loads(self.privateKeys)

# <<<----------------------------------->>> Response <<<------------------------------------------------------------->>>

class ResponseCreateWallet(BaseModel):
    """Response for create wallet"""
    passphrase: str = Field(description="Secret word for account recovery")
    mnemonicWords: str = Field(description="Mnemonic phrase")
    privateKey: TPrivateKey = Field(description="Private key for account")
    publicKey: TPublicKey = Field(description="Public key for account")
    address: TAddress = Field(description="Wallet address")

class ResponseGetOptimalFee(BaseModel):
    fee: decimal.Decimal

class ResponseGetBalance(BaseModel):
    """Response for get balance"""
    balance: decimal.Decimal
    token: str = None

    def __init__(self, **kwargs):
        super(ResponseGetBalance, self).__init__(**kwargs)
        if self.token is None:
            del self.token

class ResponseSignAndSendTransaction(BaseModel):
    time: int = Field(description="The time when the transaction was sent")
    transactionHash: str = Field(description="The Transaction Hash")
    fee: Optional[decimal.Decimal] = Field(default=None, description="Transaction fee")
    amount: Optional[decimal.Decimal] = Field(default=None, description="The amount of the shipment")
    inputs: Optional[List[BodyInputsOrOutputs]] = Field(default=None, description="Information about the sender")
    outputs: Optional[List[BodyInputsOrOutputs]] = Field(default=None, description="Information about the recipient")
    token: Optional[str] = Field(default=None, description="Token name")
    data: Optional[Dict] = Field(default=None, description="This includes what the api could not process")

    def __init__(self, **kwargs):
        super(ResponseSignAndSendTransaction, self).__init__(**kwargs)
        if self.token is None:
            del self.token
        if self.data is None:
            del self.data

class ResponseCreateTransaction(BaseModel):
    """Response to create transaction"""
    createTxHex: str = Field(description="The hex of the unsigned transaction")
    bodyTransaction: ResponseSignAndSendTransaction = Field(description="Transaction body in json")
    fee: decimal.Decimal = Field(description="Transaction fee")

class ResponseAllTransaction(BaseModel):
    address: TAddress = Field(description="Wallet address")
    transactions: Optional[List[ResponseSignAndSendTransaction]] = Field(description="All transactions", default=None)
