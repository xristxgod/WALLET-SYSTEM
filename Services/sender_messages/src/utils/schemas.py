from typing import Optional, List

from pydantic import BaseModel, Field

from src.utils.types import FULL_NETWORK, CryptAddress, TGChatID, TGUsername

# <<<=====================================>>> Format of received messages <<<========================================>>>

class BodyParticipant(BaseModel):
    address: FULL_NETWORK = Field("Recipient's/Sender's wallet address")
    amount: float = Field("Amount of sending/receiving")

class BodyTransaction(BaseModel):
    time: int = Field(description="Transaction confirmation time")
    transactionHash: str = Field(description="Transaction hash/id")
    fee: float = Field(description="Transaction fee")
    amount: float = Field(description="Transaction amount")
    inputs: List[BodyParticipant] = Field(description="Sender/s of the transaction")
    outputs: List[BodyParticipant] = Field(description="Recipient/s of the transaction")
    token: Optional[str] = Field(description="Tokens/smart-contracts within the network, Example: USDT")

class HeadMessage(BaseModel):
    network: FULL_NETWORK = Field(description="Networks and token, Example: TRON-TRX, TRON-USDT")
    block: int = Field(description="The number of the block in which the transaction was detected!")

class BodyMessage(BaseModel):
    address: CryptAddress = Field(description="Crypto wallet address, Example: THqAa2Nh2sbdSWrxNHfePybGp4exuqgtAf")
    transactions: List[BodyTransaction] = Field(description="Transactions from the specified block in the head!")

# <<<=====================================>>> Format of send messages <<<============================================>>>

class BodyApiBalance(BaseModel):
    chatID: TGChatID = Field(description="Telegram user chat id")
    username: TGUsername = Field(description="Telegram user username")
    network: FULL_NETWORK = Field(description="Full network, Example: TRON-TRX, TRON-USDT")
    amount: float = Field(description="Transaction amount")
    transactionHash: str = Field(description="Transaction hash/id")
    method: Optional[str] = Field(description="Method for sender", default="add")

class BodyApiTransaction(BaseModel):
    chatID: TGChatID = Field(description="Telegram user chat id")
    network: FULL_NETWORK = Field(description="Full network, Example: TRON-TRX, TRON-USDT")
    transactionHash: str = Field(description="Transaction hash/id")
    inputs: List[BodyParticipant] = Field(description="Sender/s of the transaction")
    outputs: List[BodyParticipant] = Field(description="Recipient/s of the transaction")
    fee: float = Field(description="Transaction fee")
    amount: float = Field(description="Transaction amount")
    status: int = Field(description="Transaction status", default=2)