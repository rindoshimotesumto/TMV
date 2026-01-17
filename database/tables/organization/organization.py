import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_organization_table(cursor: sqlite3.Cursor) -> None:
    """
    Создание таблицы "organization" в базе данных SQLite.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    try:
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
        db_ok("Таблица organization успешно создана ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Ошибка при создании таблицы organization: {e} ❌")

def add_organization(cursor: sqlite3.Cursor, name: str) -> None:
    """
    Добавление новой организации в таблицу "organization".

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
        name (str): Название организации.
    """

    try:
        insert_sql = """
        INSERT INTO organization (name)
        VALUES (?);
        """
    
        cursor.execute(insert_sql, (name,))
        cursor.connection.commit()

        db_ok(f"Организация '{name}' добавлена успешно ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Ошибка при добавлении организации '{name}': {e} ❌")