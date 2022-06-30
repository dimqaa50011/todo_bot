import uuid
from datetime import datetime, date

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def format_todo(sql: str, **kwargs):
    sql += " AND ".join(tuple((f"{item} = %s" for item in kwargs.keys())))
    parameters = tuple((values for values in kwargs.values()))
    return sql, parameters


async def format_date(date_str: str):
    return datetime.strptime(f"{date_str}.{date.today().year}", "%d.%m.%Y")


async def get_scheduler_id():
    return uuid.uuid1().hex