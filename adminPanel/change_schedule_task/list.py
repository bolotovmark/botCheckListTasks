from aiogram import Dispatcher, types
from adminPanel.panel import menu_changeScheduleTask
from states.admin_panel import *

from database.methods import list_schedule_task


async def process_show_list_schedule_task(message: types.Message):
    await message.answer(text=await list_schedule_task(), parse_mode='Markdown')


def register_handlers_list_schedule_task(dp: Dispatcher):
    dp.register_message_handler(process_show_list_schedule_task,
                                content_types=['text'],
                                text='Список ежедневных задач',
                                state=FormChangeScheduleTask.menu)
