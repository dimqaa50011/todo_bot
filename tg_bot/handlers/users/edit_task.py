from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from core import bot_loader
from db_api.crud.tasks_crud import TasksCRUD
from db_api.crud.users_crud import UsersCRUD
from db_api.schemas.tasks_chemas import TaskDetail
from tg_bot.keyboards.inline.callbackdatas import edit_task_call, tasks_list_call
from tg_bot.keyboards.inline.edit_task_keyboard import get_body_and_dedline_markup, get_edit_markup
from tg_bot.keyboards.reply.main_menu import get_main_menu
from tg_bot.misc.scheduler import remind_you_of_a_task

crud_task = TasksCRUD()
crud_user = UsersCRUD()


async def get_task_detail(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=60)
    task_id = int(callback_data.get("task_id"))

    markup = await get_edit_markup()

    async with state.proxy() as data:
        data["task_id"] = task_id

    await state.set_state("edit_task")

    card = await get_card_task(task_id)

    await call.message.edit_text(card)
    await call.message.edit_reply_markup(markup)


async def task_compliteb(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Задача выполнена!\nПоздравляю!", show_alert=True)

    data = await state.get_data()

    await crud_task.update_item(_id=data.get("task_id"), update_dict={"complited": True})
    await call.message.edit_reply_markup()
    await state.finish()


async def edit_body_or_dedline(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await state.set_state("choise_attr")

    msg = "Что будем редактировать?"
    markup = await get_body_and_dedline_markup()
    await call.message.answer(msg, reply_markup=markup)


async def edit_body_task(message: CallbackQuery | Message, state: FSMContext, callback_data: dict = None):
    if isinstance(message, CallbackQuery):
        msg = "Напиши новый текст задачи"
        await process_edit_task_callback(
            message=message, state_name="new_body", state=state, answer=msg, callback_data=callback_data
        )

    elif isinstance(message, Message):
        await process_edit_task_message(message=message, state=state, answer="Текст задачи обновлен")


async def edit_dedline_task(message: CallbackQuery | Message, state: FSMContext, callback_data: dict = None):
    if isinstance(message, CallbackQuery):
        msg = "Напиши дату и время для уведомления в формате дд.мм чч:мм"
        await process_edit_task_callback(
            message=message, state_name="new_dedline", state=state, answer=msg, callback_data=callback_data
        )

    elif isinstance(message, Message):
        await process_edit_task_message(message=message, state=state, answer="Дедлайн обновлен")


async def process_edit_task_callback(
    *, message: CallbackQuery, state_name: str, state: FSMContext, answer: str, callback_data: dict
):
    call = message
    async with state.proxy() as data:
        data["field"] = callback_data.get("attr")
    await state.set_state(state_name)
    await call.answer()
    await call.message.edit_text(answer)


async def process_edit_task_message(*, message: Message, state: FSMContext, answer: str):
    data = await state.get_data()

    markup = await get_main_menu()
    field = data.get("field")
    value = message.text
    match field:
        case "dedline":
            value = await dedline_format(message.text)
            await edit_notify(task_id=data.get("task_id"), user_id=message.from_user.id, dedline=value)

    await state.finish()
    await crud_task.update_item(_id=data.get("task_id"), update_dict={field: value})
    await message.answer(answer, reply_markup=markup)


async def get_card_task(task_id: int):
    task: TaskDetail = await crud_task.get_item(_id=task_id)
    dedline = task.dedline
    if task.dedline is None:
        dedline = "Не назначен"

    return f"Дедлайн: {dedline}\n\nЗадача:\n{task.body}"


async def dedline_format(text: str):  # FIXME
    dedline_date, dedline_time = text.strip().split(" ")
    dedline_date = dedline_date.replace(",", ".").replace("/", ".")
    dedline_time = dedline_time.replace(".", ":").replace(",", ":")

    dedline = datetime.strptime(f"{dedline_date}.{datetime.now().year} {dedline_time}", "%d.%m.%Y %H:%M")
    return dedline


async def edit_notify(*, task_id: int, user_id: int, dedline: datetime):
    user = await crud_user.get_item(_id=user_id)
    scheduler: AsyncIOScheduler = await bot_loader.get_scheduler()
    try:
        scheduler.remove_job(job_id=task_id)
    except JobLookupError as ex:
        logger.warning(ex)
    finally:
        scheduler.add_job(
            remind_you_of_a_task,
            DateTrigger(run_date=dedline, timezone=user.time_zone),
            id=str(task_id),
            args=(task_id, user_id),
        )


def register_edit_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_task_detail, tasks_list_call.filter(task="task"), state="tasks_list")
    dp.register_callback_query_handler(task_compliteb, edit_task_call.filter(attr="complited"), state="edit_task")
    dp.register_callback_query_handler(edit_body_or_dedline, edit_task_call.filter(attr="empty"), state="edit_task")
    dp.register_callback_query_handler(edit_body_task, edit_task_call.filter(attr="body"), state="choise_attr")
    dp.register_message_handler(edit_body_task, state="new_body")
    dp.register_callback_query_handler(edit_dedline_task, edit_task_call.filter(attr="dedline"), state="choise_attr")
    dp.register_message_handler(edit_dedline_task, state="new_dedline")
