from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from states.admin_panel import FormAddNewUser, FormChangeListUsers
from database.methods import db_exists_user, db_insert_new_user
from adminPanel.panel import menu_changeUsers
from keyboards import Keyboards


# @dp.message_handler(content_types=['text'], text='Добавить', state=FormChangeListUsers.menu)
async def start_form_AddNewUser(message: types.Message):
    await FormAddNewUser.id.set()
    await message.answer("Введите ID нового пользователя:", reply_markup=Keyboards.empty_method)


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FormAddNewUser.id)
async def process_id_invalid(message: types.Message):
    """
    id is invalid
    """
    return await message.reply("ID должен состоять только из чисел. Пожалуйста, уточните ID у нового пользователя.")


# @dp.message_handler(lambda message: message.text.isdigit(), state=FormAddNewUser.id)
async def process_id(message: types.Message, state: FSMContext):
    user = await db_exists_user(int(message.text))
    if not user:
        await FormAddNewUser.next()
        await state.update_data(id=int(message.text))

        await message.answer("Укажите должность с клавиатуры", reply_markup=Keyboards.position)
    else:
        await message.answer(f"Этот пользователь уже находиться в базе")


# @dp.message_handler(lambda message: message.text not in ["Администратор", "Рабочий"], state=FormAddNewUser.position_name)
async def process_position_invalid(message: types.Message):
    return await message.reply("Выберите должность c клавиатуры:", reply_markup=Keyboards.position)


# @dp.message_handler(lambda message: message.text in ["Администратор", "Рабочий"], state=FormAddNewUser.position_name)
async def process_position(message: types.Message, state):
    await FormAddNewUser.next()
    await state.update_data(position_name=message.text)

    async with state.proxy() as data:
        if message.text == "Администратор":
            data['position_id'] = 2
        else:
            data['position_id'] = 1
    await message.answer("Напишите ФИО", reply_markup=Keyboards.empty_method)


# @dp.message_handler(state=FormAddNewUser.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer(f"Новый пользователь добавлен:\n"
                             f"ID: {data['id']}\n"
                             f"Должность: {data['position_name']}\n"
                             f"ФИО: {data['name']}")
    await state.finish()
    await db_insert_new_user(data['id'], data['position_id'], data['name'])
    await FormChangeListUsers.menu.set()

    return await menu_changeUsers(message)


def register_handlers_add_new_user(dp: Dispatcher):
    dp.register_message_handler(start_form_AddNewUser, content_types=['text'],
                                text='Добавить',
                                state=FormChangeListUsers.menu)
    dp.register_message_handler(process_id_invalid,
                                lambda message: not message.text.isdigit(),
                                state=FormAddNewUser.id)
    dp.register_message_handler(process_id,
                                lambda message: message.text.isdigit(),
                                state=FormAddNewUser.id)
    dp.register_message_handler(process_position_invalid,
                                lambda message: message.text not in ["Администратор", "Рабочий"],
                                state=FormAddNewUser.position_name)
    dp.register_message_handler(process_position,
                                lambda message: message.text in ["Администратор", "Рабочий"],
                                state=FormAddNewUser.position_name)
    dp.register_message_handler(process_name, state=FormAddNewUser.name)
