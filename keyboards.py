from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.methods import db_get_list_types_event, db_get_list_events_type, db_get_list_events_type_offset


class Keyboards:
    ###
    position = types.ReplyKeyboardMarkup(resize_keyboard=True)
    position.add(types.InlineKeyboardButton(text="Администратор"))
    position.add(types.InlineKeyboardButton(text="Рабочий"))
    position.add(types.InlineKeyboardButton(text="↩️ Отменить и вернуться в панель управления"))
    ###

    ###
    menu_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_admin.add(types.InlineKeyboardButton(text="Панель управления пользователями"))
    menu_admin.add(types.InlineKeyboardButton(text="Панель управления задачами"))
    menu_admin.add(types.InlineKeyboardButton(text="Панель управления ежедневным расписанием"))
    ##menu_admin.add(types.InlineKeyboardButton(text="Редактировать список задач"))
    ###

    ###
    non_auth = types.ReplyKeyboardMarkup(resize_keyboard=True)
    non_auth.add(types.InlineKeyboardButton(text="Получить id"))
    ###

    ###
    empty_method = types.ReplyKeyboardMarkup(resize_keyboard=True)
    empty_method.add(types.InlineKeyboardButton(text="↩️ Отменить и вернуться в панель управления"))
    ###

    ###
    data = [
        [
            types.KeyboardButton(text="Добавить"),
            types.KeyboardButton(text="Удалить")
        ],
    ]
    menu_change_user = types.ReplyKeyboardMarkup(keyboard=data, resize_keyboard=True)
    menu_change_user.add(types.InlineKeyboardButton(text="Список пользователей"))
    menu_change_user.add(types.InlineKeyboardButton(text="↩️ Вернуться в главное меню"))
    ###

    ###
    list_types = types.ReplyKeyboardMarkup(resize_keyboard=True)
    list_types.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    list_types.add(types.InlineKeyboardButton(text="Cписок задач"))
    list_types.add(types.InlineKeyboardButton(text="Удалить задачу"))
    list_types.add(types.InlineKeyboardButton(text="Удалить тип задачи"))
    list_types.add(types.InlineKeyboardButton(text="↩️ Вернуться в главное меню"))
    ###

    ###
    add_rem = [
        [
            types.KeyboardButton(text="Добавить задачи"),
            types.KeyboardButton(text="Удалить задачи")
        ],
    ]
    menu_change_schedule_task = types.ReplyKeyboardMarkup(keyboard=add_rem, resize_keyboard=True)
    menu_change_schedule_task.add(types.InlineKeyboardButton(text="Список ежедневных задач"))
    menu_change_schedule_task.add(types.InlineKeyboardButton(text="↩️ Вернуться в главное меню"))
    ###

    ###
    bool = [
        [
            types.KeyboardButton(text="✅"),
            types.KeyboardButton(text="❌")
        ],
    ]
    boolean_keyboard = types.ReplyKeyboardMarkup(keyboard=bool, resize_keyboard=True)
    boolean_keyboard.add(types.InlineKeyboardButton(text="↩️ Отменить и вернуться в панель управления"))
    ###

    ###
    add_new_type_task = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_new_type_task.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    add_new_type_task.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    ###


async def kb_types_events():
    types_event = await db_get_list_types_event()
    if types_event:
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
        return inline_kb_full
    else:
        return None


async def kb_events(type_id):
    events = await db_get_list_events_type(type_id)
    if events:
        inline_kb_full = InlineKeyboardMarkup(row_width=3)
        buf_list = []
        i: int
        i = 0
        for event in events:
            i = i + 1
            buf_list.append(InlineKeyboardButton(f"{event[1]}", callback_data=f"{event[0]}"))

            if i % 3 == 0:
                inline_kb_full.row(buf_list[0], buf_list[1], buf_list[2])
                buf_list.clear()

        if len(buf_list) != 0:
            for but in buf_list:
                inline_kb_full.insert(but)
        # inline_kb_full.add(InlineKeyboardButton("↩️ Вернуться к выбору типа", callback_data="back"))
        return inline_kb_full
    else:
        return None


async def kb_book_events(type_id, offset):
    events = await db_get_list_events_type_offset(type_id, offset)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    if events:


        for event in events:
            inline_kb_full.add(InlineKeyboardButton(f"{event[1]}({event[3]})", callback_data=f"{event[0]}"))

        if offset >= 5:
            inline_kb_full.row(InlineKeyboardButton("⏪Назад", callback_data="back"), InlineKeyboardButton("⏩Вперед", callback_data="next"))
        else:
            inline_kb_full.add(InlineKeyboardButton("⏩Вперед", callback_data="next"))
        # inline_kb_full.add(InlineKeyboardButton("↩️ Вернуться к выбору типа", callback_data="back"))

    else:
        inline_kb_full.add(InlineKeyboardButton("⏪Назад", callback_data="back"))

    return inline_kb_full

