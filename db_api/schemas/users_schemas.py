from datetime import datetime

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    id: int = Field(...)
    username: str = Field(default=None)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    joined_date: datetime = Field(default=datetime.now())
    is_admin: bool = Field(default=False)
    deleted: bool = Field(default=False)
    time_zone: str = Field(default=None)
