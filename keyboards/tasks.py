BTN_TEXTS: dict[str, dict[str, str]] = {
    "my_tasks": {"ru": "📋 Мои задачи", "uz": "📋 Mening vazifalarim"},
    "profile": {"ru": "👤 Профиль", "uz": "👤 Profil"},
    "users": {"ru": "👥 Пользователи", "uz": "👥 Foydalanuvchilar"},
    "reports": {"ru": "📊 Отчёты", "uz": "📊 Hisobotlar"},
    "settings": {"ru": "⚙️ Настройки системы", "uz": "⚙️ Tizim sozlamalari"},
    "in_progress": {"ru": "🟡 В процессе", "uz": "🟡 Jarayonda"},
    "completed": {"ru": "✅ Выполненные", "uz": "✅ Tugallangan"},
    "canceled": {"ru": "❌ Отменённые", "uz": "❌ Bekor qilingan"},
    "overdue": {"ru": "⏰ Просроченные", "uz": "⏰ Muddati o‘tgan"},
    "task": {"ru": "🗂 Задача №", "uz": "🗂 Vazifa №"},
    "back_to_menu": {"ru": "◀️", "uz": "◀️"},
}


ROLE_BUTTONS: dict[str, tuple[str, ...]] = {
    "user": ("my_tasks", "in_progress", "completed", "canceled", "overdue", "profile"),
    "admin": ("my_tasks", "users", "reports", "profile"),
    "superadmin": ("my_tasks", "users", "reports", "settings", "profile"),
}
