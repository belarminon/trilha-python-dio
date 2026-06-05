from pydantic import AwareDatetime, BaseModel, NativeDatetime, PositiveFloat


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: PositiveFloat
    timestamp: NativeDatetime | AwareDatetime