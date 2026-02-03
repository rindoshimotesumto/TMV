from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from answers_template import ANSWERS, ERRORS
from database.database import DataBase
from handlers.start.login_user_state import LoginUser
from handlers.utils.login_user import login_user
from keyboards.builder_inline_btns import build_menu_kb

router = Router()
db = DataBase()


# /start — очистка состояния и попытка авто-логина пользователя
# сначала проверяем кэш, затем БД
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    # защита от редкого случая отсутствия from_user
    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    # пробуем авторизовать по tg_id (кэш → БД)
    status, answer, lang, role, password = await login_user(message.from_user.id)

    # если не найден — просим PIN
    if not status:
        await message.answer(text=answer)
        await state.set_state(LoginUser.pin_code)

    # если найден — показываем меню
    else:
        await message.answer(text=answer, reply_markup=build_menu_kb(role, lang))


# обработка ввода PIN-кода
# ищем пользователя: сначала кэш, потом БД → при успехе сохраняем данные во FSM
@router.message(LoginUser.pin_code)
async def input_pin(message: Message, state: FSMContext):
    # принимаем только текст
    if not message.text:
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # убираем пробелы
    pin_code = (message.text or "").strip()

    # защита от отсутствия from_user
    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    # PIN должен быть числовым и длиной 14 символов
    if not (pin_code.isdigit() and len(pin_code) == 14):
        await message.answer(ANSWERS["login"]["wrong_pin"]["uz"])
        return

    # login_user вернет:
    # status — найден ли пользователь
    # answer — текст ответа
    # lang / role — язык и роль
    # password — пароль из БД (чтобы не делать второй запрос)
    status, answer, lang, role, password = await login_user(
        message.from_user.id, pin_code
    )

    # если пользователь не найден — сообщаем и выходим
    if status is False:
        await message.answer(text=answer)
        await state.clear()
        return

    # пользователь найден — просим пароль
    await message.answer(ANSWERS["login"]["input_password"]["uz"])

     # сохраняем данные для следующего шага проверки
    await state.update_data(pin_code=pin_code, password=password, lang=lang, role=role)
    await state.set_state(LoginUser.password)


# обработка ввода пароля
# сравниваем введенный пароль с сохраненным → успех = меню, иначе повтор
@router.message(LoginUser.password)
async def input_password(message: Message, state: FSMContext):
    # принимаем только текст
    if not message.text:
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # очищаем ввод
    input_password = (message.text or "").strip()

    # защита от отсутствия from_user
    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    # базовая проверка длины пароля
    if not (8 <= len(input_password) <= 64):
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # получаем сохраненные данные из FSM
    data = await state.get_data()
    password, lang, role = data["password"], data["lang"], data["role"]

    # если пароль совпал — успешный вход
    if password == input_password:
        await message.answer(
            text=ANSWERS["login"]["login_success"][lang],
            reply_markup=build_menu_kb(role, lang),
        )

        await state.clear()
        return

     # если не совпал — ошибка и повтор ввода
    else:
        await message.answer(
            text=ANSWERS["login"]["wrong_password"]["uz"],
        )

        return
