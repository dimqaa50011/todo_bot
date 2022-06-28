from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.inline import adding_task_calllback


async def get_type_task_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    btns = (
        InlineKeyboardButton(text="Одноразовая",
                             callback_data=adding_task_calllback.new(type_task="once", task="task")),
        InlineKeyboardButton(
            text="Постоянная", callback_data=adding_task_calllback.new(type_task="const", task="task"))
    )

    for btn in btns:
        markup.insert(btn)

    return markup
