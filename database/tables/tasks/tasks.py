import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_tasks_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'tasks' в базе данных с указанными столбцами и ограничениями.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_audio_file_id TEXT NOT NULL,
            audio_text TEXT NOT NULL,

            user_id INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """

        cursor.execute(create_table_sql)
        cursor.connection.commit()
        
        db_ok("Created 'tasks' table successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error creating 'tasks' table: {e} ❌")


def add_task(cursor: sqlite3.Cursor, tg_audio_file_id: str, audio_text: str, user_id: int) -> None:
    """
    Добавляет новую задачу в таблицу 'tasks'.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
        tg_audio_file_id (str): ID аудио файла.
        audio_text (str): Текст аудио.
        user_id (int): Идентификатор пользователя, которому принадлежит задача.
    """

    try:
        insert_task_sql = """
        INSERT INTO tasks (tg_audio_file_id, audio_text, user_id)
        VALUES (?, ?, ?);
        """

        cursor.execute(insert_task_sql, (tg_audio_file_id, audio_text, user_id))
        cursor.connection.commit()

        db_ok(f"Added task for user_id({user_id}) successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error adding task: {e} ❌")