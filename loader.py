from aiogram import Bot, Dispatcher
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient

from tg_bot.settings import load_settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler_di import ContextSchedulerDecorator


class LoaderCoreBot:
    __settings = load_settings('.env')
    __bot = Bot(token=__settings.tg_bot.bot_token, parse_mode='HTML')
    __storage = MemoryStorage()
    __dp = Dispatcher(bot=__bot, storage=__storage)

    client = MongoClient("localhost", 27020)
    job_stores = {
        'default': MongoDBJobStore(client=client)
    }

    __scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))

    @classmethod
    async def load_core(cls):
        return cls.__bot, cls.__dp, cls.__storage, cls.__settings, cls.__scheduler

    @classmethod
    async def load_bot(cls):
        return cls.__bot
