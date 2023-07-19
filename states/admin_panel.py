from aiogram.dispatcher.filters.state import State, StatesGroup


# 1
class AdminPanel(StatesGroup):
    menu = State()


# 2
class FormChangeListUsers(StatesGroup):
    menu = State()


# 3
class FormAddNewUser(StatesGroup):
    id = State()
    position_name = State()
    name = State()
    position_id = 0


# 4
class FormRemoveUser(StatesGroup):
    id = State()
    check = State()