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

# RESPONSE

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
    message: bool = Field("")