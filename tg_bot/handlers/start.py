from aiogram import types, Dispatcher
from tg_bot.keyboards.reply.menu import main_menu
from tg_bot.misc.insert_db import insert_user


async def start(message: types.Message):
    await insert_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=main_menu)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
