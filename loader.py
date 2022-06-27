from aiogram import Bot, Dispatcher
from tg_bot.settings import load_settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class LoaderCoreBot:
    __settings = load_settings('.env')
    __bot = Bot(token=__settings.tg_bot.bot_token, parse_mode='HTML')
    __storage = MemoryStorage()
    __dp = Dispatcher(bot=__bot, storage=__storage)
    
    @classmethod
    async def load_core(cls):
        return cls.__bot, cls.__dp, cls.__storage, cls.__settings
    


