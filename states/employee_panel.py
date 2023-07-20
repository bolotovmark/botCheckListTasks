from aiogram.dispatcher.filters.state import State, StatesGroup

class EmployeePanel(StatesGroup):
    menu = State()