import logging

from pymysql.err import IntegrityError

from tg_bot.db_api.mysql import Database


async def insert_user(user_id: int, full_name: str, username: str = None):
    db = Database()
    try:
        db.add_user(user_id, full_name, username)
    except IntegrityError:
        logging.info("Такой пользователь уже существует")


async def insert_task(scheduler_id: hex, text: str, user_id: int, type_task: str):
    db = Database()
    once = True if type_task == "once" else False

    db.add_task(text, scheduler_id, user_id, once)
    logging.info(f"Новая запись в базе! Пользователь: {user_id}")


async def update_task(task_id: int, value: bool | str, status: bool = False):
    field = "status" if status else "todo_text"
    params = (value, task_id)

    db = Database()
    db.update_task(field, *params)
