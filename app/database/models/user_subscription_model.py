from sqlalchemy import Table, Column, ForeignKey
from . import Base


user_subscriptions = Table(
    "user_subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("publication_id", ForeignKey("publications.id"), primary_key=True)
)
