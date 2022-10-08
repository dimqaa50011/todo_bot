from aiogram import Bot
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from core import bot_loader
from db_api.crud.tasks_crud import TasksCRUD
from db_api.crud.users_crud import UsersCRUD
from db_api.schemas.scheduler_schemas import SchrdulerSchema
from db_api.schemas.tasks_chemas import TaskDetail
from db_api.schemas.users_schemas import UserItem


class SetNotify:
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.DEFAULT_TIMEZONE = "Europe/Moscow"
        self.crud_user = UsersCRUD()
        self.crud_task = TasksCRUD()
        self.scheduler = scheduler

    async def set_notice(self, scheduler_data: SchrdulerSchema):
        time_zone = await self._get_timezone(user_id=scheduler_data.user_id)

        self.scheduler.add_job(
            self._remind_you_of_a_task,
            DateTrigger(run_date=scheduler_data.dedline, timezone=time_zone),
            id=str(scheduler_data.task_id),
            args=(scheduler_data.task_id, scheduler_data.user_id),
        )

    async def edit_notify(self, scheduler_data: SchrdulerSchema):
        try:
            self.scheduler.remove_job(job_id=scheduler_data.task_id)
        except JobLookupError as ex:
            logger.warning(ex)
        finally:
            await self.set_notice(scheduler_data=scheduler_data)

    async def _get_timezone(self, user_id: int):
        user: UserItem = await self.crud_user.get_item(_id=user_id)

        if user.time_zone is None:
            return self.DEFAULT_TIMEZONE
        return user.time_zone

    @staticmethod
    async def _remind_you_of_a_task(task_id: int, user_id: int):
        crud = TasksCRUD()
        task_user: TaskDetail = await crud.get_item(_id=task_id)
        bot: Bot = await bot_loader.get_bot_instance()

        msg = ("Напоминание о задаче\n", task_user.body)

        await bot.send_message(chat_id=user_id, text="\n".join(msg))


async def create_notify_setter():
    scheduler: AsyncIOScheduler = await bot_loader.get_scheduler()
    return SetNotify(scheduler=scheduler)
