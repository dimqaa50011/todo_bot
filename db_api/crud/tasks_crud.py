from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.engine.cursor import CursorResult

from db_api.models.tasks import Tasks

from .base_crud import BaseCRUD


class TasksCRUD(BaseCRUD):
    _model = Tasks.__table__

    async def create_item(self, user_id: int, body: str, dedline: Optional[datetime] = None):
        query = self._model.insert()
        values = {"body": body, "dedline": dedline, "user_id": user_id}

        answer: CursorResult = await self.executer(query=query, values=values)
        return answer.inserted_primary_key[0]

    async def get_item(self, _id: int):
        query = select(self._model).where(self._model.c.id == _id)
        answer: CursorResult = await self.executer(query=query, values=None)
        return answer.fetchone()

    async def get_all_items(self, user_id: int):
        query = select(self._model).where(and_(self._model.c.user_id == user_id, self._model.c.deleted == False))
        answer: CursorResult = await self.executer(query=query)

        return answer.fetchall()

    async def delete_item(self, _id: int):
        await self.executer(query=self._model.update().where(self._model.c.id == _id), values={"deleted": True})

    async def update_item(self, _id: int, update_dict: dict):
        await self.executer(query=self._model.update().where(self._model.c.id == _id), values=update_dict)
