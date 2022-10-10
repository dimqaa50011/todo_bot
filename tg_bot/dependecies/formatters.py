from datetime import datetime

from loguru import logger

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import TaskDetail


class CustomFormatters:
    crud_task = TasksCRUD()

    @staticmethod
    async def dedline_format(text: str):
        logger.debug(text)
        dedline_date, dedline_time = text.strip().split(" ")
        dedline_date = dedline_date.replace(",", ".").replace("/", ".")
        dedline_time = dedline_time.replace(".", ":").replace(",", ":")

        dedline = datetime.strptime(f"{dedline_date}.{datetime.now().year} {dedline_time}", "%d.%m.%Y %H:%M")
        return dedline

    @classmethod
    async def get_card_task(cls, task_id: int):
        task: TaskDetail = await cls.crud_task.get_item(_id=task_id)

        dedline = "Не назначен" if task.dedline is None else await cls._custom_date_format(task.dedline)

        return f"Дедлайн: {dedline}\n\nЗадача:\n{task.body}"

    @staticmethod
    async def _custom_date_format(dedline: datetime):
        return dedline.strftime("%A %d %b %H:%M")
