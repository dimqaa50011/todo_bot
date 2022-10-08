from datetime import datetime

from pydantic import BaseModel, Field


class BaseUserItem(BaseModel):
    id: int = Field(...)


class UserItem(BaseModel):
    username: str = Field(default=None)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    joined_date: datetime = Field(default=datetime.now())
    is_admin: bool = Field(default=False)
    time_zone: str = Field(default=None)


class CreateUser(BaseUserItem, UserItem):
    deleted: bool = Field(default=False)
