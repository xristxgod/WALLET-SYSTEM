from typing import Union, List, Dict

from pydantic import BaseModel, Field

from src.utils.types import CRYPTOAddress

# <<<===================================>>> Transactions <<<=========================================================>>>

# BODY

class BodyCreateTransaction(BaseModel):
    chat_id: Union[int, bytes] = Field("")
    network: str = Field("")
    inputs: List[CRYPTOAddress] = Field("")
    outputs: List[Dict[CRYPTOAddress, str]] = Field("")

class BodySendTransaction(BaseModel):
    pass

# RESPONSE

class ResponseCreateTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")

class ResponseSendTransaction(BaseModel):
    fee: str = Field("")
    bodyTransaction: Dict = Field("")