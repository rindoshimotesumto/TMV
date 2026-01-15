import sqlite3
from database.db_logger.db_logger import db_ok, db_error

def create_branches_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'branches' в базе данных с указанными полями. 

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных.
    """
    
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,

            organization_id INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (organization_id) REFERENCES organization(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """

        cursor.execute(create_table_sql)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_branches_organization_id
        ON branches(organization_id);
        """)

        cursor.connection.commit()
        db_ok("Table 'branches' created successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error creating table 'branches': {e} ❌")


def add_branch(cursor: sqlite3.Cursor, name: str, organization_id: int) -> None:
    """
    Добавляет новую запись в таблицу 'branches'.

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных.
        name (str): Название филиала.
        organization_id (int): Идентификатор организации, к которой принадлежит филиал.
    """
    
    try:
        insert_sql = """
        INSERT INTO branches (name, organization_id)
        VALUES (?, ?);
        """

        cursor.execute(insert_sql, (name, organization_id))
        cursor.connection.commit()
        
        db_ok(f"Branch '{name}' added successfully ✅")

    except sqlite3.Error as e:
        cursor.connection.rollback()
        db_error(f"Error adding branch '{name}': {e} ❌")