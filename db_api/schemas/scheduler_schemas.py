from datetime import datetime

from pydantic import BaseModel


class SchrdulerSchema(BaseModel):
    task_id: int
    user_id: int
    dedline: datetime
