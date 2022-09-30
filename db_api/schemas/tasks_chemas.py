from datetime import datetime

from pydantic import BaseModel, Field


class BaseTaskSchema(BaseModel):
    body: str = Field(...)


class CreateTask(BaseTaskSchema):
    dedline: datetime = Field(default=None)
    complited: bool = Field(default=False)
    deleted: bool = Field(default=False)
    user_id: int = Field(...)


class TaskDetail(BaseTaskSchema):
    id: int = Field(...)
    dedline: datetime = Field(default=None)


class TaskList(BaseTaskSchema):
    items: list[TaskDetail]
