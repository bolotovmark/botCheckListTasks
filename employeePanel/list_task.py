from aiogram import Dispatcher, types
from states.employee_panel import EmployeePanel, FormNavigateScheduleTasks
from keyboards import Keyboards, kb_book_calendar
from database.methods import db_get_list_daily_task_offset, db_get_schedule_tasks, \
    db_insert_many_daily_task, list_daily_task
from aiogram.dispatcher import FSMContext


async def menu_navigateScheduleTasks(message: types.Message, state: FSMContext):
    await FormNavigateScheduleTasks.select_offset.set()
    async with state.proxy() as data:
        data['offset'] = 0
    await message.answer("Календарь задач", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите день календаря, который хотите просмотреть", reply_markup=Keyboards.select_day)


async def process_select_offset(callback_query: types.CallbackQuery, state: FSMContext):
    offset: int
    async with state.proxy() as data:
        data['offset'] = callback_query.data
        offset = data['offset']
    bot = callback_query.bot
    out_text = await list_daily_task(offset)
    await bot.edit_message_text(
        text=out_text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_calendar(offset),
        parse_mode="Markdown"
    )


async def process_change_offset_back(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = int(data['offset']) - 1
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_change_offset_next(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = int(data['offset']) + 1
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_change_offset_today(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = 0
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_generate_daily_task(callback_query: types.CallbackQuery, state: FSMContext):
    if not await db_get_list_daily_task_offset(0):
        schedule_task = await db_get_schedule_tasks()
        await db_insert_many_daily_task(schedule_task)

    callback_query.data = 0
    return await process_select_offset(callback_query, state)


def register_handlers_employee_calendar_panel(dp: Dispatcher):
    dp.register_message_handler(menu_navigateScheduleTasks,
                                content_types=['text'],
                                text='Календарь заданий',
                                state=EmployeePanel.menu)

    dp.register_callback_query_handler(process_change_offset_back,
                                       lambda c: c.data == "back",
                                       state=FormNavigateScheduleTasks.select_offset)

    dp.register_callback_query_handler(process_change_offset_next,
                                       lambda c: c.data == "next",
                                       state=FormNavigateScheduleTasks.select_offset)

    dp.register_callback_query_handler(process_change_offset_today,
                                       lambda c: c.data == "today",
                                       state=FormNavigateScheduleTasks.select_offset)

    dp.register_callback_query_handler(process_generate_daily_task,
                                       lambda c: c.data == "generate",
                                       state=FormNavigateScheduleTasks.select_offset)
    # dp.register_message_handler(process_generate_daily_task,
    #                             content_types=['text'],
    #                             text='Сгенерировать задания на сегодня',
    #                             state=FormNavigateScheduleTasks.check)
    #
    # dp.register_callback_query_handler(process_navigate_back,
    #                                    lambda c: c.data == "back",
    #                                    state=FormNavigateScheduleTasks.navigate)
    #
    # dp.register_callback_query_handler(process_navigate_next,
    #                                    lambda c: c.data == "next",
    #                                    state=FormNavigateScheduleTasks.navigate)
