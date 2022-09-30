from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db_api.session import async_session


class BaseCRUD(ABC):
    _model = None

    @abstractmethod
    async def create_item(self):
        pass

    @abstractmethod
    async def get_item(self):
        pass

    @abstractmethod
    async def get_all_items(self):
        pass

    @abstractmethod
    async def update_item(self):
        pass

    @abstractmethod
    async def delete_item(self):
        pass

    async def executer(self, query, values: Optional[dict] = None):
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(statement=query, params=values)
                await session.commit()
        return result
