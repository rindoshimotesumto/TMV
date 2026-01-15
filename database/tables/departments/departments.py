import sqlite3

def create_departments_table(cursor: sqlite3.Cursor) -> None:
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