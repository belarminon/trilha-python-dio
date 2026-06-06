import sqlalchemy as sa
from enum import Enum
from src.database import metadata

class PersonType(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

people = sa.Table(
    "people",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("email", sa.String, unique=True, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("classification", sa.Enum(PersonType, name="person_type"), nullable=False),
    sa.Column("created_at", sa.DateTime, default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, onupdate=sa.func.now())
)