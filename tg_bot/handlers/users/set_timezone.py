from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from db_api.crud.users_crud import UsersCRUD
from tg_bot.dependecies.geolocation import Geolocator

crud = UsersCRUD()


async def get_city_name(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state("city_name")
    await message.answer("Напиши название города, в котором сейчас находишься")


async def process_set_timezone(message: Message, state: FSMContext):
    user_timezone = await Geolocator.get_timezone(message.text)
    await crud.update_item(user_id=message.from_user.id, update_dict={"time_zone": user_timezone})
    await state.finish()
    await message.answer("Часовой пояс установлен")


def register_set_timezone_handlers(dp: Dispatcher):
    dp.register_message_handler(get_city_name, commands=["set_timezone"], state="*")
    dp.register_message_handler(process_set_timezone, state="city_name")
