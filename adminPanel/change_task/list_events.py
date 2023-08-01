from aiogram import Dispatcher, types

from states.admin_panel import FormWatchListEvent, FormChangeTasks

from database.methods import db_get_list_events, db_get_list_types_event, db_get_list_events_type

from keyboards import Keyboards, kb_types_events


async def start_form_watchListEvents(message: types.Message):
    await FormWatchListEvent.menu.set()
    await message.answer("Открыта форма просмотра списка задач", reply_markup=Keyboards.empty_method)

    await message.answer("Укажите, по какому типу хотите посмотреть задачи", reply_markup=await kb_types_events())


async def watch_events(callback_query: types.CallbackQuery):
    list_events_type = await db_get_list_events_type(callback_query.data)
    bot = callback_query.bot
    out_text = ''
    if list_events_type:
        out_text = out_text + f"---{list_events_type[0][5]}---\n\n"
        for event in list_events_type:
            out_text = out_text + f"Задача: *{event[1]}*\n" \
                                  f"------------------------------\n"
    else:
        out_text = "⚠️Задач такого типа в базе нет!"
    await bot.edit_message_text(
        text=out_text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_types_events(),
        parse_mode="Markdown"
    )


def register_handlers_list_events(dp: Dispatcher):
    dp.register_message_handler(start_form_watchListEvents,
                                content_types=['text'],
                                text='Cписок задач',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(watch_events,
                                       lambda c: c.data.isdigit(),
                                       state=FormWatchListEvent.menu)
