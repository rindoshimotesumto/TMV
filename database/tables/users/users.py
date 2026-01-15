import sqlite3

def create_users_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'users' в базе данных с указанными полями.

    Args:   
        cursor (sqlite3.Cursor): Соединение с базой данных.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER NOT NULL UNIQUE,

        pin_code TEXT NOT NULL CHECK (
            pin_code GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
        ),

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