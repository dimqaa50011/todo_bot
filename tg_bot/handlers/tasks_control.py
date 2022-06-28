from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards.inline import get_tasks_markup, tasks_list_callback, get_edit_keyboard, edit_callback
from tg_bot.misc.insert_db import update_task


async def get_tasks(message: types.Message):
    markup = await get_tasks_markup(message.from_user.id)
    await message.answer("Активные задачи", reply_markup=markup)


async def task_info(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    await state.set_state("task_info")
    async with state.proxy() as data:
        data["task_id"] = callback_data.get("task_id")
        data["text"] = callback_data.get("text")

    markup = await get_edit_keyboard()
    await call.message.answer(callback_data.get('text'), reply_markup=markup)


async def performed_task(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()

    task_id = data.get("task_id")
    await update_task(task_id=task_id, value=True, status=True)
    await state.finish()
    await call.message.answer("Задача выполнена! Поздравляю!")


async def get_new_text_task(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state("edit_text")
    await call.message.answer("Введите новый текст задачи")


async def edit_text_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")
    await update_task(task_id=task_id, value=message.text)

    await state.finish()
    await message.answer("Задача обновлена")


def register_control_tasks_handlers(dp: Dispatcher):
    dp.register_message_handler(get_tasks, text="Мои задачи")
    dp.register_callback_query_handler(task_info, tasks_list_callback.filter(my_task="task"))
    dp.register_callback_query_handler(performed_task, edit_callback.filter(field="status"), state="task_info")
    dp.register_callback_query_handler(get_new_text_task, edit_callback.filter(field="text"), state="task_info")
    dp.register_message_handler(edit_text_task, state="edit_text")
