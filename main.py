import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from states.admin_panel import *
from states.none_auth import NoneAuth

from common.start import register_handlers_start

from adminPanel.panel import menu_changeUsers, register_handlers_admin_panel

from adminPanel.change_users.list_users import register_handlers_list_users
from adminPanel.change_users.menu import register_handlers_change_users_panel
from adminPanel.change_users.remove_user import register_handlers_remove_user
from adminPanel.change_users.add_new_user import register_handlers_add_new_user

from adminPanel.change_task.add_event import register_handlers_add_new_event
from adminPanel.change_task.menu import register_handlers_change_tasks_panel
from adminPanel.change_task.list_events import register_handlers_list_events
from adminPanel.change_task.remove_event import register_handlers_remove_event
from adminPanel.change_task.remove_type import register_handlers_remove_type_event

from adminPanel.change_schedule_task.menu import register_handlers_change_schedule_task_panel
from adminPanel.change_schedule_task.add_task import register_handlers_add_schedule_task
from adminPanel.change_schedule_task.list import register_handlers_list_schedule_task
from adminPanel.change_schedule_task.remove_task import register_handlers_remove_schedule_task

from adminPanel.statistics.calendar import register_handlers_admin_calendar_panel
from adminPanel.statistics.menu import register_handlers_statistics_panel
from adminPanel.statistics.user_stat import register_handlers_admin_user_stat_panel

from adminPanel.urgent_task import register_handlers_admin_panel_ugrentTask

from employeePanel.panel import register_handlers_employee_panel
from employeePanel.list_task import register_handlers_employee_calendar_panel
from employeePanel.mark_daily_task import register_handlers_employee_panel_markDailyTask
from database.methods import db_exists_user, db_remove_user

import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Conn sqlite3
# conn = sqlite3.connect('db.sqlite')

register_handlers_start(dp)  # common.start

#####
register_handlers_admin_panel(dp)  # adminPanel.panel

register_handlers_remove_user(dp)  # adminPanel.change_users.remove_user
register_handlers_add_new_user(dp)  # adminPanel.change_user.add_new_user
register_handlers_change_users_panel(dp)  # adminPanel.change_users.menu
register_handlers_list_users(dp)  # adminPanel.change_users.list_users

register_handlers_add_new_event(dp)  # adminPanel.change_task.add_event
register_handlers_change_tasks_panel(dp)  # adminPanel.change_task.menu
register_handlers_list_events(dp)   # adminPanel.change_task.list_events
register_handlers_remove_event(dp)  # adminPanel.change_task.add_event
register_handlers_remove_type_event(dp)  # adminPanel.change_task.remove_type

register_handlers_change_schedule_task_panel(dp)    # adminPanel.change_schedule_task.menu
register_handlers_add_schedule_task(dp)  # adminPanel.change_schedule_task.add_task
register_handlers_list_schedule_task(dp)  # adminPanel.change_schedule_task.list
register_handlers_remove_schedule_task(dp)  # adminPanel.change_schedule_task.remove_task

register_handlers_admin_calendar_panel(dp)  # adminPanel.statistics.calendar
register_handlers_statistics_panel(dp)  # adminPanel.statistics.menu
register_handlers_admin_user_stat_panel(dp)  # adminPanel.statistics.user_stat

register_handlers_admin_panel_ugrentTask(dp)  # adminPanel.urgent_task
#####

register_handlers_employee_panel(dp)  # employeePanel.panel
register_handlers_employee_calendar_panel(dp)  # employeePanel.list_task
register_handlers_employee_panel_markDailyTask(dp)  # employeePanel.mark_daily_task


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
