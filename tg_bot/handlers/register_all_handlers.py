from aiogram import Dispatcher

from .users import *


def start_register_all_handlers(dp: Dispatcher):
    register_admin_hanlers(dp)
    register_start_handlers(dp)
    register_adding_tasks_handlers(dp)
    register_adding_notify_handlers(dp)
    register_set_timezone_handlers(dp)
    register_tasks_list_handlers(dp)

    register_echo_handler(dp)  # Эхо регистрировать самым последним
