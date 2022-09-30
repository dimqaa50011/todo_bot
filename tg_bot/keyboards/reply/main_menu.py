from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu():
    return ReplyKeyboardMarkup(
        [[KeyboardButton(text="Добавить задачу"), KeyboardButton(text="Мои задачи")]], resize_keyboard=True
    )
