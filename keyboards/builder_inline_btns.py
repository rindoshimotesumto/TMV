from typing import Iterable

import aiosqlite
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from answers_template import ANSWERS
from keyboards.tasks import BTN_TEXTS, ROLE_BUTTONS
from logger.logger import write_logs


def build_menu_kb(role: str = "user", lang: str = "uz") -> InlineKeyboardMarkup | None:
    """
    Генерирует клавиатуру меню по роли пользователя.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: tuple = ROLE_BUTTONS.get(role, ROLE_BUTTONS["user"])

    try:
        for btn in btns:
            builder.button(text=BTN_TEXTS[btn][lang], callback_data=btn)

        builder.adjust(2)
        return builder.as_markup()

    except Exception as e:
        write_logs(f"[ERROR]: keyboards/builder_inline_btns.py | build_menu_kb() | {e}")
        return None


def build_tasks_kb(
    tasks: Iterable[aiosqlite.Row], lang: str = "uz"
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Генерирует клавиатуру задач.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    answer: str = ANSWERS["tasks"]["not_tasks"][lang]

    try:
        for t in tasks:
            builder.button(
                text=f"{BTN_TEXTS['task'][lang]}{t['task_id']}",
                callback_data=f"task_n:{t['task_id']}",
            )

            builder.adjust(1)
            answer = ANSWERS["tasks"]["tasks"][lang]

    except Exception as e:
        write_logs(
            f"[ERROR]: keyboards/builder_inline_btns.py | build_tasks_kb() | {e}"
        )

    finally:
        builder.row(
            InlineKeyboardButton(
                text=f"{BTN_TEXTS['back_to_menu'][lang]}", callback_data="back_to_menu"
            ),
            width=1,
        )

        return answer, builder.as_markup()
