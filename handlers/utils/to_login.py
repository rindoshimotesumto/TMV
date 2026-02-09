from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from answers_template import ANSWERS
from handlers.start.state import SignIn

async def to_login_user(call: CallbackQuery, state: FSMContext) -> None:
    """
        Перевод пользователя в login-flow.
    
        Используется в callback-хендлерах, когда:
        - cache_user отсутствует
        - пользователь не найден в кеше
        - требуется повторная авторизация
    
        Действия:
        - отправляет сообщение с просьбой ввести PIN
        - переводит FSM в состояние ожидания PIN-кода
    """

    await call.message.answer(ANSWERS["login"]["input_pin"]["uz"])
    await state.set_state(SignIn.pin_code)