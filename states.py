from aiogram.dispatcher.filters.state import State, StatesGroup


# 3
class FormChangeTypesTask(StatesGroup):
    menu = State()
    name = State()
    delete = State()
    list = State()


# 1
class EmployeePanel(StatesGroup):
    menu = State()

############ Изменение списка пользователей
