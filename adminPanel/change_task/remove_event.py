from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from states.admin_panel import FormChangeTasks, FormRemoveEvent

from keyboards import Keyboards, kb_types_events, kb_events, kb_book_events
from database.methods import db_remove_event, db_get_list_events_type


async def start_form_removeEvent(message: types.Message, state: FSMContext):
    await FormRemoveEvent.select_type.set()
    async with state.proxy() as data:
        data['page'] = 0
    await message.answer("Открыта форма удаления задач", reply_markup=Keyboards.empty_method)

    await message.answer("Укажите, по какому типу хотите посмотреть задачи", reply_markup=await kb_types_events())


async def process_select_type(callback_query: types.CallbackQuery, state: FSMContext):
    type_id: str
    offset: int
    async with state.proxy() as data:
        data['type_id'] = callback_query.data
        type_id = data['type_id']
        offset = data['page']
    await FormRemoveEvent.select_id.set()

    list_events_type = await db_get_list_events_type(callback_query.data)
    bot = callback_query.bot
    out_text = f'🔹*{list_events_type[0][5]}*\n\n'
    if list_events_type:
        name_group = list_events_type[0][3]
        if name_group is None:
            out_text = out_text + "*🔘|Без группы|*\n"
        else:
            out_text = out_text + f"*🔘|{name_group}|*\n"
        i = 0
        for task in list_events_type:
            i = i + 1
            if name_group != task[3]:
                i = 1
                name_group = task[3]
                out_text = out_text + f"\n*🔘|{name_group}|*\n"
            out_text = out_text + f"{i}. *{task[1]}*\n"

    else:
        out_text = "⚠️Задач такого типа в базе нет!"
    bot = callback_query.bot
    await bot.edit_message_text(
        text=f"{out_text} \nВыберите задачу, которую нужно удалить:",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_book_events(type_id, offset),
        parse_mode="Markdown"
    )


async def process_select_id(callback_query: types.CallbackQuery, state: FSMContext):
    id_task = callback_query.data
    await db_remove_event(id_task)
    async with state.proxy() as data:
        callback_query.data = data['type_id']
    return await process_select_type(callback_query, state)


async def process_next_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) + 5
        callback_query.data = data['type_id']
    return await process_select_type(callback_query, state)


async def process_back_page(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = int(data['page']) - 5
        callback_query.data = data['type_id']
    return await process_select_type(callback_query, state)


async def process_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    return await start_form_removeEvent(callback_query.message, state)


def register_handlers_remove_event(dp: Dispatcher):
    dp.register_message_handler(start_form_removeEvent,
                                content_types=['text'],
                                text='Удалить задачу',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(process_select_type,
                                       lambda c: c.data.isdigit(),
                                       state=FormRemoveEvent.select_type)

    dp.register_callback_query_handler(process_select_id,
                                       lambda c: c.data.isdigit(),
                                       state=FormRemoveEvent.select_id)

    dp.register_callback_query_handler(process_next_page,
                                       lambda c: c.data == "next",
                                       state=FormRemoveEvent.select_id)

    dp.register_callback_query_handler(process_back_page,
                                       lambda c: c.data == "back",
                                       state=FormRemoveEvent.select_id)

    dp.register_callback_query_handler(process_back_to_menu,
                                       lambda c: c.data == "back_to_menu",
                                       state=FormRemoveEvent.select_id)

