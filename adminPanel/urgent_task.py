from aiogram import Dispatcher, types

from adminPanel.panel import admin_menu, cancel_handler_panels_admin
from database.methods import db_get_date_offset, db_insert_urgent_task
from aiogram.dispatcher import FSMContext
from states.admin_panel import FormSetUrgentTask, AdminPanel
from keyboards import Keyboards


async def menu_urgentTask(message: types.Message):
    await FormSetUrgentTask.select_name.set()
    await message.answer("*Введите название срочной задачи:* ",
                         parse_mode="Markdown",
                         reply_markup=Keyboards.back_to_main)


async def process_set_urgentTask(message: types.Message, state: FSMContext):
    name_event = message.text
    await db_insert_urgent_task(name_event)
    await message.answer("✅ Задача успешно добавлена!")
    return await cancel_handler_panels_admin(message)


def register_handlers_admin_panel_ugrentTask(dp: Dispatcher):
    dp.register_message_handler(menu_urgentTask,
                                content_types=['text'],
                                text='Назначить срочное задание',
                                state=AdminPanel.menu)

    dp.register_message_handler(process_set_urgentTask,
                                lambda message:
                                message.text != "↩️ Вернуться в главное меню",
                                content_types='text',
                                state=FormSetUrgentTask.select_name)
