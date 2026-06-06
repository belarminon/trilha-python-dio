from pydantic import BaseModel, NonNegativeFloat

class AccountIn(BaseModel):
    user_id: int
    balance: NonNegativeFloat