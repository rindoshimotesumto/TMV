from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


USER_COMMANDS = {
    "uz": {
        "my_tasks": "📋 Mening vazifalarim",
        "new_tasks": "🆕 Yangi vazifalar",
        "in_progress": "⏳ Jarayondagi vazifalar",
        "done": "✅ Bajarilgan vazifalar",
        "my_profile": "👤 Mening profilim",
    },
    "ru": {
        "my_tasks": "📋 Мои задачи",
        "new_tasks": "🆕 Новые задачи",
        "in_progress": "⏳ Задачи в процессе",
        "done": "✅ Завершённые задачи",
        "my_profile": "👤 Мой профиль",
    }
}

SUPER_ADMIN_COMMANDS = {
    "uz": {
        "manage_organizations": "🏢 Tashkilotlar",
        "manage_branches": "🏬 Filiallar",
        "manage_departments": "🏷 Bo'limlar",
        "manage_positions": "💼 Lavozimlar",
        "manage_users": "👥 Foydalanuvchilar",
        "manage_admins": "🧑‍💻 Adminlar",
        "manage_tasks": "🗂 Vazifalar",
        "stats": "📊 Statistika",
        "settings": "⚙️ Sozlamalar"
    },

    "ru": {
        "manage_organizations": "🏢 Организации",
        "manage_branches": "🏬 Филиалы",
        "manage_departments": "🏷 Отделы",
        "manage_positions": "💼 Должности",
        "manage_users": "👥 Пользователи",
        "manage_admins": "🧑‍💻 Админы",
        "manage_tasks": "🗂 Задачи",
        "stats": "📊 Статистика",
        "settings": "⚙️ Настройки"
    }
}


def build_kb(lang: str = "uz", role: str="user") -> InlineKeyboardMarkup:
    """
    commands -> словарь вида {"uz": {...}, "ru": {...}}
    lang -> язык
    role -> уровень доступа пользователья (user, admin, superadmin)
    """
    builder = InlineKeyboardBuilder()

    commands = USER_COMMANDS

    if role in ["superadmin", "admin"]:
        commands = SUPER_ADMIN_COMMANDS
        
    for cb, text in commands.get(lang, commands["ru"]).items():
        builder.button(text=text, callback_data=cb)

    builder.adjust(2)
    return builder.as_markup()