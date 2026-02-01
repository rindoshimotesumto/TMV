import aiosqlite

from logger.logger import write_logs


async def create_positions_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,

                department_id INTEGER NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT ON UPDATE CASCADE);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE positions ERROR: {e}")
        raise
