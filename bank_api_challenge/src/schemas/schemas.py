from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TransactionCreate(BaseModel):
    type: str  # deposit / withdraw
    amount: float


class TransactionResponse(BaseModel):
    type: str
    amount: float

    class Config:
        from_attributes = True