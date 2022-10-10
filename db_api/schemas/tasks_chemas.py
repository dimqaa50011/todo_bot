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


class BaseTaskCallback(BaseModel):
    task_id: str = Field(default="0")
    user_id: str = Field(default="0")
    offset: str = Field(default="0")
    field: str = Field(default="0")
    action: str = Field(default="0")


class TaskCallback(BaseTaskCallback):
    level: str
