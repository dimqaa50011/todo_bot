from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self.__scheduler = scheduler

    async def on_process_message(self, message: types.Message, middle_data: dict):
        middle_data["scheduler"] = self.__scheduler

    async def on_process_callback_query(self, call: types.CallbackQuery, middle_data: dict):
        middle_data["scheduler"] = self.__scheduler


