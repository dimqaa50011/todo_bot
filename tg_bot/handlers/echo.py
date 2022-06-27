from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def echo(message: types.Message):
    text = [
        'Эхо без состояния',
        'Сообщение',
        message.text
    ]
    await message.answer('\n'.join(text))


async def echo_state(message: types.Message, state: FSMContext):
    text = [
        f'Эхо в состоянии {await state.get_state()}',
        'Сообщение',
        message.text
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo)
    dp.register_message_handler(echo_state, state='*', content_types=types.ContentTypes.ANY)
