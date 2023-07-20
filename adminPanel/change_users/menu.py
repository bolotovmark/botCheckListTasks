from aiogram import Dispatcher, types
from adminPanel.panel import menu_changeUsers
from states.admin_panel import *


# @dp.message_handler(Text(equals='Отменить и вернуться в панель управления', ignore_case=True), state=[FormAddNewUser.id, FormAddNewUser.position_name, FormAddNewUser.name, FormRemoveUser.id, FormRemoveUser.check])
async def back_to_change_users_panel(message: types.Message):
    await FormChangeListUsers.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await menu_changeUsers(message)


def register_handlers_change_users_panel(dp: Dispatcher):
    dp.register_message_handler(back_to_change_users_panel,
                                content_types=['text'],
                                text='Отменить и вернуться в панель управления',
                                state=[FormAddNewUser.id, FormAddNewUser.position_name,
                                       FormAddNewUser.name, FormRemoveUser.id, FormRemoveUser.check])
