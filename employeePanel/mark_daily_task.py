from aiogram import Dispatcher, types
from states.employee_panel import EmployeePanel, FormNavigateScheduleTasks
from keyboards import Keyboards, kb_book_calendar
from database.methods import db_get_list_daily_task_offset, db_get_schedule_tasks, \
    db_insert_many_daily_task, list_daily_task
from aiogram.dispatcher import FSMContext


async def start_form_(message: types.Message, state: FSMContext):
    await FormNavigateScheduleTasks.select_offset.set()
    async with state.proxy() as data:
        data['offset'] = 0
    await message.answer("Календарь задач", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите день календаря, который хотите просмотреть", reply_markup=Keyboards.select_day)

def register_handlers_employee_calendar_panel(dp: Dispatcher):
    dp.register_message_handler(menu_navigateScheduleTasks,
                                content_types=['text'],
                                text='Календарь заданий',
                                state=EmployeePanel.menu)