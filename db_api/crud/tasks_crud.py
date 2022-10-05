from typing import Optional

from sqlalchemy import and_, select, text
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.selectable import Select

from db_api.models.tasks import Tasks
from db_api.schemas.tasks_chemas import CreateTask, TaskDetail

from .base_crud import BaseCRUD


class TasksCRUD(BaseCRUD):
    _model = Tasks.__table__

    async def create_item(self, fields: CreateTask):
        query = self._model.insert()

        answer: CursorResult = await self.executer(query=query, values=fields.dict())
        return answer.inserted_primary_key[0]

    async def get_item(self, _id: int):
        query = select(self._model).where(self._model.c.id == _id)
        answer: CursorResult = await self.executer(query=query, values=None)
        result = answer.fetchone()
        return TaskDetail(id=result.id, body=result.body, dedline=result.dedline)

    async def get_all_items(
        self, *, user_id: int, offset: Optional[int] = None, limit: int = 10, get_count: bool = False
    ):
        query: Select = (
            select(self._model)
            .where(and_(self._model.c.user_id == user_id, self._model.c.deleted == False))
            .limit(limit)
        )

        if not offset is None:
            query: Select = query.offset(offset)

        answer: CursorResult = await self.executer(query=query)

        tasks_list = await self.__create_tasks_list(answer.fetchall())

        if get_count:
            count_query = select(text("COUNT(user_id)")).where(self._model.c.user_id == user_id)
            result: CursorResult = await self.executer(query=count_query)

            return (tasks_list, result.scalar())

        return await self.__create_tasks_list(answer.fetchall())

    async def delete_item(self, _id: int):
        await self.executer(query=self._model.update().where(self._model.c.id == _id), values={"deleted": True})

    async def update_item(self, _id: int, update_dict: dict):
        await self.executer(query=self._model.update().where(self._model.c.id == _id), values=update_dict)

    async def __create_tasks_list(self, tasks: list):
        result = []
        async for task in self.__get_task_detail(tasks):
            result.append(TaskDetail(id=task.id, body=task.body, dedline=task.dedline))

        return tuple(result)

    async def __get_task_detail(self, tasks: list):
        for task in tasks:
            yield task
