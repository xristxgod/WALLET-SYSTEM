from typing import Optional, List

from pydantic import BaseModel, Field
from src.types import TGMessage, TGChatID

# <<<=================================>>> User endpoint <<<==========================================================>>>

# <<< Body >>>

class BodyRegUser(BaseModel):
    chat_id: TGChatID = Field(description="ID of the new user")
    username: Optional[str] = Field(default=None, description="Username of the new user")
    isAdmin: Optional[bool] = Field(default=False, description="Is the user an admin?")

class BodyBalance(BaseModel):
    chat_id: TGChatID = Field(description="ID of the user")
    username: Optional[str] = Field(default=None, description="Username of the user")
    network: str = Field(description="The network where the deposit/debit occurred")
    amount: str = Field(description="The number of coins that have been replenished/debited")

class BodyInfo(BaseModel):
    message: TGMessage = Field(description="Message with information")
    chatIds: Optional[List[TGChatID]] = Field(default=None, description="Send a message to an individual user")
    isAll: Optional[bool] = Field(default=False, description="Send a message to all users or just one")

    def __init__(self, **kwargs):
        super(BodyInfo, self).__init__(**kwargs)
        if self.chatIds is not None and self.isAll is not None:
            self.isAll = False
        if self.chatIds is None and self.isAll is None:
            self.isAll = True
        if self.chatIds is not None and \
                (isinstance(self.chatIds, str) and self.chatIds.isdigit()) or isinstance(self.chatIds, int):
            self.chatIds = [self.chatIds]

# <<< Response >>>

class ResponseUserMethod(BaseModel):
    message: bool

# <<<=================================>>> Checker endpoint <<<=======================================================>>>

# <<< Body >>>

class BodyNews(BaseModel):
    message: TGMessage = Field(description="Message with bad information")

# <<< Response >>>

class ResponseCheckerMethod(BaseModel):
    message: bool

# <<<=================================>>> Transaction endpoint <<<===================================================>>>

# <<< Body >>>

class BodyTransaction(BaseModel):
    chatId: int = Field(description="ID of the user")
    transactionHash: str = Field(description="Transaction hash")
    fromAddress: str = Field(description="Sender's wallet address")
    toAddress: str = Field(description="Recipient's wallet address")
    amount: str = Field(description="Amount")
    network: str = Field(description="The network and the token '{network}-{token}' in which the transaction occurred.")

# <<< Response >>>

class ResponseTransactionMethod(BaseModel):
    message: bool