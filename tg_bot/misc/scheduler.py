from aiogram import Bot

from core import bot_loader
from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import TaskDetail


async def remind_you_of_a_task(task_id: int, user_id: int):
    crud = TasksCRUD()
    task_user: TaskDetail = await crud.get_item(_id=task_id)
    bot: Bot = await bot_loader.get_bot_instance()

    msg = ("Напоминание о задаче\n", task_user.body)

    await bot.send_message(chat_id=user_id, text="\n".join(msg))
