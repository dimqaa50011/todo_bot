from aiogram import Dispatcher, types
from loguru import logger
from sqlalchemy.exc import IntegrityError

from db_api.crud.users_crud import UsersCRUD
from db_api.schemas.users_schemas import CreateUser
from tg_bot.keyboards.reply.main_menu import get_main_menu

crud = UsersCRUD()


async def start_bot(message: types.Message):
    try:
        await crud.create_item(
            CreateUser(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
        )
    except IntegrityError as ex:
        logger.warning(ex)
    markup = await get_main_menu()
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=markup)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start_bot, commands=["start"])
