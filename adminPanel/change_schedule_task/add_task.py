from aiogram import Dispatcher, types
from adminPanel.panel import menu_changeScheduleTask
from states.admin_panel import *


# @dp.message_handler(Text(equals='Отменить и вернуться в панель управления', ignore_case=True), state=[FormAddNewUser.id, FormAddNewUser.position_name, FormAddNewUser.name, FormRemoveUser.id, FormRemoveUser.check])
async def start_form_addNewScheduleTask(message: types.Message):
    print(1)
    pass


def register_handlers_add_schedule_task(dp: Dispatcher):
    dp.register_message_handler(start_form_addNewScheduleTask,
                                content_types=['text'],
                                text='Добавить задачи',
                                state=FormChangeScheduleTask.menu)
