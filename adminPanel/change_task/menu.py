from aiogram import Dispatcher, types
from adminPanel.panel import menu_changeTask
from states.admin_panel import *


async def back_to_change_task_panel(message: types.Message):
    await FormChangeTasks.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await menu_changeTask(message)


def register_handlers_change_tasks_panel(dp: Dispatcher):
    dp.register_message_handler(back_to_change_task_panel,
                                content_types=['text'],
                                text='Отменить и вернуться в панель управления',
                                state=[FormAddNewEvent.type_event, FormAddNewEvent.name,
                                       FormAddNewTypeTask.name, FormWatchListEvent.menu,
                                       FormRemoveEvent.select_type, FormRemoveEvent.select_id])
