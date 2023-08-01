from aiogram import Dispatcher, types

from states.admin_panel import FormUserStatistics, FormStatistics

from keyboards import Keyboards, kb_book_calendar
from database.methods import db_get_list_daily_task_offset, db_get_schedule_tasks, \
    db_insert_many_daily_task, list_daily_task
from aiogram.dispatcher import FSMContext


async def menu_userStatistics(message: types.Message, state: FSMContext):
    await FormUserStatistics.select_offset.set()
    async with state.proxy() as data:
        data['offset'] = 0
    await message.answer("Статистика выполнения задач по месяцам", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите месяц, который хотите посмотреть", reply_markup=Keyboards.select_day)


def register_handlers_admin_user_stat_panel(dp: Dispatcher):
    dp.register_message_handler(menu_userStatistics,
                                content_types=['text'],
                                text='Статистика выполенных задач',
                                state=FormStatistics.menu)

    dp.register_callback_query_handler(process_change_offset_back,
                                       lambda c: c.data == "back",
                                       state=FormNavigateCalendar.select_offset)