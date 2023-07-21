from aiogram import types


class Keyboards:
    ###
    position = types.ReplyKeyboardMarkup(resize_keyboard=True)
    position.add(types.InlineKeyboardButton(text="Администратор"))
    position.add(types.InlineKeyboardButton(text="Рабочий"))
    position.add(types.InlineKeyboardButton(text="Отменить и вернуться в панель управления"))
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
    empty_method.add(types.InlineKeyboardButton(text="Отменить и вернуться в панель управления"))
    ###

    ###
    menu_change_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_change_user.add(types.InlineKeyboardButton(text="Список пользователей"))
    menu_change_user.add(types.InlineKeyboardButton(text="Добавить"))
    menu_change_user.add(types.InlineKeyboardButton(text="Удалить"))
    menu_change_user.add(types.InlineKeyboardButton(text="Вернуться в главное меню"))
    ###

    ###
    list_types = types.ReplyKeyboardMarkup(resize_keyboard=True)
    list_types.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    list_types.add(types.InlineKeyboardButton(text="Cписок задач"))
    #list_types.add(types.InlineKeyboardButton(text="Удалить тип"))
    list_types.add(types.InlineKeyboardButton(text="Вернуться в главное меню"))
    ###

    ###
    bool = [
        [
            types.KeyboardButton(text="✅"),
            types.KeyboardButton(text="❌")
        ],
    ]
    boolean_keyboard = types.ReplyKeyboardMarkup(keyboard=bool, resize_keyboard=True)
    boolean_keyboard.add(types.InlineKeyboardButton(text="Отменить и вернуться в панель управления"))
    ###

    ###
    add_new_type_task = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_new_type_task.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    add_new_type_task.add(types.InlineKeyboardButton(text="Добавить новую задачу"))
    ###
