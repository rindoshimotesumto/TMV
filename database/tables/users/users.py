import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_users_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'users' в базе данных с указанными полями.

    Args:   
        cursor (sqlite3.Cursor): Соединение с базой данных.
    """
    
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL UNIQUE,

            pin_code TEXT NOT NULL,

            password TEXT NOT NULL CHECK (8 <= LENGTH(password) <= 64),

            position_id INTEGER NOT NULL,

            surname TEXT NOT NULL,
            last_name TEXT NOT NULL,
            middle_name TEXT NOT NULL,

            date_of_birth DATE NOT NULL,

            phone_number TEXT UNIQUE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            works INTEGER DEFAULT 1,

            FOREIGN KEY (position_id) REFERENCES positions(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """

        cursor.execute(create_table_sql)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_position_id
        ON users(position_id);
        """)

        cursor.connection.commit()
        db_ok("Created 'users' table successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error creating 'users' table: {e} ❌")


def add_user(cursor: sqlite3.Cursor, tg_id: int, pin_code: str, password: str, position_id: int,
             surname: str, last_name: str, middle_name: str,
             date_of_birth: str, phone_number: str | None = None) -> None:
    """
    Добавляет нового пользователя в таблицу 'users'.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных.
        tg_id (int): Telegram ID пользователя.
        pin_code (str): PIN пользователя.
        password (str): Пароль пользователя.
        position_id (int): ID должности пользователя.
        surname (str): Фамилия пользователя.
        last_name (str): Имя пользователя.
        middle_name (str): Отчество пользователя.
        date_of_birth (str): Дата рождения пользователя в формате 'YYYY-MM-DD'.
        phone_number (str): Номер телефона пользователя.
    """
    
    try:
        insert_user_sql = """
        INSERT INTO users (tg_id, pin_code, password, position_id, surname, last_name, middle_name, date_of_birth, phone_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        cursor.execute(insert_user_sql, (tg_id, pin_code, password, position_id,
                                         surname, last_name, middle_name,
                                         date_of_birth, phone_number))

        cursor.connection.commit()
        db_ok(f"Added user with tg_id({tg_id}) successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error adding user with tg_id({tg_id}): {e} ❌")