from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.tasks_chemas import TaskCallback, TaskDetail

from .callbackdatas import paginator_call

crud = TasksCRUD()
task_call = CallbackData("tasks", "level", "user_id", "task_id", "offset", "field", "action")


async def list_tasks(*, user_id: int, offset: int | str = 0):
    offset = 0 if isinstance(offset, str) and offset == "0" else offset

    CURRENT_LEVEL = 0
    all_user_tasks, count_task = await crud.get_all_items(user_id=user_id, offset=offset, get_count=True)

    markup = InlineKeyboardMarkup(row_width=1)

    async for task in one_task(all_user_tasks):
        task: TaskDetail
        callback_data = await make_task_callback_data(
            TaskCallback(level=CURRENT_LEVEL + 1, user_id=user_id, task_id=task.id, offset=offset)
        )
        markup.insert(InlineKeyboardButton(text=task.body, callback_data=callback_data))

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


async def task_detail(task_id: int, user_id: int):
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()

    complited_callback = await make_task_callback_data(
        TaskCallback(level=CURRENT_LEVEL + 1, task_id=task_id, user_id=user_id, field="complited")
    )
    body_task_callback = await make_task_callback_data(
        TaskCallback(level=CURRENT_LEVEL + 1, task_id=task_id, user_id=user_id, field="body")
    )
    dedline_task_callback = await make_task_callback_data(
        TaskCallback(level=CURRENT_LEVEL + 1, task_id=task_id, user_id=user_id, field="dedline")
    )

    back_callback = await make_task_callback_data(
        TaskCallback(
            level=CURRENT_LEVEL - 1,
            user_id=user_id,
        )
    )

    markup.row(
        InlineKeyboardButton(text="Выполнено", callback_data=complited_callback),
        InlineKeyboardButton(text="Изменить текст", callback_data=body_task_callback),
    )
    markup.row(
        InlineKeyboardButton(text="Изменить дедлайн", callback_data=dedline_task_callback),
        InlineKeyboardButton(text="Назад", callback_data=back_callback),
    )

    return markup


async def get_back_markup(task_id: int, user_id: int, button_text: str | None = None):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    back_callback = await make_task_callback_data(
        TaskCallback(level=CURRENT_LEVEL - 1, user_id=user_id, task_id=task_id)
    )

    text = "Назад"
    if not button_text is None and isinstance(button_text, str):
        text = button_text

    markup.row(InlineKeyboardButton(text=text, callback_data=back_callback))

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


async def make_task_callback_data(task_callback: TaskCallback):
    return task_call.new(
        level=task_callback.level,
        user_id=task_callback.user_id,
        task_id=task_callback.task_id,
        offset=task_callback.offset,
        field=task_callback.field,
        action=task_callback.action,
    )
