from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsAdmin(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool = None) -> None:
        self.is_admin = is_admin

    async def check(self, obj: Message) -> bool:
        if self.is_admin is None:
            return False

        return obj.from_user.id in obj.bot.get("admins")
