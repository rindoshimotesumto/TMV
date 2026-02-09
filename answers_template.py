alphaADMIN = "https://t.me/rindoshimotesumto"

ANSWERS: dict[str, dict[str, dict[str, str]]] = {
    "login": {
        "login_success": {
            "ru": "Вы успешно вошли в систему ✅",
            "uz": "Siz tizimga muvaffaqiyatli kirdingiz ✅",
        },
        "login_failed": {
            "ru": "Я вас не узнал ❌\nОбратитесь к администратору 👨‍💻",
            "uz": "Men sizni tanimadim ❌\nAdministratorga murojaat qiling 👨‍💻",
        },
        "wrong_password": {
            "ru": "Неверный пароль ⚠️", 
            "uz": "Noto'g'ri parol ⚠️"
        },
        "wrong_pin": {
            "ru": "Неверный ЖШШИР ⚠️",
            "uz": "Noto'g'ri JSHSHIR ⚠️"
        },
        "input_pin": {
            "ru": "Введите свой ЖШШИР ✍️",
            "uz": "O'z JSHSHIR -gizni kiriting ✍️",
        },
        "input_password": {
            "ru": "Введите пароль 🔐 (8–64 символа)",
            "uz": "Parolingizni kiriting 🔐 (8–64 belgi)",
        },
    },
    
    "tasks": {
        "tasks": {
            "ru": "Ваши задачи 🗂",
            "uz": "Sizning vazifalaringiz 🗂"
        },
        "my_tasks": {
            "ru": "📭 У вас пока нет задач",
            "uz": "📭 Sizda hali vazifalar yo‘q",
        },
        "in_progress": {
            "ru": "📭 Нет задач в процессе",
            "uz": "📭 Jarayonda vazifalar yo‘q",
        },
        "completed": {
            "ru": "📭 Нет выполненных задач",
            "uz": "📭 Bajarilgan vazifalar yo‘q",
        },
        "canceled": {
            "ru": "📭 Нет отменённых задач",
            "uz": "📭 Bekor qilingan vazifalar yo‘q",
        },
        "overdue": {
            "ru": "📭 Нет просроченных задач",
            "uz": "📭 Muddati o‘tgan vazifalar yo‘q",
        }
    }
}


ERRORS = {
    "telegram_id_not_found": {
        "ru": "Не удалось получить ID Telegram аккаунта!",
        "uz": "Telegram akkaunt ID sini aniqlab bo‘lmadi!",
    }
}


LOCKS = {
    "too_many_attempts": {
        "ru": "⛔ Слишком много попыток ввода.\nПопробуйте снова через {minutes} мин.",
        "uz": "⛔ Juda ko‘p urinishlar qilindi.\n{minutes} daqiqadan keyin qayta urinib ko‘ring."
    }
}
