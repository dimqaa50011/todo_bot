from aiogram import Dispatcher
from aiogram.types import Message


async def echo_text(message: Message):
    await message.answer(f"Эхо текс без состояния {message.text}")


def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(callback=echo_text)
