from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbackdatas import cancel_call


async def get_cancel_markup(*, cancel: bool = False, back: bool = False):
    markup = InlineKeyboardMarkup(row_width=2)

    if cancel:
        cancel_button = await get_cancel_button()
        markup.insert(cancel_button)

    if back:
        back_button = await get_back_button()
        markup.insert(back_button)

    return markup


async def get_cancel_button():
    return InlineKeyboardButton(text="Отмена", callback_data=cancel_call.new(action="cancel"))


async def get_back_button():
    return InlineKeyboardButton(text="Назад", callback_data=cancel_call.new(action="back"))
