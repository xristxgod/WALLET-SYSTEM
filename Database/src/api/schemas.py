from typing import Union, List, Dict, Optional

from pydantic import BaseModel, Field

from src.models import WalletModel
from src.utils.types import CRYPTOAddress, CRYPTONetwork, CRYPTOMnemonicWords, TGChatID

# <<<===================================>>> Wallet <<<===============================================================>>>
# BODY

class BodyCreateWallet(BaseModel):
    chatID: TGChatID = Field("")
    network: CRYPTONetwork = Field("")
    passphrase: Optional[str] = Field("")
    mnemonic_words: Optional[CRYPTOMnemonicWords] = Field("")

class BodyCheckBalance(BaseModel):
    chatID: TGChatID = Field("")
    network: CRYPTONetwork = Field("")
    address: Optional[CRYPTOAddress] = Field("")
    convert: Optional[List[str]]

    def __init__(self, **kwargs):
        super(BodyCheckBalance, self).__init__(**kwargs)
        if self.address is None:
            self.address = WalletModel.query.filter_by(user_id=self.chatID, network=self.network.split("_")[0]).first()
        if self.convert is not None and isinstance(self.convert, str):
            self.convert = [self.convert]

# RESPONSE

class ResponseCreateWallet(BaseModel):
    message: Union[bool, str] = Field("")

class ResponseCheckBalance(BaseModel):
    balance: str = Field("")
    network: CRYPTONetwork = Field("")
    convert: Optional[List[Dict]] = Field("")

    def __init__(self, **kwargs):
        super(ResponseCheckBalance, self).__init__(**kwargs)
        if self.convert is None:
            del self.convert

# <<<===================================>>> Transactions <<<=========================================================>>>
# BODY

class BodyTransaction(BaseModel):
    chatID: TGChatID = Field("")
    network: CRYPTONetwork = Field("")
    inputs: Optional[List[CRYPTOAddress]] = Field("")
    outputs: List[Dict[CRYPTOAddress, str]] = Field("")

    def __init__(self, **kwargs):
        super(BodyTransaction, self).__init__(**kwargs)
        if self.inputs is None:
            self.inputs = [WalletModel.query.filter_by(user_id=self.chatID).all()]
        if isinstance(self.chatID, bytes) or isinstance(self.chatID, str):
            self.chat_id = int(self.chatID, 0) if self.chatID[:2] == "0x" else int("0x"+self.chatID, 0)

# RESPONSE

class ResponseCreateTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")

class ResponseSendTransaction(BaseModel):
    message: Union[bool, str] = Field("")