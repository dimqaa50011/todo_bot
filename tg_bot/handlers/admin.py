from aiogram import types, Dispatcher


async def admin_command(message: types.Message):
    await message.answer('Сообщение для администратора')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=[
                                'admin_start'], is_admin=True)
