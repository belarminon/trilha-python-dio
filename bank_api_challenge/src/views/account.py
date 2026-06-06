from pydantic import BaseModel, AwareDatetime, NaiveDatetime


class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: NaiveDatetime | AwareDatetime


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    timestamp: NaiveDatetime | AwareDatetime
