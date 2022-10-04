import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Callable

from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from geopy.location import Location
from timezonefinder import TimezoneFinder

from db_api.crud.users_crud import UsersCRUD

crud = UsersCRUD()


async def get_city_name(message: Message, state: FSMContext):
    await state.set_state("city_name")
    await message.answer("Напиши название города, в котором сейчас находишься")


async def process_set_timezone(message: Message, state: FSMContext):
    user_timezone = await get_timezone(message.text)
    await crud.update_item(_id=message.from_user.id, update_dict={"time_zone": user_timezone})
    await state.finish()
    await message.answer("Часовой пояс установлен")


async def get_timezone(city_name: str):
    latitude, longitude = await get_latitude_and_longitude(city_name)
    time_zone = await process_timezone(latitude, longitude)

    return time_zone


async def get_latitude_and_longitude(city_name: str):
    async with Nominatim(user_agent="todo_bot", adapter_factory=AioHTTPAdapter) as geolocator:
        location: Location = await geolocator.geocode(city_name)

    return (location.latitude, location.longitude)


async def process_timezone(latitude: float, longitude: float):
    return await run_blocked_function(get_timezone_sync, latitude, longitude)


async def run_blocked_function(func: Callable, *args):
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args)


def get_timezone_sync(latitude: float, longitude: float):
    tz = TimezoneFinder()
    return tz.timezone_at_land(lat=latitude, lng=longitude)


def register_set_timezone_handlers(dp: Dispatcher):
    dp.register_message_handler(get_city_name, commands=["set_timezone"])
    dp.register_message_handler(process_set_timezone, state="city_name")
