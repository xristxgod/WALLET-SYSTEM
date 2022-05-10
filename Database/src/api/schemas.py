from typing import Union, List, Dict, Optional

from pydantic import BaseModel, Field

from src.models import WalletModel
from src.utils.types import CRYPTOAddress

# <<<===================================>>> Transactions <<<=========================================================>>>

# BODY

class BodyTransaction(BaseModel):
    chat_id: Union[int, bytes] = Field("")
    network: str = Field("")
    inputs: Optional[List[CRYPTOAddress]] = Field("")
    outputs: List[Dict[CRYPTOAddress, str]] = Field("")

    def __init__(self, **kwargs):
        super(BodyTransaction, self).__init__(**kwargs)
        if self.inputs is None:
            self.inputs = [WalletModel.query.filter_by(user_id=self.chat_id)]
        if isinstance(self.chat_id, bytes) or isinstance(self.chat_id, str):
            self.chat_id = int(self.chat_id, 0) if self.chat_id[:2] == "0x" else int("0x"+self.chat_id, 0)

# RESPONSE

class ResponseCreateTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")

class ResponseSendTransaction(BaseModel):
    message: bool = Field("")