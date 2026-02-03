from typing import Iterable, Optional

import aiosqlite

from database.database import DataBase
from logger.logger import write_logs


async def create_tasks_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_audio_file_id TEXT NOT NULL,
                audio_text TEXT NOT NULL,

                status TEXT CHECK (status IN ('new', 'in_progress', 'completed', 'canceled', 'overdue')) DEFAULT 'new',

                user_id INTEGER NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE tasks ERROR: {e}")
        raise


async def get_users_task_by_tgID(
    db: DataBase, user_id: int, status: Optional[str] = None
) -> Iterable[aiosqlite.Row] | None:
    """
    Возвращает список задач пользователя.\n
    Если передан статус — возвращает только задачи с этим статусом,
    иначе — все задачи пользователя.
    """
    try:
        # базовый SQL-запрос: берём задачи и связываем их с таблицей назначений
        sql: str = """
        SELECT
            t.user_id,
            t.audio_text,
            t.tg_audio_file_id,
            t_ass.task_id

        FROM tasks t
        JOIN task_assignees t_ass
            ON t_ass.task_id = t.id
        WHERE t_ass.user_id = ?
        """

        # список параметров для подстановки в SQL (начинаем с user_id)
        params: list = [user_id]

        # если указан статус — добавляем фильтр по статусу задачи
        if status is not None:
            sql += " AND t_ass.status = ?"
            params.append(status)

        # сортировка по убыванию id задачи и ограничение количества результатов
        sql += " ORDER BY t.id DESC LIMIT 3"

        # выполняем запрос и возвращаем все найденные строки
        return await db.execute(query=sql, params=tuple(params), fetchall=True)

    except Exception as e:
        write_logs(f"[ERROR] database/tables/tasks.py | get_users_task_by_tgID() | {e}")
        return
