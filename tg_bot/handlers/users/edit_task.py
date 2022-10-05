from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import TaskDetail
from tg_bot.keyboards.inline.callbackdatas import tasks_list_call

crud = TasksCRUD()


async def get_task_detail(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=60)
    await state.set_state("edit_task")

    card = await get_card_task(int(callback_data.get("task_id")))

    await call.message.edit_text(card)


async def get_card_task(task_id: int):
    task: TaskDetail = await crud.get_item(_id=task_id)

    if task.dedline is None:
        dedline = "Не назначен"

    dedline = task.dedline

    return f"Дедлайн: {dedline}\n\nЗадача:\n{task.body}"


def register_edit_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_task_detail, tasks_list_call.filter(task="task"), state="tasks_list")
