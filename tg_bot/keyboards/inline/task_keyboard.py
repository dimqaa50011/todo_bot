from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline import adding_task_callback, tasks_list_callback, edit_callback, get_cancel
from tg_bot.keyboards.inline.callbakbatas import notify_callback
from tg_bot.misc.getters_data_db import get_my_task


async def get_type_task_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    btns = (
        InlineKeyboardButton(text="Одноразовая",
                             callback_data=adding_task_callback.new(type_task="once", task="task")),
        InlineKeyboardButton(
            text="Постоянная", callback_data=adding_task_callback.new(type_task="const", task="task"))
    )

    for btn in btns:
        markup.insert(btn)

    return markup


async def get_tasks_markup(user_id: int):
    markup = InlineKeyboardMarkup()

    data = await get_my_task(fetchall=True, user_id=user_id, status=False)
    for item in data:
        print(f"[SCHEDULER_ID] {item.get('scheduler_id').decode('utf-8')}")
        markup.insert(
            InlineKeyboardButton(text=item.get("todo_text"),
                                 callback_data=tasks_list_callback.new(task_id=item.get("id"),
                                                                       text=item.get("todo_text"),
                                                                       scheduler_id=item.get('scheduler_id').decode(
                                                                           'utf-8'),
                                                                       my_task="task")))

    return markup


async def get_edit_keyboard():
    markup = InlineKeyboardMarkup()
    cancel = await get_cancel()

    btns = (
        InlineKeyboardButton(text="Выполнено", callback_data=edit_callback.new(field="status")),
        InlineKeyboardButton(text="Редактировать", callback_data=edit_callback.new(field="text")),
        cancel
    )

    for btn in btns:
        markup.insert(btn)

    return markup


async def get_notify_keyboard():
    markup = InlineKeyboardMarkup()
    btns = (
        InlineKeyboardButton(text="Включить", callback_data=notify_callback.new(ans="yes")),
        InlineKeyboardButton(text="Не включать", callback_data=notify_callback.new(ans="no"))
    )

    for btn in btns:
        markup.insert(btn)

    return markup
