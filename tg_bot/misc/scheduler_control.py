from datetime import date

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import LoaderCoreBot
from tg_bot.misc.getters_data_db import get_my_task


async def send_message(task_id: int, user_id: int):
    task = await get_my_task(fetch=True, id=task_id)
    bot = await LoaderCoreBot.load_bot()

    await bot.send_message(user_id, task.get("todo_text"))


async def add_once_notify(scheduler: AsyncIOScheduler, task_id: int, user_id: int, notify_id: str, date_notify: date):
    scheduler.add_job(send_message, trigger="date", run_date=date_notify, id=notify_id, args=(task_id, user_id))


async def add_scheduler(scheduler, task_id: int,
                        user_id: int,
                        notify_id: str,
                        trigger: str,
                        date_notify: date | None = None):

    if trigger == "date":
        await add_once_notify(scheduler, task_id, user_id, notify_id, date_notify)
