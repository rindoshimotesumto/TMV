import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_task_assignees_table(cursor: sqlite3.Cursor) -> None:
    
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS task_assignees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,

        status TEXT CHECK (status IN ('started', 'in_progress', 'completed', 'not_started', 'failed', 'canceled')) DEFAULT 'not_started',
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(task_id, user_id),

        FOREIGN KEY (task_id)
            REFERENCES tasks(id)
            ON DELETE CASCADE,

        FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        ); 
        """
            
        cursor.execute(create_table_sql)
        db_ok("Таблица task_assignees успешно создана ✅ ✅")

    except sqlite3.Error as e:
        db_error(f"Ошибка при создании таблицы task_assignees: {e} ❌")



def add_task_assignee(cursor: sqlite3.Cursor, task_id: int, user_id: int, status: str="not_started") -> None:
    try:
        insert_sql = """
        INSERT INTO task_assignees (task_id, user_id, status)
        VALUES (?, ?, ?);
        """
        cursor.execute(insert_sql, (task_id, user_id, status))
        db_ok(f"Пользователь с ID {user_id} успешно назначен на задачу с ID {task_id} ✅")
        
    except sqlite3.IntegrityError as e:
        db_error(f"Ошибка при назначении пользователя с ID {user_id} на задачу с ID {task_id}: {e} ❌")
    
    except sqlite3.Error as e:
        db_error(f"Общая ошибка базы данных при назначении пользователя с ID {user_id} на задачу с ID {task_id}: {e} ❌")