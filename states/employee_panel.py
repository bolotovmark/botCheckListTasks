from aiogram.dispatcher.filters.state import State, StatesGroup


# Main
class EmployeePanel(StatesGroup):
    menu = State()


# EmployeePanel
class FormNavigateScheduleTasks(StatesGroup):
    menu = State()
