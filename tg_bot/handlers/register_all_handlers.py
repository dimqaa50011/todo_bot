from aiogram import Dispatcher

from .users import *


def start_register_all_handlers(dp: Dispatcher):
    register_admin_hanlers(dp)
    register_start_handlers(dp)

    register_echo_handler(dp)  # Эхо регистрировать самым последним
