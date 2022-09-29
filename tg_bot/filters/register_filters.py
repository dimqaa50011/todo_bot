from aiogram import Dispatcher

from .admin import IsAdmin


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
