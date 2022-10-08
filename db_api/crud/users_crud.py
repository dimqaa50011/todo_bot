from loguru import logger
from sqlalchemy import select
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.schema import Table

from core import bot_loader
from db_api.models.users import Users
from db_api.schemas.users_schemas import CreateUser, UserItem

from .base_crud import BaseCRUD


class UsersCRUD(BaseCRUD):
    _model: Table = Users.__table__

    async def create_item(self, fields: CreateUser):
        query = self._model.insert()

        try:
            await self.executer(query=query, values=fields.dict())
        except IntegrityError as ex:
            logger.info(ex)

    async def get_item(self, _id: int):
        query = select(self._model).where(self._model.c.id == _id)
        answer: CursorResult = await self.executer(query=query)
        result = answer.fetchone()

        return UserItem(
            username=result.username,
            first_name=result.first_name,
            last_name=result.last_name,
            is_admin=result.is_admin,
            time_zone=result.time_zone,
        )

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

    async def update_item(self, user_id: int, update_dict: dict):
        query = self._model.update().where(self._model.c.id == user_id)
        await self.executer(query=query, values=update_dict)
