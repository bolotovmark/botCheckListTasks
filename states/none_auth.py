from aiogram.dispatcher.filters.state import State, StatesGroup


class NoneAuth(StatesGroup):
    start = State()
