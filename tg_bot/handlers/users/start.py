from aiogram import Dispatcher, types


async def start_bot(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}")


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start_bot, commands=["start"])
