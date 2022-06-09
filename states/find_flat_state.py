from aiogram.dispatcher.filters.state import StatesGroup, State


class FindFlatState(StatesGroup):
    # start_find = State()
    district = State()
    params = State()
    end = State()
