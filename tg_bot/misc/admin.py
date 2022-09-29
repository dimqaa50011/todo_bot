from aiogram import Dispatcher
from loguru import logger


async def notify_admins(dp: Dispatcher, admins: list):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text="Бот запущен")
        except Exception as ex:
            logger.error(ex)