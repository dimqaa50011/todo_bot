from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from db_api.crud.tasks_crud import TasksCRUD
from tg_bot.keyboards.inline.callbackdatas import notify_callback

crud = TasksCRUD()


async def without_notice(call: CallbackQuery, state: FSMContext):
    await call.answer("Уведомления отключены", show_alert=True)
    await state.finish()
    await call.message.edit_reply_markup()


async def notification_adding_process(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(text="Напиши дату и время для уведомления в формате dd.mm HH:MM")
    await state.set_state("add_date_time")


async def add_dedline(message: Message, state: FSMContext):
    data = await state.get_data()
    dedline = await dedline_format(message.text)
    await crud.update_item(_id=data.get("task_id"), update_dict={"dedline": dedline})
    await message.answer("Уведомления включены")
    await state.finish()


async def dedline_format(text: str):
    dedline_date, dedline_time = text.strip().split(" ")
    dedline_date = dedline_date.replace(",", ".")
    dedline_time = dedline_time.replace(".", ":").replace(",", ":")

    dedline = datetime.strptime(f"{dedline_date}.{datetime.now().year} {dedline_time}", "%d.%m.%Y %H:%M")
    return dedline


def register_adding_notify_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(without_notice, notify_callback.filter(add="no"), state="add_notify")
    dp.register_callback_query_handler(
        notification_adding_process, notify_callback.filter(add="yes"), state="add_notify"
    )
    dp.register_message_handler(add_dedline, state="add_date_time")
