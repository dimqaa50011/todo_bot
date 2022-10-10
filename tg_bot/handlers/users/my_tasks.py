from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from db_api.crud.tasks_crud import TasksCRUD
from db_api.schemas.scheduler_schemas import SchrdulerSchema
from db_api.schemas.tasks_chemas import BaseTaskCallback
from tg_bot.dependecies.formatters import CustomFormatters
from tg_bot.dependecies.scheduler import SetNotify, create_notify_setter
from tg_bot.keyboards.inline.callbackdatas import paginator_call
from tg_bot.keyboards.inline.multilevel_menu import get_back_markup, list_tasks, task_call, task_detail
from tg_bot.keyboards.reply.main_menu import get_main_menu

crud_task = TasksCRUD()


async def get_my_tasks(message: Message | CallbackQuery, state: FSMContext, callback_item: BaseTaskCallback = None):
    if isinstance(message, Message):
        markup = await list_tasks(user_id=message.from_user.id)
        await message.answer("Активные задачи", reply_markup=markup)
    if isinstance(message, CallbackQuery):
        call = message
        markup = await list_tasks(user_id=call.message.chat.id)
        await call.message.edit_text("Активные задачи")
        await call.message.edit_reply_markup(markup)


async def detail_task(call: CallbackQuery, state: FSMContext, callback_item: BaseTaskCallback):
    markup = await task_detail(task_id=callback_item.task_id, user_id=callback_item.user_id)
    card = await CustomFormatters.get_card_task(int(callback_item.task_id))
    await call.message.edit_text(card, reply_markup=markup)


async def update_tasks(call: CallbackQuery, state: FSMContext, callback_item: BaseTaskCallback):
    field = callback_item.field

    if field == "complited":
        await task_compliteb(call, state=state, callback_item=callback_item)
    elif field == "body":
        await edit_body_task(call, state=state, callback_item=callback_item)

    elif field == "dedline":
        await edit_dedline_task(call, state=state, callback_item=callback_item)


async def task_compliteb(call: CallbackQuery, state: FSMContext, callback_item: BaseTaskCallback):
    await call.answer(text="Задача выполнена!\nПоздравляю!", show_alert=True)
    await crud_task.update_item(_id=int(callback_item.task_id), update_dict={"complited": True})
    notify_setter: SetNotify = await create_notify_setter()
    await notify_setter.remove_notify(task_id=callback_item.task_id)
    await get_my_tasks(call, state=state, callback_item=callback_item)


async def edit_body_task(message: CallbackQuery | Message, state: FSMContext, callback_item: BaseTaskCallback = None):
    if isinstance(message, CallbackQuery):
        await process_callback_query(
            call=message,
            state=state,
            state_name="edit_body",
            callback_item=callback_item,
            answer="Напиши новый текст задачи",
        )

    elif isinstance(message, Message):
        await process_update_task(state=state, new_value=message.text)
        markup = await get_main_menu()
        await message.answer("Задача обновлена", reply_markup=markup)


async def edit_dedline_task(
    message: CallbackQuery | Message, state: FSMContext, callback_item: BaseTaskCallback = None
):
    if isinstance(message, CallbackQuery):
        await process_callback_query(
            call=message,
            state=state,
            state_name="edit_dedline",
            callback_item=callback_item,
            answer="Напиши дату и время для уведомления в формате дд.мм чч:мм",
        )
    elif isinstance(message, Message):
        try:
            dedline = await CustomFormatters.dedline_format(message.text)
        except ValueError as ex:
            logger.warning(ex)
            await message.answer(
                "Неверный формат даты или времени. Попробуй снова.\nНапиши дату и время для уведомления в формате дд.мм чч:мм"
            )
            return

        data = await state.get_data()
        notify_setter: SetNotify = await create_notify_setter()
        await notify_setter.edit_notify(
            SchrdulerSchema(task_id=data.get("task_id"), user_id=data.get("user_id"), dedline=dedline)
        )

        await process_update_task(state=state, new_value=dedline)
        markup = await get_main_menu()
        await message.answer("Дедлайн задачи обновлен", reply_markup=markup)


async def process_callback_query(
    *, call: CallbackQuery, state: FSMContext, state_name: str, callback_item: BaseTaskCallback, answer: str
):
    markup = await get_back_markup(task_id=callback_item.task_id, user_id=callback_item.user_id)
    await call.answer(cache_time=30)
    await state.set_state(state_name)
    async with state.proxy() as data:
        data["task_id"] = int(callback_item.task_id)
        data["field"] = callback_item.field
        data["user_id"] = call.message.chat.id

    await call.message.edit_reply_markup()
    await call.message.answer(answer, reply_markup=markup)


async def process_update_task(*, state: FSMContext, new_value: str | datetime):
    data = await state.get_data()
    await crud_task.update_item(_id=data.get("task_id"), update_dict={data.get("field"): new_value})
    await state.finish()


async def next_or_previous_task_list(call: CallbackQuery, callback_data: dict):
    await call.answer()

    offset = int(callback_data.get("offset"))
    offset = offset + 10 if callback_data.get("next") == "yes" else offset - 10

    markup = await list_tasks(user_id=call.message.chat.id, offset=offset)
    await call.message.edit_reply_markup(markup)


async def navigator(call: CallbackQuery, state: FSMContext, callback_data: dict):
    if not state is None:
        await state.finish()

    current_level = callback_data.get("level")

    callback_item = BaseTaskCallback(
        user_id=callback_data.get("user_id"),
        task_id=callback_data.get("task_id"),
        field=callback_data.get("field"),
        offset=callback_data.get("offset"),
        action=callback_data.get("action"),
    )

    levels = {"0": get_my_tasks, "1": detail_task, "2": update_tasks}

    current_level_function = levels.get(current_level)
    await current_level_function(call, callback_item=callback_item, state=state)


def register_my_tasks_handlers(dp: Dispatcher):
    dp.register_message_handler(get_my_tasks, Text("Мои задачи"), state="*")
    dp.register_callback_query_handler(next_or_previous_task_list, paginator_call.filter(pager="pager"))
    dp.register_callback_query_handler(navigator, task_call.filter(), state="*")
    dp.register_message_handler(edit_body_task, state="edit_body")
    dp.register_message_handler(edit_dedline_task, state="edit_dedline")
