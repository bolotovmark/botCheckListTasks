from aiogram import Dispatcher, types

from states.admin_panel import FormUserStatistics, FormStatistics

from keyboards import Keyboards, kb_book_calendar, kb_book_admin_calendar_month
from database.methods import db_get_list_daily_task_offset, db_get_schedule_tasks, \
    db_insert_many_daily_task, list_daily_task, list_month_statistics
from aiogram.dispatcher import FSMContext


async def menu_userStatistics(message: types.Message, state: FSMContext):
    await FormUserStatistics.select_offset.set()
    async with state.proxy() as data:
        data['offset'] = 0
    await message.answer("Статистика выполнения задач по месяцам", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите месяц, который хотите посмотреть", reply_markup=Keyboards.select_month)


async def process_select_offset(callback_query: types.CallbackQuery, state: FSMContext):
    offset: int
    async with state.proxy() as data:
        data['offset'] = callback_query.data
        offset = data['offset']
    bot = callback_query.bot
    out_text = await list_month_statistics(offset)
    await bot.edit_message_text(
        text=out_text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_admin_calendar_month(offset),
        parse_mode="Markdown"
    )


async def process_set_offset_this_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = 0
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_set_offset_last_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = -1
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_change_offset_next_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = int(data['offset']) + 1
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


async def process_change_offset_before_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['offset'] = int(data['offset']) - 1
        callback_query.data = data['offset']
        return await process_select_offset(callback_query, state)


def register_handlers_admin_user_stat_panel(dp: Dispatcher):
    dp.register_message_handler(menu_userStatistics,
                                content_types=['text'],
                                text='Статистика выполенных задач',
                                state=FormStatistics.menu)

    dp.register_callback_query_handler(process_set_offset_this_month,
                                       lambda c: c.data in ["this_month", "today"],
                                       state=FormUserStatistics.select_offset)

    dp.register_callback_query_handler(process_change_offset_before_month,
                                       lambda c: c.data == "back",
                                       state=FormUserStatistics.select_offset)

    dp.register_callback_query_handler(process_change_offset_next_month,
                                       lambda c: c.data == "next",
                                       state=FormUserStatistics.select_offset)

    dp.register_callback_query_handler(process_set_offset_last_month,
                                       lambda c: c.data == "last_month",
                                       state=FormUserStatistics.select_offset)

