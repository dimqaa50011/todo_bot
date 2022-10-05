from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from tg_bot.keyboards.inline.callbackdatas import paginator_call
from tg_bot.keyboards.inline.tasks_list_keyboard import get_task_list_markup


async def get_my_tasks(message: Message, state: FSMContext):
    markup = await get_task_list_markup(user_id=message.from_user.id, offset=None)

    await state.set_state("tasks_list")
    await message.answer("Активные задачи", reply_markup=markup)


async def next_or_previous_task_list(call: CallbackQuery, callback_data: dict):
    await call.answer()

    offset = int(callback_data.get("offset"))
    offset = offset + 10 if callback_data.get("next") == "yes" else offset - 10

    try:
        markup = await get_task_list_markup(user_id=call.message.chat.id, offset=offset)
    except IndexError as ex:
        logger.warning(ex)
        return

    await call.message.edit_reply_markup(markup)


def register_tasks_list_handlers(dp: Dispatcher):
    dp.register_message_handler(get_my_tasks, Text("Мои задачи"))
    dp.register_callback_query_handler(
        next_or_previous_task_list, paginator_call.filter(pager="pager"), state="tasks_list"
    )
