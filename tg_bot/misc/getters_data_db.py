import logging

from tg_bot.db_api.mysql import Database


async def get_my_task(fetch: bool = False, fetchall: bool = False, **kwargs):
    db = Database()
    data = db.get_task(fetch=fetch, fetchall=fetchall, **kwargs)
    logging.info(f"Данные получены {data}")

    return data
