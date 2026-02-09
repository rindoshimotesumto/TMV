from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from answers_template import ANSWERS

from database.database import DataBase
from database.tables.tasks import get_users_task_by_tg_id

from handlers.utils.to_login import to_login_user

from keyboards.builder_inline_btns import build_menu_kb, build_tasks_kb
from keyboards.tasks import ROLE_BUTTONS

router = Router()
db = DataBase()


async def send_or_edit(
    call: CallbackQuery,
    text: str,
    reply_markup=None) -> None:
    """
        Универсальный helper для callback-хендлеров меню.
    
        Пытается отредактировать текущее сообщение (меню),
        если Telegram не разрешает редактирование — отправляет новое сообщение.
    
        Используется для:
        - меню задач
        - возврата в главное меню
        - списков задач по статусам
    
        Это позволяет не дублировать try/except в каждом handler.
    """
    if not call.message:
        return

    try:
        # Пытаемся обновить текущее сообщение (inline-меню)
        await call.message.edit_text(text=text, reply_markup=reply_markup)

    except Exception:
        # Если редактирование невозможно (старое сообщение / ограничение Telegram)
        # — отправляем новое сообщение с тем же содержимым
        await call.message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(F.data.in_(ROLE_BUTTONS["user"]))
async def call_of_user_btns(
    call: CallbackQuery,
    state: FSMContext,
    cache_user: dict | None = None
):
    """
        Обработчик пользовательских кнопок раздела задач.
    
        Срабатывает на callback_data из ROLE_BUTTONS["user"].
        Ожидается, что call.data — это статус задач:
            my_tasks / in_progress / completed / overdue / и т.д.
    
        Логика:
        - подтверждаем callback (убираем "часики" в Telegram)
        - если пользователь есть в cache_user → загружаем задачи из БД
        - строим клавиатуру задач
        - обновляем текущее меню (edit) или отправляем новое (fallback)
        - если пользователь не авторизован → переводим в login-flow
    """
    await call.answer()

    if not call.message:
        return
    
    # cache_user приходит из CacheUserMiddleware
    if cache_user:
        # Получаем задачи пользователя по tg_id/db_id и статусу (call.data)
        tasks = await get_users_task_by_tg_id(db, cache_user["db_id"], call.data)
        
        # Строим текст + inline клавиатуру списка задач
        answer, kb = build_tasks_kb(tasks, call.data, cache_user["lang"])
        
        # Пытаемся обновить текущее сообщение меню
        await send_or_edit(call, answer, kb)
        return

    # Если пользователя нет в кеше — отправляем в процедуру логина
    await to_login_user(call, state)


@router.callback_query(F.data == "back_to_menu")
async def call_of_back_to_menu(
    call: CallbackQuery,
    state: FSMContext,
    cache_user: dict | None = None
):
    """
        Обработчик кнопки "back_to_menu".
    
        Логика:
        - подтверждаем callback
        - если пользователь авторизован (есть cache_user):
            показываем главное меню по роли и языку
        - если нет:
            переводим в login-flow (ввод PIN)
    """
    await call.answer()

    if not call.message:
        return

    if cache_user:
        # Текст успешного входа / возврата в меню
        answer = ANSWERS["login"]["login_success"][cache_user["lang"]]
        
        # Главное меню строится на основе роли пользователя
        kb = build_menu_kb(cache_user["role"], cache_user["lang"])
        
        # Обновляем текущее меню или отправляем новое
        await send_or_edit(call, answer, kb)
        return

    # Не авторизован — отправляем в login-flow
    await to_login_user(call, state)