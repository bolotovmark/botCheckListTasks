from aiogram import Dispatcher, types
from states.admin_panel import (AdminPanel, FormChangeListUsers,
                                FormChangeTasks, FormChangeScheduleTask,  FormStatistics,
                                FormSetUrgentTask)
from keyboards import Keyboards


# @dp.message_handler(lambda message: message.text not in ["Панель управления пользователями", "Редактировать список типов задач"], state=AdminPanel.menu)
async def admin_menu(message: types.Message):
    await message.answer("Для навигации используйте панель", reply_markup=Keyboards.menu_admin)


# @dp.message_handler(content_types=['text'], text='Панель управления пользователями', state=AdminPanel.menu)
async def menu_changeUsers(message: types.Message):
    await FormChangeListUsers.menu.set()
    await message.answer("Панель управления пользователями", reply_markup=Keyboards.menu_change_user)


# @dp.message_handler(content_types=['text'], text='Редактировать список типов задач', state=AdminPanel.menu)
async def menu_changeTask(message: types.Message):
    await FormChangeTasks.menu.set()
    await message.answer("Панель управления задачами", reply_markup=Keyboards.list_types)


async def menu_changeScheduleTask(message: types.Message):
    await FormChangeScheduleTask.menu.set()
    await message.answer("Панель управления ежедневным расписанием", reply_markup=Keyboards.menu_change_schedule_task)


async def menu_statistics(message: types.Message):
    await FormStatistics.menu.set()
    await message.answer("Статистика", reply_markup=Keyboards.stat)


# @dp.message_handler(Text(equals='Вернуться в главное меню', ignore_case=True), state=[FormChangeListUsers])
async def cancel_handler_panels_admin(message: types.Message):
    await AdminPanel.menu.set()
    return await admin_menu(message)


def register_handlers_admin_panel(dp: Dispatcher):
    dp.register_message_handler(admin_menu,
                                lambda message:
                                message.text not in ["Панель управления пользователями",
                                                     "Панель управления задачами",
                                                     "Панель управления ежедневным расписанием",
                                                     "Статистика", "Назначить срочное задание"],
                                state=AdminPanel.menu)

    dp.register_message_handler(menu_changeUsers,
                                content_types=['text'],
                                text='Панель управления пользователями',
                                state=AdminPanel.menu)

    dp.register_message_handler(menu_changeTask,
                                content_types=['text'],
                                text='Панель управления задачами',
                                state=AdminPanel.menu)

    dp.register_message_handler(menu_changeScheduleTask,
                                content_types=['text'],
                                text='Панель управления ежедневным расписанием',
                                state=AdminPanel.menu)

    dp.register_message_handler(menu_statistics,
                                content_types=['text'],
                                text='Статистика',
                                state=AdminPanel.menu)

    dp.register_message_handler(cancel_handler_panels_admin,
                                content_types=['text'],
                                text='↩️ Вернуться в главное меню',
                                state=[FormChangeListUsers, FormChangeTasks,
                                       FormChangeScheduleTask, FormStatistics,
                                       FormSetUrgentTask])
