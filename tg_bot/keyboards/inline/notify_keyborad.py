from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbackdatas import notify_callback


async def get_notify_markup():
    markup = InlineKeyboardMarkup()

    btns = (
        InlineKeyboardButton(text="Да", callback_data=notify_callback.new(add="yes")),
        InlineKeyboardButton(text="Нет", callback_data=notify_callback.new(add="no")),
    )

    for btn in btns:
        markup.insert(btn)

    return markup
