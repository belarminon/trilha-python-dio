from datetime import datetime
from pydantic import BaseModel, EmailStr
from src.models.person import PersonType, PersonDocument

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    classification: PersonType
    document: str
    document_type: PersonDocument

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    classification: PersonType | None = None

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
