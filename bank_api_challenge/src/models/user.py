import sqlalchemy as sa
from src.database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String, unique=True, nullable=False),
    sa.Column("email", sa.String, unique=True, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("person_id", sa.ForeignKey("people.id"), nullable=False),
    sa.Column("created_at", sa.DateTime, default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, onupdate=sa.func.now())
)
