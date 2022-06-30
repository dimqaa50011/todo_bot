from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tg_bot.keyboards.inline import notify_callback
from tg_bot.misc.formatters import format_date
from tg_bot.misc.scheduler_control import add_scheduler


async def add_notify(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data.get("type_task") == "once":
        await state.set_state("add_once_notify")
        await call.message.answer("Введите дату напоминания в формате дд.мм")


async def cancel_notify(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Уведомления отключены", show_alert=True)
    await state.finish()
    await call.message.edit_reply_markup()


async def register_scheduler(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()

    date = await format_date(message.text)
    await add_scheduler(scheduler, task_id=data.get('task_id'), trigger='date',
                        user_id=message.from_user.id,
                        notify_id=data.get("scheduler_id"),
                        date_notify=date)

    await state.finish()
    await message.answer("Уведомления настроены")


def register_notify(dp: Dispatcher):
    dp.register_callback_query_handler(add_notify, notify_callback.filter(ans="yes"), state="add_notify")
    dp.register_callback_query_handler(cancel_notify, notify_callback.filter(ans="no"), state="add_notify")
    dp.register_message_handler(register_scheduler, state="add_once_notify")
