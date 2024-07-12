from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    fullname = State()
    phone = State()
    description = State()