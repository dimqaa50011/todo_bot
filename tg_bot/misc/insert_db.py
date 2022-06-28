from tg_bot.db_api.mysql import Database


async def add_user(user_id: int, full_name: str, username: str = None):
    db = Database()
    db.ad
