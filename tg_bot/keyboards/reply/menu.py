from cgitb import text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Добавить задачу"),
            KeyboardButton(text="Мои задачи")
        ]
    ], resize_keyboard=True
)
