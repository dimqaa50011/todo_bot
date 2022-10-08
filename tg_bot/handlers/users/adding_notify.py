from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from db_api.crud.tasks_crud import TasksCRUD
from db_api.crud.users_crud import UsersCRUD
from db_api.schemas.scheduler_schemas import SchrdulerSchema
from tg_bot.dependecies.formatters import CustomFormatters
from tg_bot.dependecies.scheduler import SetNotify, create_notify_setter
from tg_bot.keyboards.inline.callbackdatas import notify_callback

task_crud = TasksCRUD()
user_crud = UsersCRUD()


async def without_notice(call: CallbackQuery, state: FSMContext):
    await call.answer("Уведомления отключены", show_alert=True)
    await state.finish()
    await call.message.edit_reply_markup()


async def notification_adding_process(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(text="Напиши дату и время для уведомления в формате дд.мм чч:мм")
    await state.set_state("add_date_time")


async def add_dedline(message: Message, state: FSMContext):
    notify_setter: SetNotify = await create_notify_setter()
    data = await state.get_data()

    try:
        dedline = await CustomFormatters.dedline_format(message.text)
    except ValueError as ex:
        logger.warning(ex)
        await message.answer("Неверный формат даты или времени. Попробуй снова.")
        return

    await task_crud.update_item(_id=data.get("task_id"), update_dict={"dedline": dedline})

    await notify_setter.set_notice(
        SchrdulerSchema(task_id=data.get("task_id"), user_id=message.from_user.id, dedline=dedline)
    )
    # await SetNotify.set_notice(
    #     SchrdulerSchema(task_id=data.get("task_id"), user_id=message.from_user.id, dedline=dedline)
    # )

    await message.answer("Уведомления включены")
    await state.finish()


def register_adding_notify_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(without_notice, notify_callback.filter(add="no"), state="add_notify")
    dp.register_callback_query_handler(
        notification_adding_process, notify_callback.filter(add="yes"), state="add_notify"
    )
    dp.register_message_handler(add_dedline, state="add_date_time")
