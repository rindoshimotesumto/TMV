from types import CoroutineType
from typing import Any, Iterable, Optional

import aiosqlite
from aiosqlite import Row

from database.database import DataBase
from logger.logger import write_logs


async def create_users_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (                          -- создаём таблицу users, если её ещё нет

                id INTEGER PRIMARY KEY AUTOINCREMENT,                   -- внутренний авто-инкрементный ID (PK)

                tg_id INTEGER NOT NULL UNIQUE,                          -- Telegram ID пользователя, обязателен и уникален

                role TEXT
                    CHECK (role IN ('admin', 'user', 'superadmin'))
                    DEFAULT 'user',                                     -- роль пользователя с ограничением допустимых значений

                lang TEXT
                    CHECK (lang IN ('uz', 'ru', 'en'))
                    DEFAULT 'uz',                                       -- язык интерфейса пользователя

                pin_code TEXT NOT NULL UNIQUE,                          -- PIN/идентификатор входа, уникальный (используется для логина)

                password TEXT NOT NULL
                    CHECK (8 <= LENGTH(password) <= 64),                -- пароль (длина ограничена на уровне БД)

                position_id INTEGER NOT NULL,                           -- ссылка на должность (таблица positions)

                surname TEXT NOT NULL,                                  -- фамилия
                last_name TEXT NOT NULL,                                -- имя
                middle_name TEXT NOT NULL,                              -- отчество

                date_of_birth DATE NOT NULL,                            -- дата рождения

                phone_number TEXT UNIQUE,                               -- номер телефона (уникальный, но может быть NULL)

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,                          -- дата создания записи

                updated_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,                          -- дата последнего обновления (надо обновлять триггером/кодом)

                works INTEGER DEFAULT 1,                                -- флаг активности (1 = работает, 0 = отключён)

                FOREIGN KEY (position_id)
                    REFERENCES positions(id)
                    ON DELETE RESTRICT                                  -- нельзя удалить должность, если есть пользователи
                    ON UPDATE CASCADE                                   -- при изменении id должности — обновится здесь
            );
        """)

    except Exception as e:
        write_logs(f"⚠️ TABLE users ERROR: {e}")  # логируем ошибку создания таблицы
        raise  # пробрасываем ошибку выше


async def get_info_of_user(
    db: DataBase, tg_id: int, pin_code: Optional[str] = None
) -> Optional[Row] | None:
    try:
        # базовый SELECT: берём только то, что нужно для авторизации/кэша
        sql: str = """
        SELECT id, lang, role FROM users
        """

        # по умолчанию ищем по tg_id
        _: str = " WHERE tg_id = ?;"

        params: list = []

        # если pin_code не передали — ищем по tg_id
        if pin_code is None:
            params.append(tg_id)

        # иначе ищем по pin_code (тут tg_id вообще игнорируется)
        else:
            _ = " WHERE pin_code = ?;"
            params.append(pin_code)

        # собираем финальный SQL
        sql += _

        # выполняем и берём одну строку
        user = await db.execute(query=sql, params=tuple(params), fetchone=True)

        write_logs("CALL: database/tables/users.py | get_info_of_user() | ✅")
        return user

    except Exception as e:
        write_logs(f"[ERROR]: database/tables/users.py | get_info_of_user() | {e}")
        return None


async def get_user_account_password(
    db: DataBase, tg_id: int, pin_code: Optional[str] = None
) -> Optional[Row] | None:
    try:
        # берём только password
        sql: str = """
        SELECT password FROM users
        """

        # по умолчанию фильтруем по tg_id
        _: str = " WHERE tg_id = ?;"

        params: list = []

        # если pin_code не передали — ищем по tg_id
        if pin_code is None:
            params.append(tg_id)

        # иначе ищем по pin_code (tg_id игнорится)
        else:
            _ = " WHERE pin_code = ?;"
            params.append(pin_code)

        # собираем финальный SQL
        sql += _

        # выполняем и берём одну строку
        user = await db.execute(query=sql, params=tuple(params), fetchone=True)

        write_logs("CALL: /database/tables/users.py | get_user_account_password() | ✅")
        return user

    except Exception as e:
        write_logs(
            f"[ERROR]: database/tables/users.py | get_user_account_password() | {e}"
        )
        return None
