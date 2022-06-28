import asyncio
import logging

from aiogram import Dispatcher

from loader import LoaderCoreBot
from tg_bot.db_api.mysql import Database
from tg_bot.filters import AdminFilter
from tg_bot.handlers import register_admin, register_echo, register_start
from tg_bot.handlers.add_task import register_add_task_handler
from tg_bot.handlers.tasks_control import register_control_tasks_handlers
from tg_bot.misc.cancel_handler import register_cancel

logger = logging.getLogger(__name__)


def register_middlewares(dp):
    # dp.setup_middleware()
    pass


def register_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_handlers(dp):
    register_admin(dp)
    register_start(dp)
    register_add_task_handler(dp)
    register_control_tasks_handlers(dp)
    register_cancel(dp)

    register_echo(dp)


async def on_startup_notify(dp: Dispatcher, admins: list):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def runner():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    bot, dp, storage, settings = await LoaderCoreBot.load_core()

    db = Database()
    db.create_tables()

    register_middlewares(dp)
    register_filters(dp)
    register_handlers(dp)

    await on_startup_notify(dp, settings.tg_bot.admins)

    try:
        await dp.start_polling()
    finally:
        await storage.close()
        await storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(runner())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
