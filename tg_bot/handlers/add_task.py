from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards.inline import cancel_keyboard, get_type_task_keyboard, adding_task_callback, get_notify_keyboard
from tg_bot.misc.formatters import get_scheduler_id
from tg_bot.misc.insert_db import insert_task


async def run_add_task(message: types.Message, state: FSMContext):
    markup = await get_type_task_keyboard()
    await state.set_state("run_add_task")
    await message.answer("Выберете тип задачи", reply_markup=markup)


async def get_text_task(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()

    markup = await cancel_keyboard(cancel=True)

    await state.set_state("add_text")
    async with state.proxy() as data:
        data["type_task"] = callback_data.get("type_task")

    await call.message.answer("Введите текст задачи", reply_markup=markup)


async def add_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    markup = await get_notify_keyboard()
    scheduler_id = await get_scheduler_id()

    await insert_task(
        scheduler_id=scheduler_id,
        text=message.text,
        user_id=message.from_user.id,
        type_task=data.get('type_task')
    )

    await state.set_state("add_notify")
    async with state.proxy() as data:
        data["scheduler_id"] = scheduler_id
    await message.answer("Включить уведомления?", reply_markup=markup)


def register_add_task_handler(dp: Dispatcher):
    dp.register_message_handler(run_add_task, text="Добавить задачу")
    dp.register_callback_query_handler(
        get_text_task, adding_task_callback.filter(task="task"), state="run_add_task")
    dp.register_message_handler(add_task, state="add_text")
