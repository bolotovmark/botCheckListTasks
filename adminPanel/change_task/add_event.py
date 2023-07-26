from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.admin_panel import *

from database.methods import db_get_list_types_event, db_insert_new_type_event
from database.methods import db_insert_new_event, db_get_name_type_event, db_insert_new_event_3

from keyboards import Keyboards

from adminPanel.panel import menu_changeTask


async def start_form_AddNewEvent(message: types.Message):
    await FormAddNewEvent.type_event.set()
    await message.answer("Открыта форма добавления новой задачи", reply_markup=Keyboards.empty_method)
    types_event = await db_get_list_types_event()
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    buf_list = []
    i: int
    i = 0
    for type_event in types_event:
        i = i + 1
        buf_list.append(InlineKeyboardButton(f"{type_event[1]}", callback_data=f"{type_event[0]}"))

        if i % 2 == 0:
            inline_kb_full.row(buf_list[0], buf_list[1])
            buf_list.clear()

    if len(buf_list) != 0:
        inline_kb_full.row(buf_list[0])

    inline_kb_full.add(InlineKeyboardButton("🆕 Придумать новый тип задачи", callback_data="addNewTypeTask"))
    await message.answer("Укажите тип новой задачи c клавиатуры:", reply_markup=inline_kb_full)


async def start_form_AddNewTypeTask(callback_query: types.CallbackQuery):
    await FormAddNewTypeTask.name.set()
    bot = callback_query.bot
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "Введите название нового типа:")
    # await callback_query.answer("Введите название нового типа:")


async def process_get_new_type(message: types.Message, state: FSMContext):
    await FormAddNewEvent.name.set()
    query = await db_insert_new_type_event(message.text)
    async with state.proxy() as data:
        data['type_event'] = query[0]
    await message.answer("Новый тип добавлен в базу")
    await message.answer("Придумайте наименование задаче: ")


async def process_get_type(callback_query: types.CallbackQuery, state: FSMContext):

    await FormAddNewEvent.name.set()
    async with state.proxy() as data:
        data['type_event'] = callback_query.data
    bot = callback_query.bot
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "Придумайте наименование задачи: ")


async def process_name_type_task(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FormAddNewEvent.bool_check.set()
    await message.answer("Хотите добавить ключевое слово для группировки?", reply_markup=Keyboards.boolean_keyboard)


async def process_choice_true(message: types.Message, state: FSMContext):
    await FormAddNewEvent.group_name.set()
    await message.answer("Напишите к какой группе относиться задача", reply_markup=Keyboards.empty_method)



async def process_choice_false(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_type = data['type_event']
        name = data['name']
        await db_insert_new_event(name, id_type)

        name_type_event = await db_get_name_type_event(id_type)

        await message.answer("Добавлена новая задача в базу\n\n"
                             f"\nНаименование: *{name}*\n"
                             f"Тип задачи: *{name_type_event[0]}*\n", parse_mode="Markdown")

        await FormChangeTasks.menu.set()
        return await menu_changeTask(message)


async def process_group_task(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_type = data['type_event']
        name = data['name']
        group = message.text
        await db_insert_new_event_3(name, id_type, group)

        name_type_event = await db_get_name_type_event(id_type)

        await message.answer("Добавлена новая задача в базу\n\n"
                             f"\nНаименование: *{name}*\n"
                             f"Тип задачи: *{name_type_event[0]}*\n"
                             f"Группа: *{group}*", parse_mode="Markdown")

        await FormChangeTasks.menu.set()
        return await menu_changeTask(message)


def register_handlers_add_new_event(dp: Dispatcher):

    dp.register_message_handler(start_form_AddNewEvent,
                                content_types=['text'],
                                text='Добавить новую задачу',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(process_get_type,
                                       lambda c: c.data.isdigit(),
                                       state=FormAddNewEvent.type_event)

    dp.register_message_handler(process_get_new_type,
                                lambda message: message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewTypeTask.name)

    dp.register_message_handler(process_name_type_task,
                                lambda message: message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewEvent.name)

    dp.register_callback_query_handler(start_form_AddNewTypeTask,
                                       lambda c: c.data == "addNewTypeTask",
                                       state=FormAddNewEvent.type_event)

    dp.register_message_handler(process_choice_false,
                                content_types=['text'],
                                text='❌',
                                state=FormAddNewEvent.bool_check)

    dp.register_message_handler(process_choice_true,
                                content_types=['text'],
                                text='✅',
                                state=FormAddNewEvent.bool_check)

    dp.register_message_handler(process_group_task,
                                lambda message: message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewEvent.group_name)
