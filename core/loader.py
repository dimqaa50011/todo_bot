from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient
from tzlocal import get_localzone

from .config import settings


class Loader:
    def __init__(self):
        self.__bot = Bot(token=settings.bot_config.BOT_TOKEN)
        self.__storage = self.get_fsm_storage()
        self.__dp = Dispatcher(bot=self.__bot, storage=self.__storage)
        self.__admins = list(map(int, settings.bot_config.ADMINS.split(",")))
        self.__bot["admins"] = self.__admins
        self.__client_mongodb = MongoClient(settings.scheduler_db.SCHEDULER_HOST, settings.scheduler_db.SCHEDULER_PORT)
        self.__default_jobstorage_scheduler = {"default": MongoDBJobStore(client=self.__client_mongodb)}
        self.__scheduler = AsyncIOScheduler(
            jobstores=self.__default_jobstorage_scheduler, timezone=str(get_localzone())
        )

    async def get_dispatcher(self):
        return self.__dp

    def get_fsm_storage(self):
        return RedisStorage2() if settings.bot_config.USE_REDIS else MemoryStorage()

    async def get_admins(self):
        return self.__admins

    async def get_bot_instance(self):
        return self.__bot

    async def get_all_attrs(self):
        return (self.__bot, self.__dp, self.__storage, self.__admins)

    async def get_scheduler(self):
        return self.__scheduler


bot_loader = Loader()
