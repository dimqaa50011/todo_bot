from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbackdatas import edit_task_call
from .cancel_and_back_keyboards import get_cancel_button


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


async def get_body_and_dedline_markup():
    markup = InlineKeyboardMarkup()
    cancel = await get_cancel_button()

    markup.row(
        InlineKeyboardButton(text="Текст задачи", callback_data=edit_task_call.new(edit_task="edit_task", attr="body")),
        InlineKeyboardButton(text="Дедлайн", callback_data=edit_task_call.new(edit_task="edit_task", attr="dedline")),
    )
    markup.row(cancel)

    return markup
