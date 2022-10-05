from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db_api.crud.tasks_crud import TasksCRUD

from .callbackdatas import paginator_call, tasks_list_call

crud = TasksCRUD()


async def get_task_list_markup(*, user_id: int, offset: Optional[int]):
    all_user_tasks, count_task = await crud.get_all_items(user_id=user_id, offset=offset, get_count=True)

    markup = InlineKeyboardMarkup(row_width=1)

    async for task in one_task(all_user_tasks):
        markup.insert(InlineKeyboardButton(text=task.body, callback_data=tasks_list_call.new(task_id=task.id)))

    if count_task > 10:
        pager = await next_and_previous(offset)
        for btn in pager:
            markup.insert(btn)

    return markup


async def one_task(all_tasks):
    for task in all_tasks:
        yield task


async def next_and_previous(offset: Optional[int]):
    if offset is None:
        offset = 0

    button_next = InlineKeyboardButton(text="Далее >>", callback_data=paginator_call.new(next=1, offset=offset))
    button_previous = InlineKeyboardButton(text="<< Назад", callback_data=paginator_call.new(next=-1, offset=offset))

    return (button_previous, button_next)
