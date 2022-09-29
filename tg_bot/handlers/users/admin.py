from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(message: Message):
    await message.answer("Привет, админ!")


def register_admin_hanlers(dp: Dispatcher):
    dp.register_message_handler(callback=admin_start, commands=["start_admin"], is_admin=True)
