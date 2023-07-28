from aiogram.dispatcher.filters.state import State, StatesGroup


# Main
class EmployeePanel(StatesGroup):
    menu = State()


# EmployeePanel
class FormNavigateScheduleTasks(StatesGroup):
    select_offset = State()
    navigate = State()


# EmployeePanel
class FormMarkDailyTask(StatesGroup):
    select_offset = State()
    select_task_id = State()
    select_mark = State()
    description = State()


