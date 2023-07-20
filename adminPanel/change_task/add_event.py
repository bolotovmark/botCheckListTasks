from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.admin_panel import *

from database.methods import db_get_list_types_event

from keyboards import Keyboards


async def start_form_AddNewEvent(message: types.Message):
    await FormAddNewEvent.type_event.set()
    await message.answer("Открыта форма добавления новой задачи", reply_markup=Keyboards.empty_method)
    types_event = await db_get_list_types_event()
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    buf_list = []
    for type_event in types_event:
        buf_list.append(InlineKeyboardButton(f"{type_event[1]}", callback_data=f"{type_event[0]}"))

        if int(type_event[0]) % 2 == 0:
            inline_kb_full.row(buf_list[0], buf_list[1])
            buf_list.clear()

    if len(buf_list) != 0:
        inline_kb_full.row(buf_list[0])

    inline_kb_full.add(InlineKeyboardButton("🆕 Указать новый тип для задачи", callback_data="addNewTypeTask"))
    await message.answer("Укажите тип новой задачи c клавиатуры:", reply_markup=inline_kb_full)


async def start_form_AddNewTypeTask(message: types.Message, callback_query: types.CallbackQuery):
    await FormAddNewTypeTask.name.set()
    await message.answer("Введите название для нового типа:", reply_markup=Keyboards.non_auth)


async def process_get_new_type(message: types.Message):



async def process_get_type(callback_query: types.CallbackQuery):
    await callback_query.answer(callback_query.data)


async def process_add_new_type_event(message: types.Message):
    pass


async def process_add_new_type_event_invalid(message: types.Message):
    pass


def register_handlers_add_new_event(dp: Dispatcher):
    dp.register_message_handler(start_form_AddNewEvent,
                                content_types=['text'],
                                text='Добавить новую задачу',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(process_get_type,
                                       lambda c: c.data.isdigit(),
                                       state=FormAddNewEvent.type_event)

    dp.register_callback_query_handler(start_form_AddNewTypeTask,
                                       lambda c: c.data == "addNewTypeTask",
                                       state=FormAddNewEvent.type_event)

    dp.register_message_handler(process_get_new_type,
                                state=FormAddNewTypeTask.name)