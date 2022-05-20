import decimal
from typing import Optional, List

from pydantic import BaseModel, Field

from src.types import TAddress

# <<<===================================>>> Helper <<<===============================================================>>>

class BodyInputsOrOutputs(BaseModel):
    """Body for create transaction in outputs"""
    address: TAddress = Field(description="The recipient's wallet address.")
    amount: decimal.Decimal = Field(description="Amount")

# <<<===================================>>> Body <<<=================================================================>>>

class BodyTransaction(BaseModel):
    time: int = Field(description="The time when the transaction was sent")
    transactionHash: str = Field(description="The Transaction Hash")
    fee: Optional[decimal.Decimal] = Field(default=None, description="Transaction fee")
    amount: Optional[decimal.Decimal] = Field(default=None, description="The amount of the shipment")
    inputs: Optional[List[BodyInputsOrOutputs]] = Field(default=None, description="Information about the sender")
    outputs: Optional[List[BodyInputsOrOutputs]] = Field(default=None, description="Information about the recipient")
    token: Optional[str] = Field(default=None, description="Token name")
    data: Optional[str] = Field(default=None, description="This includes what the api could not process")