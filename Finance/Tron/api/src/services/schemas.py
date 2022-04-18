import json
from typing import Optional, List, Dict

from pydantic import BaseModel, Field
from hdwallet.utils import generate_mnemonic, generate_passphrase

from src.types import TPrivateKey, TPublicKey, TAddress

# <<<----------------------------------->>> Body <<<----------------------------------------------------------------->>>

class BodyCreateWallet(BaseModel):
    """Body for create wallet"""
    passphrase: Optional[str] = Field(default=None, description="Secret word for account recovery")
    mnemonic_words: Optional[str] = Field(default=None, description="Mnemonic phrase")

    def __init__(self, **kwargs):
        super(BodyCreateWallet, self).__init__(**kwargs)
        if self.passphrase is None or self.passphrase == "string":
            self.passphrase = generate_passphrase(length=32)
        if self.mnemonic_words is None or self.mnemonic_words == "string":
            self.mnemonic_words = generate_mnemonic(language="english", strength=128)

class BodyCreateTransaction(BaseModel):
    """Create a transaction TRX or Tokens TRC20"""
    fromAddress: TAddress = Field(default=None, description="Sender's address")
    outputs: Optional[List[Dict]] = Field(description="Sender's address")

    def __init__(self, **kwargs):
        super(BodyCreateTransaction, self).__init__(**kwargs)
        if isinstance(self.outputs, str):
            self.outputs = json.loads(self.outputs)

class BodySignAndSendTransaction(BaseModel):
    """Sign and send transaction"""
    createTxHex: str = Field(description="The hex of the unsigned transaction")
    privateKeys: List[TPrivateKey] = Field(default=None, description="The private key of the sender")

    def __init__(self, **kwargs):
        super(BodySignAndSendTransaction, self).__init__(**kwargs)
        if isinstance(self.privateKeys, str):
            self.privateKeys = json.loads(self.privateKeys)

# <<<----------------------------------->>> Response <<<------------------------------------------------------------->>>

class ResponseCreateWallet(BaseModel):
    """Response for create wallet"""
    passphrase: str = Field(description="Secret word for account recovery")
    mnemonic_words: str = Field(description="Mnemonic phrase")
    privateKey: TPrivateKey = Field(description="Private key for account")
    publicKey: TPublicKey = Field(description="Public key for account")
    address: TAddress = Field(description="Wallet address")

class ResponseGetOptimalFee(BaseModel):
    fee: str

class ResponseGetBalance(BaseModel):
    """Response for get balance"""
    balance: str
    token: str = None

    def __init__(self, **kwargs):
        super(ResponseGetBalance, self).__init__(**kwargs)
        if self.token is None:
            del self.token

class ResponseCreateTransaction(BaseModel):
    """Response to create transaction"""
    createTxHex: str = Field(description="The hex of the unsigned transaction")
    bodyTransaction: dict = Field(description="Transaction body in json")
    fee: str = Field(description="Transaction fee")

class ResponseSignAndSendTransaction(BaseModel):
    pass