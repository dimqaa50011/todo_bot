from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbackdatas import edit_task_call


async def get_edit_markup():
    markup = InlineKeyboardMarkup()

    markup.insert(
        InlineKeyboardButton(
            text="Редактировать", callback_data=edit_task_call.new(edit_task="edit_task", attr="empty")
        )
    )
    markup.insert(
        InlineKeyboardButton(text="Выполена", callback_data=edit_task_call.new(edit_task="edit_task", attr="complited"))
    )

    return markup
