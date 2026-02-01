from aiogram.fsm.state import State, StatesGroup


class LoginUser(StatesGroup):
    pin_code = State()
    password = State()
    lang = State()
    role = State()
