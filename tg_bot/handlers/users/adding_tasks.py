from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import CreateTask
from tg_bot.keyboards.inline.notify_keyborad import get_notify_markup

crud = TasksCRUD()


async def add_new_task(message: Message, state: FSMContext):
    print(message.location)
    await message.answer("Какую задачу нужно записать?")
    await state.set_state("new_task")


async def body_task(message: Message, state: FSMContext):
    markup = await get_notify_markup()
    task_id = await crud.create_item(CreateTask(body=message.text, user_id=message.from_user.id))
    await message.answer("Включить уведомления?", reply_markup=markup)

    await state.set_state("add_notify")

    async with state.proxy() as data:
        data["task_id"] = task_id


def register_adding_tasks_handlers(dp: Dispatcher):
    dp.register_message_handler(add_new_task, Text("Добавить задачу"))
    dp.register_message_handler(body_task, state="new_task")
