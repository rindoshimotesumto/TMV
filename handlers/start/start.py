from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.database import DataBase
from handlers.start.login_user_state import LoginUser
from handlers.template_of_answers.answers import ANSWERS, ERRORS
from keyboards.builder_inline_btns import build_menu_kb

from .login_user import login_user

router = Router()
db = DataBase()


# обработка команды /start
# будем пытатся логинить юзера по кешу, не получится, то по базе
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    status, answer, lang, role, password = await login_user(message.from_user.id)

    if not status:
        await message.answer(text=answer)
        await state.set_state(LoginUser.pin_code)
    else:
        await message.answer(text=answer, reply_markup=build_menu_kb(role, lang))


# после получение pin_code, ищем юзера в кешах и бд
# если в кешах, то мы получаем инфу с кешов
# если в бд, то мы сохраняем в кеш а после возвращаем данные (status, answer, lang, role, password)
@router.message(LoginUser.pin_code)
async def input_pin(message: Message, state: FSMContext):
    # если не текст говорим об этом
    if not message.text:
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # убираем пустоту, в случае другого типа сообщение говорим что принимиаем только текст
    pin_code: str = (message.text or "").strip()

    # мало-ли ошибка какая
    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    # проверим на валидность\корректность
    if not (pin_code.isdigit() and len(pin_code) == 14):
        await message.answer(ANSWERS["login"]["wrong_pin"]["uz"])
        return

    # status: результат функции
    # answer: текст который мы передадим юзеру
    # lang|role: язык и роль юзера, дефолт= uz|user
    # password: нужен что-бы уменшить кол-во запросов в бд
    status, answer, lang, role, password = await login_user(
        message.from_user.id, pin_code
    )

    # если юзера нет в кешах и даже в бд, то говорим что-бы помог админ
    if status is False:
        await message.answer(text=answer)
        await state.clear()
        return

    # если нашел храним данные в state и переходим к получение password
    await message.answer(ANSWERS["login"]["input_password"]["uz"])

    await state.update_data(pin_code=pin_code, password=password, lang=lang, role=role)
    await state.set_state(LoginUser.password)


# после получение password, сравниваем пароли, True -> меню, False -> попробуй ещё раз
@router.message(LoginUser.password)
async def input_password(message: Message, state: FSMContext):
    # если не текст говорим об этом
    if not message.text:
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # убираем пустоту
    input_password: str = (message.text or "").strip()

    # мало-ли ошибка какая
    if not message.from_user:
        await message.answer(ERRORS["telegram_id_not_found"]["uz"])
        return

    # проверяем длину
    if not (8 <= len(input_password) <= 64):
        await message.answer(ANSWERS["login"]["wrong_password"]["uz"])
        return

    # берем информацию с state
    data: dict = await state.get_data()
    password, lang, role = data["password"], data["lang"], data["role"]

    # проверяем пароль
    if password == input_password:
        await message.answer(
            text=ANSWERS["login"]["login_success"][lang],
            reply_markup=build_menu_kb(role, lang),
        )

        await state.clear()
        return

    # если пароли не совпали говорим об этом!
    else:
        await message.answer(
            text=ANSWERS["login"]["wrong_password"]["uz"],
        )

        return
