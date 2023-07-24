from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.methods import db_get_list_types_event, db_get_list_events_type


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
    menu_change_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_change_user.add(types.InlineKeyboardButton(text="Список пользователей"))
    menu_change_user.add(types.InlineKeyboardButton(text="Добавить"))
    menu_change_user.add(types.InlineKeyboardButton(text="Удалить"))
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
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        buf_list = []
        i: int
        i = 0
        for event in events:
            i = i + 1
            buf_list.append(InlineKeyboardButton(f"{event[1]}", callback_data=f"{event[0]}"))

            if i % 2 == 0:
                inline_kb_full.row(buf_list[0], buf_list[1])
                buf_list.clear()

        if len(buf_list) != 0:
            inline_kb_full.row(buf_list[0])
        # inline_kb_full.add(InlineKeyboardButton("↩️ Вернуться к выбору типа", callback_data="back"))
        return inline_kb_full
    else:
        return None

