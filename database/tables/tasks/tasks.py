import sqlite3

def create_tasks_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'tasks' в базе данных с указанными столбцами и ограничениями.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,

        user_id INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """

    cursor.execute(create_table_sql)
    cursor.connection.commit()