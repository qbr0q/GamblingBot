from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    telegram_id: int
    username: str = Field(nullable=True)
    balance: int = Field(nullable=True, default=10000)
