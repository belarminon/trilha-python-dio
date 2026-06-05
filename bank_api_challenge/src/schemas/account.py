from pydantic import BaseModel, PositiveFloat

class AccountInfo(BaseModel):
    user_id: int
    balance: PositiveFloat