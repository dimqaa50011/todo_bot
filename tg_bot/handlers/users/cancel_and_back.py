from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from tg_bot.keyboards.inline.callbackdatas import cancel_call


async def cancel_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Отменено!", show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()


def register_cancel_and_back_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_handler, cancel_call.filter(action="cancel"), state="*")
