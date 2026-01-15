from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

user_commands = {
    "uz": {
        "my_tasks": "📋 Mening vazifalarim",
        "new_tasks": "🆕 Yangi vazifalar",
        "in_progress": "⏳ Jarayondagi vazifalar",
        "done": "✅ Bajarilgan vazifalar",
        "my_profile": "👤 Mening profilim"
    },

    "ru": {
        "my_tasks": "📋 Мои задачи",
        "new_tasks": "🆕 Новые задачи",
        "in_progress": "⏳ Задачи в процессе",
        "done": "✅ Завершённые задачи",
        "my_profile": "👤 Мой профиль"
    }
}

def get_user_kb(lang: str="uz") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for key, value in user_commands[lang].items():

        builder.button(
            text=value,
            callback_data=key
        )

    builder.adjust(2)
    return builder.as_markup()