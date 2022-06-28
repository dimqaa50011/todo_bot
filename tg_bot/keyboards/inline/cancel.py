from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg_bot.keyboards.inline import cancel_callback


async def get_cancel():
    return InlineKeyboardButton(text="Отмена", callback_data=cancel_callback.new(trigger="cancel"))


async def get_back():
    return InlineKeyboardButton(text="Назад", callback_data=cancel_callback.new(trigger="back"))


async def cancel_keyboard(cancel: bool = False, back: bool = False):
    markup = InlineKeyboardMarkup(row_width=2)

    if cancel:
        cancel_btn = await get_cancel()
        markup.insert(cancel_btn)
    if back:
        back_btn = await get_back()
        markup.insert(back_btn)

    return markup
