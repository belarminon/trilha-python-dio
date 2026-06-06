from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

from person import Person

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    useremail = Column(String, unique=True)
    password = Column(String)
    person_id = Column(Integer, ForeignKey("people.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    person = relationship("Person", back_populates="users")
