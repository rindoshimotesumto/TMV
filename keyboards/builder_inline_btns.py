from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.tasks import BTN_TEXTS, ROLE_BUTTONS
from logger.logger import write_logs


def build_menu_kb(role: str = "user", lang: str = "uz") -> InlineKeyboardMarkup | None:
    """
    Генерирует клавиатуру меню по роли пользователя.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: tuple | None = ROLE_BUTTONS.get(role)

    if btns:
        for btn in btns:
            builder.button(text=BTN_TEXTS[btn][lang], callback_data=btn)

    else:
        write_logs("[ERROR]: keyboards/builder_inline_btns.py | build_menu_kb()")
        return

    builder.adjust(2)
    return builder.as_markup()
