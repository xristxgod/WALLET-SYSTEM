from typing import Union, List, Dict, Optional

from pydantic import BaseModel, Field

from src.models import WalletModel
from src.utils.types import CRYPTOAddress

# <<<===================================>>> Transactions <<<=========================================================>>>

# BODY

class BodyCreateTransaction(BaseModel):
    chat_id: Union[int, bytes] = Field("")
    network: str = Field("")
    inputs: Optional[List[CRYPTOAddress]] = Field("")
    outputs: List[Dict[CRYPTOAddress, str]] = Field("")

    def __init__(self, **kwargs):
        super(BodyCreateTransaction, self).__init__(**kwargs)
        if self.inputs is None:
            self.inputs = [WalletModel.query.filter_by(user_id=self.chat_id)]


class BodySendTransaction(BaseModel):
    pass

# RESPONSE

class ResponseCreateTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")

class ResponseSendTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")