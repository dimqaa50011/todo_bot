from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.schema import Table

from core import bot_loader
from db_api.models.users import Users

from .base_crud import BaseCRUD


class UsersCRUD(BaseCRUD):
    _model: Table = Users.__table__

    async def create_item(
        self,
        _id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_admin: bool = False,
        deleted: bool = False,
    ):
        query = self._model.insert()
        values = {
            "id": _id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "joined_date": datetime.now(),
            "is_admin": is_admin,
            "deleted": deleted,
        }
        try:
            await self.executer(query=query, values=values)
        except IntegrityError as ex:
            logger.info(ex)

    async def get_item(self, _id: int):
        query = select(self._model).where(self._model.c.id == _id)
        answer: CursorResult = await self.executer(query=query)

        return answer.fetchone()

    async def get_all_items(self, _id: int):
        if _id in await bot_loader.get_admins():
            query = select(self._model).where(self._model.c.deleted == False)
            answer: CursorResult = await self.executer(query=query)

            return answer.fetchall()

        return None

    async def delete_item(self, _id: int):
        answer: CursorResult = await self.executer(
            query=self._model.update().where(self._model.c.id == _id), values={"deleted": True}
        )

        return answer

    async def update_item(self):
        pass
