from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db_api.crud.tasks_crud import TasksCRUD

from .callbackdatas import paginator_call, tasks_list_call

crud = TasksCRUD()


async def get_task_list_markup(*, user_id: int, offset: Optional[int]):
    all_user_tasks, count_task = await crud.get_all_items(user_id=user_id, offset=offset, get_count=True)

    markup = InlineKeyboardMarkup(row_width=1)

    async for task in one_task(all_user_tasks):
        markup.insert(
            InlineKeyboardButton(text=task.body, callback_data=tasks_list_call.new(task_id=task.id, task="task"))
        )

    if count_task > 10:
        previous_btn, next_btn = await next_and_previous(offset)

        offset = 0 if offset is None else offset

        if offset <= 0:
            markup.row(next_btn)
        elif not len(all_user_tasks):
            markup.row(previous_btn)
        elif count_task - offset <= 10:
            markup.row(previous_btn)
        else:
            markup.row(previous_btn, next_btn)

    return markup


async def one_task(all_tasks):
    for task in all_tasks:
        yield task


async def next_and_previous(offset: Optional[int]):
    if offset is None:
        offset = 0

    return (
        InlineKeyboardButton(
            text="<< Назад", callback_data=paginator_call.new(next="no", offset=offset, pager="pager")
        ),
        InlineKeyboardButton(
            text="Далее >>", callback_data=paginator_call.new(next="yes", offset=offset, pager="pager")
        ),
    )
