from aiogram import Dispatcher, types
from states.employee_panel import EmployeePanel, FormNavigateScheduleTasks
from keyboards import Keyboards


async def employee_menu(message: types.Message):
    await message.answer("Для навигации используйте панель", reply_markup=Keyboards.menu_employee)


async def cancel_handler_panels_employee(message: types.Message):
    await EmployeePanel.menu.set()
    return await employee_menu(message)


async def back_to_employee_panel(message: types.Message):
    await EmployeePanel.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await employee_menu(message)


def register_handlers_employee_panel(dp: Dispatcher):
    dp.register_message_handler(employee_menu,
                                lambda message: message.text not in ["Календарь заданий"],
                                state=EmployeePanel.menu)

    dp.register_message_handler(cancel_handler_panels_employee,
                                content_types=['text'],
                                text='↩️ Вернуться в главное меню',
                                state=[FormNavigateScheduleTasks])

    dp.register_message_handler(back_to_employee_panel,
                                content_types=['text'],
                                text='↩️ Отменить и вернуться в панель управления',
                                state=[FormNavigateScheduleTasks.select_offset, FormNavigateScheduleTasks.navigate])
