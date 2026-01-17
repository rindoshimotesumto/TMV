import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_departments_table(cursor: sqlite3.Cursor) -> None:
    try:
        """
        Создает таблицу 'departments' в базе данных с указанными полями.

        Args:
            cursor (sqlite3.Cursor): Соединение с базой данных.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,

            branch_id INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """

        cursor.execute(create_table_sql)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_departments_branch_id
        ON departments(branch_id);
        """)

        cursor.connection.commit()
        db_ok("Таблица departments успешно создана ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Ошибка при создании таблицы departments: {e} ❌")

def add_department(cursor: sqlite3.Cursor, name: str, branch_id: int) -> None:
    try:
        """
        Добавляет новый отдел в таблицу 'departments'.

        Args:
            cursor (sqlite3.Cursor): Соединение с базой данных.
            name (str): Название отдела.
            branch_id (int): Идентификатор филиала, к которому относится отдел.
        """
        
        insert_sql = """
        INSERT INTO departments (name, branch_id)
        VALUES (?, ?);
        """

        cursor.execute(insert_sql, (name, branch_id))
        cursor.connection.commit()

        db_ok(f"Отдел '{name}' добавлен успешно ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Ошибка при добавлении отдела '{name}': {e} ❌")