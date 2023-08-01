from aiogram import Dispatcher, types
from adminPanel.panel import menu_changeUsers, menu_statistics
from states.admin_panel import *


async def back_to_statistics_panel(message: types.Message):
    await FormStatistics.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await menu_statistics(message)


def register_handlers_statistics_panel(dp: Dispatcher):
    dp.register_message_handler(back_to_statistics_panel,
                                content_types=['text'],
                                text='↩️ Отменить и вернуться в панель управления',
                                state=[FormNavigateCalendar.select_offset,
                                       FormUserStatistics.select_offset])
