import sqlite3

def create_organization_table(cursor: sqlite3.Cursor) -> None:
    """
    Создание таблицы "organization" в базе данных SQLite.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS organization (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_table_sql)
    cursor.connection.commit()