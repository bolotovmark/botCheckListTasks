from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.admin_panel import FormWathcListEvent, FormChangeTasks

from database.methods import db_get_list_events


async def start_form_watchListEvents(message: types.Message):
    list_events = await db_get_list_events()
    if list_events:
        type_event = list_events[0][1]
        out_text = f"*---{list_events[0][1]}---*\n\n\n"
        for event in list_events:
            if event[1] != type_event:
                type_event = event[1]
                await message.answer(out_text, parse_mode="Markdown")
                out_text = f"*---{event[1]}---*\n\n\n"
            out_text = out_text + f"Задача: *{event[0]}*\n" \
                                  f"------------------------------\n"
        await message.answer(out_text, parse_mode="Markdown")
    else:
        await message.answer("⚠️Задач в базе нет!")


def register_handlers_list_events(dp: Dispatcher):

    dp.register_message_handler(start_form_watchListEvents,
                                content_types=['text'],
                                text='Cписок задач',
                                state=FormChangeTasks.menu)
