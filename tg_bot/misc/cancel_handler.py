from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards.inline import cancel_callback


async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Отменено", show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()


def register_cancel(dp: Dispatcher):
    dp.register_callback_query_handler(cancel, cancel_callback.filter(trigger="cancel"), state="*")
