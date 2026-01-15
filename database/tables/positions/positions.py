import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_positions_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'positions' в базе данных с указанными столбцами и ограничениями.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
    """

    try:
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
        db_ok("Created 'positions' table successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error creating 'positions' table: {e} ❌")


def add_position(cursor: sqlite3.Cursor, name: str, department_id: int) -> None:
    """
    Добавляет новую позицию в таблицу 'positions'.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных SQLite.
        name (str): Название позиции.
        department_id (int): Идентификатор отдела, к которому относится позиция.
    """

    try:
        insert_sql = """
        INSERT INTO positions (name, department_id)
        VALUES (?, ?);
        """

        cursor.execute(insert_sql, (name, department_id))
        cursor.connection.commit()
        
        db_ok(f"Added position '{name}' successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error adding position '{name}': {e} ❌")