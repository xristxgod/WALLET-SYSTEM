from typing import Optional

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


# <<< Response >>>

class ResponseUserMethod(BaseModel):
    message: bool

