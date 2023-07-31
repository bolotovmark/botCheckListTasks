from aiogram import Dispatcher, types

from database.methods import list_daily_task, list_daily_task_mark_false, db_get_daily_task, \
    db_check_mark_daily_task_id, db_update_daily_task
from employeePanel.panel import employee_menu
from states.employee_panel import EmployeePanel, FormMarkDailyTask
from keyboards import Keyboards, kb_book_daily_task
from aiogram.dispatcher import FSMContext


async def start_form_markDailyTask(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = 0
        data['user_id'] = message.from_user.id
    await FormMarkDailyTask.select_offset.set()
    await message.answer("Открыта форма отметки задач", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите за какой день, хотите отметить задачу", reply_markup=Keyboards.select_day)


async def process_get_offset_day_id(callback_query: types.CallbackQuery, state: FSMContext):
    day: int
    async with state.proxy() as data:
        data['day'] = callback_query.data
        day = callback_query.data

    bot = callback_query.bot
    out_text = await list_daily_task_mark_false(day)
    await FormMarkDailyTask.select_task_id.set()
    await bot.edit_message_text(
        text=out_text + "\n*Выберите задачу, которую хотите удалить*",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_daily_task(day, 0),
        parse_mode="Markdown"
    )


async def process_change_day_back(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = "-1"
        callback_query.data = data['day']
        data['page'] = "0"
        return await process_get_offset_day_id(callback_query, state)


async def process_change_day_today(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = 0
        callback_query.data = data['day']
        data['page'] = "0"
        return await process_get_offset_day_id(callback_query, state)


async def process_reload_daily_task(callback_query: types.CallbackQuery, state: FSMContext):
    day: int
    page: int
    async with state.proxy() as data:
        day = data['day']
        data['page'] = callback_query.data
        page = callback_query.data
    bot = callback_query.bot

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_daily_task(day, page),
    )


async def process_next_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) + 5
        callback_query.data = data['page']
        return await process_reload_daily_task(callback_query, state)


async def process_back_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) - 5
        callback_query.data = data['page']
        return await process_reload_daily_task(callback_query, state)


async def process_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = 0
        callback_query.message.from_user.id = data['user_id']
    return await start_form_markDailyTask(callback_query.message, state)


async def process_get_task_id(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['task_id'] = callback_query.data
    await FormMarkDailyTask.select_mark.set()
    task = await db_get_daily_task(callback_query.data)
    out_text = (f"Задача: *{task[1]}*\n"
                f"Тип: *{task[2]}*\n"
                f"Группа:  *{task[3]}*\n\n")
    await callback_query.bot.edit_message_text(
        text=f"{out_text}Отметить задачу законченной?",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=Keyboards.select_bool,
        parse_mode="Markdown"
    )


async def process_mark_false(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        callback_query.data = data['day']
        return await process_get_offset_day_id(callback_query, state)


async def process_mark_true(callback_query: types.CallbackQuery):
    await FormMarkDailyTask.description.set()
    await callback_query.bot.edit_message_text(
        text=f"❗️ Напишите описание к выполенной задаче",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=Keyboards.skip_stage,
        parse_mode="Markdown"
    )


async def process_set_description(message: types.Message, state: FSMContext):
    task_id: int
    user_id: str
    description = message.text
    async with state.proxy() as data:
        task_id = data['task_id']
        user_id = data['user_id']
    mark_task = await db_check_mark_daily_task_id(task_id)
    if mark_task:
        await db_update_daily_task(task_id, user_id, description)
        await message.answer("✅ Задача успешно отмечена!")
    else:

        await message.answer("❌ Задача была отмечена ранее другим пользователем!")
    await state.reset_data()
    await EmployeePanel.menu.set()
    # await state.finish()
    return await employee_menu(message)


async def process_skip_stage(callback_query: types.CallbackQuery, state: FSMContext):
    callback_query.message.text = None
    return await process_set_description(callback_query.message, state)


def register_handlers_employee_panel_markDailyTask(dp: Dispatcher):
    dp.register_message_handler(start_form_markDailyTask,
                                content_types=['text'],
                                text='Отметить выполненные задания',
                                state=EmployeePanel.menu)

    dp.register_callback_query_handler(process_change_day_back,
                                       lambda c: c.data == "back",
                                       state=FormMarkDailyTask.select_offset)

    dp.register_callback_query_handler(process_change_day_today,
                                       lambda c: c.data == "today",
                                       state=FormMarkDailyTask.select_offset)

    dp.register_callback_query_handler(process_next_page,
                                       lambda c: c.data == "next",
                                       state=FormMarkDailyTask.select_task_id)

    dp.register_callback_query_handler(process_back_page,
                                       lambda c: c.data == "back",
                                       state=FormMarkDailyTask.select_task_id)

    dp.register_callback_query_handler(process_back_to_menu,
                                       lambda c: c.data == "back_to_menu",
                                       state=FormMarkDailyTask.select_task_id)

    dp.register_callback_query_handler(process_get_task_id,
                                       lambda c: c.data.isdigit(),
                                       state=FormMarkDailyTask.select_task_id)

    dp.register_callback_query_handler(process_mark_false,
                                       lambda c: c.data == "false",
                                       state=FormMarkDailyTask.select_mark)

    dp.register_callback_query_handler(process_mark_true,
                                       lambda c: c.data == "true",
                                       state=FormMarkDailyTask.select_mark)

    dp.register_message_handler(process_set_description,
                                lambda message:
                                message.text != '↩️ Отменить и вернуться в панель управления',
                                state=FormMarkDailyTask.description)

    dp.register_callback_query_handler(process_skip_stage,
                                       lambda c: c.data == "skip",
                                       state=FormMarkDailyTask.description)
