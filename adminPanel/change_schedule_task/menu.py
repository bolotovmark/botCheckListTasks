from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from adminPanel.panel import menu_changeScheduleTask
from states.admin_panel import *


async def back_to_change_schedule_task_panel(message: types.Message, state: FSMContext):
    await state.reset_data()
    await FormChangeListUsers.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await menu_changeScheduleTask(message)


def register_handlers_change_schedule_task_panel(dp: Dispatcher):
    dp.register_message_handler(back_to_change_schedule_task_panel,
                                content_types=['text'],
                                text='↩️ Отменить и вернуться в панель управления',
                                state=[FormAddNewScheduleTask.type_id, FormAddNewScheduleTask.event_id,
                                       FormRemoveScheduleTask.type_id, FormRemoveScheduleTask.task_id])
