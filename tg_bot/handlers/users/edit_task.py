from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import TaskDetail
from tg_bot.keyboards.inline.callbackdatas import edit_task_call, tasks_list_call
from tg_bot.keyboards.inline.edit_task_keyboard import get_edit_markup

crud = TasksCRUD()


async def get_task_detail(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=60)
    task_id = int(callback_data.get("task_id"))

    markup = await get_edit_markup()

    async with state.proxy() as data:
        data["task_id"] = task_id

    await state.set_state("edit_task")

    card = await get_card_task(task_id)

    await call.message.edit_text(card)
    await call.message.edit_reply_markup(markup)


async def task_compliteb(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Задача выполнена!\nПоздравляю!", show_alert=True)

    data = await state.get_data()

    await crud.update_item(_id=data.get("task_id"), update_dict={"complited": True})
    await call.message.edit_reply_markup()
    await state.finish()


async def get_card_task(task_id: int):
    task: TaskDetail = await crud.get_item(_id=task_id)

    if task.dedline is None:
        dedline = "Не назначен"

    dedline = task.dedline

    return f"Дедлайн: {dedline}\n\nЗадача:\n{task.body}"


def register_edit_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_task_detail, tasks_list_call.filter(task="task"), state="tasks_list")
    dp.register_callback_query_handler(task_compliteb, edit_task_call.filter(attr="complited"), state="edit_task")
