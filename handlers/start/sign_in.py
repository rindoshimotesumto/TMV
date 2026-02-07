from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from answers_template import ANSWERS, ERRORS
from handlers.services.anti_brute_force import register_fail, reset_fails
from handlers.services.auntificate import auntificate, check_password
from handlers.start.state import SignIn
from keyboards.builder_inline_btns import build_menu_kb

router = Router()  # роутер aiogram для регистрации хендлеров логина


@router.message(SignIn.pin_code)
async def write_pin_code(message: Message, state: FSMContext, cache_user: dict | None):
    # хендлер шага FSM: ввод PIN-кода

    if not message.from_user:
        # защита: если Telegram не прислал пользователя
        await message.answer(text=ERRORS["telegram_id_not_found"]["uz"])
        return

    tg_id = message.from_user.id                            # Telegram ID пользователя
    lang = (cache_user or {}).get("lang", "uz")             # язык из кэша (или дефолт)

    pin_txt = (message.text or "").strip()                  # текст PIN без пробелов

    # проверка формата PIN (14 цифр)
    if not (len(pin_txt) == 14 and pin_txt.isdigit()):
        register_fail(tg_id)                                # регистрируем неудачную попытку
        await message.answer(ANSWERS["login"]["wrong_pin"][lang])
        return

    pin_code = int(pin_txt)                                 # приводим PIN к int
    answer, user = await auntificate(tg_id, pin_code)       # пробуем найти пользователя

    if user is None:
        # если пользователь не найден — считаем как fail
        register_fail(tg_id)
        await message.answer(answer)                        # текст login_failed
        return

    # сохраняем PIN во временные данные FSM
    await state.update_data(pin_code=pin_code)

    # переключаем FSM на шаг ввода пароля
    await state.set_state(SignIn.password)

    # просим ввести пароль
    await message.answer(ANSWERS["login"]["input_password"][lang])


@router.message(SignIn.password)
async def write_password(message: Message, state: FSMContext, cache_user: dict | None):
    # хендлер шага FSM: ввод пароля

    if not message.from_user:
        # защита: нет from_user
        await message.answer(text=ERRORS["telegram_id_not_found"]["uz"])
        return

    if message.text is None:
        # если пришло не текстовое сообщение — ошибка попытки
        register_fail(message.from_user.id)
        await message.answer(text=ANSWERS["login"]["wrong_password"]["uz"])
        return

    tg_id = message.from_user.id
    lang = (cache_user or {}).get("lang", "uz")     # язык пользователя

    password = (message.text or "").strip()         # пароль без пробелов

    # проверка длины пароля
    if not (8 <= len(password) <= 64):
        register_fail(tg_id)                        # считаем fail
        await message.answer(ANSWERS["login"]["wrong_password"][lang])
        return

    # берём данные FSM (там сохранён pin_code)
    data = await state.get_data()
    pin_code = data.get("pin_code")

    # проверяем пароль через сервис
    ok = await check_password(tg_id, password, pin_code)

    if not ok:
        # неверный пароль — fail
        register_fail(tg_id)
        await message.answer(ANSWERS["login"]["wrong_password"][lang])
        return

    # успех — сбрасываем счётчик анти- бутфорс
    reset_fails(tg_id)

    # повторная авторизация (теперь уже из кэша — быстро)
    answer, user = await auntificate(tg_id)

    # отправляем сообщение успеха + меню по роли
    await message.answer(
        answer,
        reply_markup=build_menu_kb(user["role"], user["lang"])
    )

    # очищаем FSM состояние (выход из сценария логина)
    await state.clear()
