from typing import Optional, List

from pydantic import BaseModel, Field
from src.types import TGMessage, TGChatID

# <<<=================================>>> User endpoint <<<==========================================================>>>

# <<< Body >>>

class BodyRegUser(BaseModel):
    chatID: TGChatID = Field(description="ID of the new user")
    username: Optional[str] = Field(default=None, description="Username of the new user")
    isAdmin: Optional[bool] = Field(default=False, description="Is the user an admin?")

class BodyBalance(BaseModel):
    chatID: TGChatID = Field(description="ID of the user")
    username: Optional[str] = Field(default=None, description="Username of the user")
    network: str = Field(description="The network where the deposit/debit occurred")
    amount: str = Field(description="The number of coins that have been replenished/debited")
    transactionHash: str = Field(description="Transaction hash")

class BodyInfo(BaseModel):
    message: TGMessage = Field(description="Message with information")
    chatIDs: Optional[List[TGChatID]] = Field(default=None, description="Send a message to an individual user")
    isAll: Optional[bool] = Field(default=False, description="Send a message to all users or just one")
    toMain: Optional[bool] = Field(default=False, description="Send a message to the main bot!")

    def __init__(self, **kwargs):
        super(BodyInfo, self).__init__(**kwargs)
        if self.chatIDs is not None and self.isAll is not None:
            self.isAll = False
        if self.chatIDs is None and self.isAll is None:
            self.isAll = True
        if self.chatIDs is not None and \
                (isinstance(self.chatIDs, str) and self.chatIDs.isdigit()) or isinstance(self.chatIDs, int):
            self.chatIDs = [self.chatIDs]

# <<< Response >>>

class ResponseUserMethod(BaseModel):
    message: bool

# <<<=================================>>> Checker endpoint <<<=======================================================>>>

# <<< Body >>>

class BodyNews(BaseModel):
    message: TGMessage = Field(description="Message with bad/good information")

class BodyInfoChecker(BaseModel):
    message: TGMessage = Field(description="Message with information")

# <<< Response >>>

class ResponseCheckerMethod(BaseModel):
    message: bool

# <<<=================================>>> Transaction endpoint <<<===================================================>>>

# <<< Body >>>

class BodyTransaction(BaseModel):
    chatID: int = Field(description="ID of the user")
    transactionHash: str = Field(description="Transaction hash")
    fromAddress: str = Field(description="Sender's wallet address")
    toAddress: str = Field(description="Recipient's wallet address")
    amount: str = Field(description="Amount")
    fee: str = Field(description="Fee")
    network: str = Field(description="The network and the token '{network}-{token}' in which the transaction occurred.")
    status: int = Field(description=(
        "There are 4 types of transaction statuses. 0 - created in api, "
        "1 - created in balancer, 2 - successfully sent, 3 - an error occurred."
    ), default=0)

    errorMessage: Optional[str] = Field(description="Serves only for the status with error 3.", default="")

# <<< Response >>>

class ResponseTransactionMethod(BaseModel):
    message: bool