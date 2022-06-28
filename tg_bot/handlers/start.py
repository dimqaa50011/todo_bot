from aiogram import types, Dispatcher
from tg_bot.keyboards.reply.menu import main_menu


async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=main_menu)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
