from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from states.admin_panel import *

from database.methods import db_get_list_schedule_type, db_insert_new_schedule_task, list_schedule_task

from keyboards import Keyboards, kb_types_events, kb_book_events


async def start_form_addNewScheduleTask(message: types.Message, state: FSMContext):
    await FormAddNewScheduleTask.type_id.set()
    async with state.proxy() as data:
        data['page'] = 0
    await message.answer("Открыта форма добавления ежедневных задач", reply_markup=Keyboards.empty_method)
    await message.answer("Выберите тип задачи, которую хотите добавить", reply_markup=await kb_types_events())


async def process_get_type_id(callback_query: types.CallbackQuery, state: FSMContext):
    type_id: str
    page: int
    async with state.proxy() as data:
        data['type_id'] = callback_query.data
        type_id = data['type_id']
        page = data['page']
    await FormAddNewScheduleTask.event_id.set()
    bot = callback_query.bot

    schedule_tasks = await db_get_list_schedule_type(type_id)
    out_text = ""
    if schedule_tasks:
        name_group = schedule_tasks[0][1]
        if name_group is None:
            out_text = out_text + "*🔘|Без группы|*\n"
        else:
            out_text = out_text + f"*🔘|{name_group}|*\n"
        i = 0
        for task in schedule_tasks:
            i = i + 1
            if name_group != task[1]:
                i = 1
                name_group = task[1]
                out_text = out_text + f"\n*🔘|{name_group}|*\n"
            out_text = out_text + f"{i}. *{task[0]}* / назначил: {task[3]}\n"

    else:
        out_text = out_text + 'Нет заданий'

    await bot.edit_message_text(
        text=out_text + "\n*Выберите задачу, которую хотите добавить*",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_events(type_id, page),
        parse_mode="Markdown"
    )


async def process_get_event_id(callback_query: types.CallbackQuery, state: FSMContext):
    event_id = callback_query.data
    await db_insert_new_schedule_task(event_id, callback_query.from_user.id)
    async with state.proxy() as data:
        callback_query.data = data['type_id']
    return await process_get_type_id(callback_query, state)


async def process_next_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) + 5
        callback_query.data = data['type_id']
    return await process_get_type_id(callback_query, state)


async def process_back_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) - 5
        callback_query.data = data['type_id']
    return await process_get_type_id(callback_query, state)


async def process_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    return await start_form_addNewScheduleTask(callback_query.message, state)


def register_handlers_add_schedule_task(dp: Dispatcher):
    dp.register_message_handler(start_form_addNewScheduleTask,
                                content_types=['text'],
                                text='Добавить задачи',
                                state=FormChangeScheduleTask.menu)

    dp.register_callback_query_handler(process_get_type_id,
                                       lambda c: c.data.isdigit(),
                                       state=FormAddNewScheduleTask.type_id)

    dp.register_callback_query_handler(process_get_event_id,
                                       lambda c: c.data.isdigit(),
                                       state=FormAddNewScheduleTask.event_id)

    dp.register_callback_query_handler(process_next_page,
                                       lambda c: c.data == "next",
                                       state=FormAddNewScheduleTask.event_id)

    dp.register_callback_query_handler(process_back_page,
                                       lambda c: c.data == "back",
                                       state=FormAddNewScheduleTask.event_id)

    dp.register_callback_query_handler(process_back_to_menu,
                                       lambda c: c.data == "back_to_menu",
                                       state=FormAddNewScheduleTask.event_id)
