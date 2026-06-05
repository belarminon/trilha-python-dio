from pydantic import BaseModel, AwareDatetime, NativeDatetime, PositiveFloat


class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: NativeDatetime | AwareDatetime


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    timestamp: NativeDatetime | AwareDatetime
