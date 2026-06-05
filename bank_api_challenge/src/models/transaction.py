import sqlalchemy as sa

from enum import Enum
from src.database import metadata


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    
    
transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("type", sa.Enum(TransactionType, name="transaction_type"), nullable=False),
    sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column("timestamp", sa.TIMESTAMP(timezone=True), default=sa.func.now())
)