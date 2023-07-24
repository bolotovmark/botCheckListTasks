from aiogram.dispatcher.filters.state import State, StatesGroup


# Main
class AdminPanel(StatesGroup):
    menu = State()


# AdminPanel
class FormChangeListUsers(StatesGroup):
    menu = State()
    # FormAddNewUser
    # FormRemoveUser


# AdminPanel
class FormChangeTasks(StatesGroup):
    menu = State()


#  FormChangeListUsers
class FormAddNewUser(StatesGroup):
    id = State()
    position_name = State()
    name = State()
    position_id = 0


#  FormChangeListUsers
class FormRemoveUser(StatesGroup):
    id = State()
    check = State()


# FormChangeTasks
class FormAddNewEvent(StatesGroup):
    type_event = State()
    name = State()
    group_name = State()


# FormAddNewEvent
class FormAddNewTypeTask(StatesGroup):
    name = State()


# FormChangeTasks
class FormWatchListEvent(StatesGroup):
    menu = State()


# FormChangeTasks
class FormRemoveEvent(StatesGroup):
    select_type = State()
    select_id = State()


# FormChangeTasks
class FormRemoveTypeEvent(StatesGroup):
    select_type = State()


