from aiogram import Dispatcher, types
from states.employee_panel import EmployeePanel, FormNavigateScheduleTasks
from keyboards import Keyboards


async def employee_menu(message: types.Message):
    await message.answer("Для навигации используйте панель", reply_markup=Keyboards.menu_employee)


async def menu_navigateScheduleTasks(message: types.Message):
    await FormNavigateScheduleTasks.menu.set()
    await message.answer("Календарь заданий", reply_markup=Keyboards.empty_method)


async def cancel_handler_panels_employee(message: types.Message):
    await EmployeePanel.menu.set()
    return await employee_menu(message)


def register_handlers_employee_panel(dp: Dispatcher):
    dp.register_message_handler(employee_menu,
                                lambda message: message.text not in ["Календарь заданий"],
                                state=EmployeePanel.menu)

    dp.register_message_handler(menu_navigateScheduleTasks(),
                                content_types=['text'],
                                text='Календарь заданий',
                                state=EmployeePanel.menu)

    dp.register_message_handler(cancel_handler_panels_employee,
                                content_types=['text'],
                                text='↩️ Вернуться в главное меню',
                                state=[FormNavigateScheduleTasks])
