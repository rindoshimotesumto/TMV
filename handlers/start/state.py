from aiogram.fsm.state import State, StatesGroup


class SignIn(StatesGroup):
    pin_code = State()
    password = State()
