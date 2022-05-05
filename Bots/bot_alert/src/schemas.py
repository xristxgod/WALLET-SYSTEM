from typing import Optional, List

from pydantic import BaseModel, Field

# <<<=================================>>> User endpoint <<<==========================================================>>>

# <<< Body >>>

class BodyRegUser(BaseModel):
    chat_id: int = Field(description="ID of the new user")
    username: Optional[str] = Field(default=None, description="Username of the new user")
    is_admin: Optional[bool] = Field(default=False, description="Is the user an admin?")

class BodyBalance(BaseModel):
    chat_id: int = Field(description="ID of the user")
    username: Optional[str] = Field(default=None, description="Username of the user")
    network: str = Field(description="The network where the deposit/debit occurred")
    amount: str = Field(description="The number of coins that have been replenished/debited")

class BodyInfo(BaseModel):
    message: str = Field(description="Message with information")
    chat_ids: Optional[List[int]] = Field(default=None, description="Send a message to an individual user")
    is_all: Optional[bool] = Field(default=False, description="Send a message to all users or just one")

    def __init__(self, **kwargs):
        super(BodyInfo, self).__init__(**kwargs)
        if self.chat_ids is not None and self.is_all is not None:
            self.is_all = False
        if self.chat_ids is None and self.is_all is None:
            self.is_all = True
        if self.chat_ids is not None and \
                (isinstance(self.chat_ids, str) and self.chat_ids.isdigit()) or isinstance(self.chat_ids, int):
            self.chat_ids = [self.chat_ids]

# <<< Response >>>

class ResponseUserMethod(BaseModel):
    message: bool

