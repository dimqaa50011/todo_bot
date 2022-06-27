from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.settings import Settings


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool = None):
        self.is_admin = is_admin

    async def check(self, obj: types.Message) -> bool:
        if self.is_admin is None:
            return False
        settings: Settings = obj.bot.get('settings')
        return obj.from_user.id in settings.tg_bot.admins
