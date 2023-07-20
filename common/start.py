from aiogram import Dispatcher, types

from keyboards import Keyboards

from states.admin_panel import AdminPanel
from states.none_auth import NoneAuth
from states.employee_panel import EmployeePanel

from database.methods import db_exists_user


# @dp.message_handler(state=[None, NoneAuth.start])
# @dp.message_handler(commands=['menu', 'start'])
async def start(message: types.Message):
    user = await db_exists_user(message.from_user.id)
    if user:
        if int(user[1]) == 2:
            keyboard = Keyboards.menu_admin
            await AdminPanel.menu.set()
        elif int(user[1]) == 1:
            keyboard = Keyboards.non_auth
            await EmployeePanel.menu.set()
        else:
            keyboard = Keyboards.non_auth
        await message.answer(f"Здравствуйте {user[2]}!", reply_markup=keyboard)
    else:
        await message.answer(
            f"Вас нет в базе. Обратитесь к администратору. \n\nВаш id для регистрации: {message.from_user.id}")


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, state=[None, NoneAuth.start])
    dp.register_message_handler(start, commands=['menu', 'start'])
