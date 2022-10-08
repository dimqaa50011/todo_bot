from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from core import bot_loader
from db_api.crud.tasks_crud import TasksCRUD
from db_api.crud.users_crud import UsersCRUD
from db_api.schemas.scheduler_schemas import SchrdulerSchema
from db_api.schemas.tasks_chemas import TaskDetail
from db_api.schemas.users_schemas import UserItem


class SetNotify:
    DEFAULT_TIMEZONE = "Europe/Moscow"
    crud_user = UsersCRUD()
    crud_task = TasksCRUD()

    @classmethod
    async def set_notice(cls, scheduler_data: SchrdulerSchema):
        time_zone = await cls._get_timezone(user_id=scheduler_data.user_id)
        scheduler: AsyncIOScheduler = await bot_loader.get_scheduler()
        scheduler.add_job(
            cls._remind_you_of_a_task,
            DateTrigger(run_date=scheduler_data.dedline, timezone=time_zone),
            id=str(scheduler_data.task_id),
            args=(scheduler_data.task_id, scheduler_data.user_id),
        )

    @classmethod
    async def _get_timezone(cls, user_id: int):
        user: UserItem = await cls.crud_user.get_item(_id=user_id)

        if user.time_zone is None:
            return cls.DEFAULT_TIMEZONE
        return user.time_zone

    @classmethod
    async def _remind_you_of_a_task(cls, task_id: int, user_id: int):
        crud = TasksCRUD()
        task_user: TaskDetail = await crud.get_item(_id=task_id)
        bot: Bot = await bot_loader.get_bot_instance()

        msg = ("Напоминание о задаче\n", task_user.body)

        await bot.send_message(chat_id=user_id, text="\n".join(msg))
