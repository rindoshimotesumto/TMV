from typing import Iterable, Optional

import aiosqlite

from database.database import DataBase
from logger.logger import write_logs


async def create_tasks_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (                                      -- создаём таблицу задач, если ещё не существует

                id INTEGER PRIMARY KEY AUTOINCREMENT,                               -- внутренний авто-инкрементный ID задачи

                tg_audio_file_id TEXT NOT NULL,                                     -- file_id голосового сообщения в Telegram
                audio_text TEXT NOT NULL,                                           -- распознанный текст аудио

                status TEXT
                    CHECK (status IN (
                        'new', 'in_progress', 'completed', 'canceled', 'overdue'
                    ))
                    DEFAULT 'new',                                                  -- статус задачи с ограничением допустимых значений

                user_id INTEGER NOT NULL,                                           -- владелец задачи (FK → users.id)

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,                                      -- время создания задачи

                updated_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,                                      -- время последнего обновления (обновлять кодом/триггером)

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE RESTRICT                                              -- нельзя удалить пользователя, если есть задачи
                    ON UPDATE CASCADE                                               -- при изменении id пользователя — обновится здесь
            );
        """)

    except Exception as e:
        write_logs(f"⚠️ TABLE tasks ERROR: {e}")  # логируем ошибку создания таблицы
        raise  # пробрасываем ошибку выше


async def get_users_task_by_tgID(
    db: DataBase, user_id: int, status: Optional[str] = None
) -> Iterable[aiosqlite.Row] | None:
    """
    Возвращает список задач пользователя.
    Если передан статус — фильтрует по статусу,
    иначе — возвращает все задачи пользователя.
    """
    try:
        # базовый SELECT — берём поля задачи + связь назначений
        sql: str = """
        SELECT
            t_ass.user_id,            -- ID пользователя-исполнителя
            t.audio_text,             -- текст задачи
            t.tg_audio_file_id,       -- Telegram file_id аудио
            t_ass.task_id             -- ID задачи

        FROM tasks t
        JOIN task_assignees t_ass     -- соединяем с таблицей назначений
            ON t_ass.task_id = t.id
        WHERE t_ass.user_id = ?       -- фильтр по пользователю
        """

        # параметры запроса (первый — user_id)
        params: list = [user_id]

        # если передан статус — добавляем фильтр
        if status is not None:
            if status != "my_tasks":  # спец-режим: "my_tasks" = без фильтра по статусу
                sql += " AND t_ass.status = ?"
                params.append(status)

        # сортировка новых задач сверху + ограничение выдачи
        sql += " ORDER BY t.id DESC LIMIT 3"

        # выполняем запрос и возвращаем все найденные строки
        return await db.execute(query=sql, params=tuple(params), fetchall=True)

    except Exception as e:
        write_logs(
            "[ERROR] database/tables/tasks.py | get_users_task_by_tgID() | "  # логируем ошибку запроса
            f"{e}"
        )
        return  # при ошибке возвращаем None
