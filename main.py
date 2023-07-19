import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from states.admin_panel import FormRemoveUser, FormChangeListUsers
from states.none_auth import NoneAuth

from common.start import register_handlers_start

from adminPanel.change_users.list_users import register_handlers_list_users
from adminPanel.change_users.menu import register_handlers_change_users_panel
from adminPanel.change_users.remove_user import register_handlers_remove_user
from adminPanel.change_users.add_new_user import register_handlers_add_new_user
from adminPanel.panel import menu_changeUsers, register_handlers_admin_panel

from database.methods import db_exists_user, db_remove_user


API_TOKEN = '6323770760:AAFpXBDSSXeg5fqscK2ReStDX8oVFfSoDYE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Conn sqlite3
#conn = sqlite3.connect('db.sqlite')

register_handlers_start(dp)  # common.start
register_handlers_list_users(dp)  # adminPanel.change_users.list_users
register_handlers_change_users_panel(dp)  # adminPanel.change_users.menu
register_handlers_admin_panel(dp)  # adminPanel.panel
register_handlers_remove_user(dp)  # adminPanel.change_users.remove_user
register_handlers_add_new_user(dp)


# Удалить пользователя

@dp.message_handler(content_types=['text'], text='✅', state=FormRemoveUser.check)
async def remove_approved(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = await db_exists_user(int(data['id']))
        if user:
            user_id = user[0]

            await db_remove_user(user_id)
            await state.reset_state()
            await FormChangeListUsers.menu.set()

            drop_state = dp.current_state(chat=user_id, user=user_id)
            await drop_state.set_state(NoneAuth.start)

            await message.answer("Пользователь удален")

        else:
            await message.answer("⚠️\nВидимо пользователя успели удалить до вашего запроса."
                                 "Обновите и проверьте список пользователей")

        return await menu_changeUsers(message)

############

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
