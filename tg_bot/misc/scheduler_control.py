from loader import LoaderCoreBot
from tg_bot.misc.getters_data_db import get_my_task


async def send_message(task_id: int, user_id: int):
    task = await get_my_task(fetch=True, id=task_id)
    bot = await LoaderCoreBot.load_bot()

    await bot.send_message(user_id, task.get("todo_text"))
