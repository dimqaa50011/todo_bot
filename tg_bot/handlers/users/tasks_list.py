from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from tg_bot.keyboards.inline.tasks_list_keyboard import get_task_list_markup


async def get_my_tasks(message: Message, state: FSMContext):
    markup = await get_task_list_markup(user_id=message.from_user.id, offset=None)

    # await state.set_state("tasks_list")
    await message.answer("Активные задачи", reply_markup=markup)


def register_tasks_list_handlers(dp: Dispatcher):
    dp.register_message_handler(get_my_tasks, Text("Мои задачи"))
