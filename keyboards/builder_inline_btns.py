from typing import Iterable

import aiosqlite
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from answers_template import ANSWERS
from keyboards.tasks import BTN_TEXTS, ROLE_BUTTONS
from logger.logger import write_logs


def build_menu_kb(role: str = "user", lang: str = "uz") -> InlineKeyboardMarkup | None:
    """
    Генерирует клавиатуру меню по роли пользователя.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: set | None = ROLE_BUTTONS.get(role)

    if not btns:
        return None

    try:
        for btn in btns:
            builder.button(text=BTN_TEXTS[btn][lang], callback_data=btn)

        builder.adjust(2)
        return builder.as_markup()

    except Exception as e:
        write_logs(f"[ERROR]: keyboards/builder_inline_btns.py | build_menu_kb() | {e}")
        return None


def build_tasks_kb(lang: str, tasks: Iterable[aiosqlite.Row]) -> tuple[str, InlineKeyboardMarkup] | None:
    """
    Генерирует inline-клавиатуру со списком задач пользователя.
    """

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: Iterable[aiosqlite.Row] | None = tasks
    no_tasks: str = ANSWERS["tasks"]["not_tasks"][lang]

    # если список задач пуст — возвращаем локализованный текст об отсутствии задач
    if not btns:
        no_tasks = ANSWERS["tasks"]["tasks"][lang]

        builder.button(
            text=BTN_TEXTS["back_to_menu"][lang], callback_data="back_to_menu"
        )

        return no_tasks, builder.as_markup()

    # если задачи есть — формируем кнопки задач и кнопку возврата в меню
    try:
        for btn in btns:
            builder.button(
                text=f"{BTN_TEXTS['task'][lang]}",
                callback_data=f"task_id:{btn['task_id']}",
            )

        # размещаем кнопки по одной в строке и собираем markup
        builder.adjust(1)
        builder.button(
            text=BTN_TEXTS["back_to_menu"][lang], callback_data="back_to_menu"
        )

        return no_tasks, builder.as_markup()

    # при любой ошибке сборки клавиатуры — пишем лог и возвращаем None
    except Exception as e:
        write_logs(
            f"[ERROR]: keyboards/builder_inline_btns.py | build_tasks_list() | {e}"
        )
        
        return None
