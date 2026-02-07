from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from answers_template import ANSWERS, ERRORS
from handlers.start.state import SignIn
from keyboards.builder_inline_btns import build_menu_kb

router = Router()  # роутер для хендлера /start


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, cache_user: dict):
    await state.clear()  # очищаем FSM состояние (сбрасываем любые прошлые шаги/данные)

    if not message.from_user:
        # защита: если Telegram не прислал объект пользователя
        await message.answer(text=ERRORS["telegram_id_not_found"]["uz"])
        return

    if cache_user:
        # если пользователь уже есть в кэше — считаем что он залогинен
        # отправляем сообщение об успешном входе и главное меню по роли
        await message.answer(
            text=ANSWERS["login"]["login_success"][cache_user["lang"]],
            reply_markup=build_menu_kb(cache_user["role"], cache_user["lang"]),
        )
        return  # прекращаем выполнение, чтобы не переходить к вводу PIN

    # если пользователя нет в кэше — начинаем сценарий логина
    # просим ввести PIN (без обращения к БД на /start)
    await message.answer(ANSWERS["login"]["input_pin"]["uz"])

    # переводим FSM в состояние ожидания PIN-кода
    await state.set_state(SignIn.pin_code)
