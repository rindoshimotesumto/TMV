import sqlite3

def create_positions_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'positions' в базе данных с указанными столбцами и ограничениями.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,

        department_id INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """

    cursor.execute(create_table_sql)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_positions_department_id
    ON positions(department_id);
    """)

    cursor.connection.commit()