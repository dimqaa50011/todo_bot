from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db_api.crud.tasks_crud import TasksCRUD

from .callbackdatas import paginator_call, tasks_list_call

crud = TasksCRUD()


async def get_task_list_markup(*, user_id: int, offset: Optional[int]):
    markup = InlineKeyboardMarkup(row_width=1)

    if not offset is None:
        if offset < 0:
            raise IndexError(f"Offset can`t be less than zero, offset={offset}")

    all_user_tasks, count_task = await crud.get_all_items(user_id=user_id, offset=offset, get_count=True)

    if not len(all_user_tasks):
        raise IndexError(f"Offset can`t be more then count_task, offset={offset} count_task={count_task}")

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

    button_next = InlineKeyboardButton(
        text="Далее >>", callback_data=paginator_call.new(next="yes", offset=offset, pager="pager")
    )
    button_previous = InlineKeyboardButton(
        text="<< Назад", callback_data=paginator_call.new(next="no", offset=offset, pager="pager")
    )

    return (button_previous, button_next)
