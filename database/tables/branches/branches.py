import sqlite3

def create_branches_table(cursor: sqlite3.Cursor) -> None:
    """
    Создает таблицу 'branches' в базе данных с указанными полями. 

    Args:
        cursor (sqlite3.Cursor): Соединение с базой данных.
    """
    
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