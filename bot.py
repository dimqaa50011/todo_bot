import asyncio

from loguru import logger

from core import bot_loader
from tg_bot.filters import register_all_filters
from tg_bot.handlers.register_all_handlers import start_register_all_handlers
from tg_bot.misc.admin import notify_admins
from tg_bot.misc.bot_commands import set_default_commands


async def runner():
    bot, dp, storage, admins = await bot_loader.get_all_attrs()

    register_all_filters(dp)

    start_register_all_handlers(dp)

    await set_default_commands(dp)
    await notify_admins(dp, admins)

    logger.info("Bot started!")

    try:
        await dp.start_polling()
    finally:
        await storage.close()
        await storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(runner())
    except (KeyboardInterrupt, SystemError) as ex:
        logger.warning("Bot stopped!")
