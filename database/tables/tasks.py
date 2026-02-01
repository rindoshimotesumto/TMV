import aiosqlite

from logger.logger import write_logs


async def create_tasks_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_audio_file_id TEXT NOT NULL,
                audio_text TEXT NOT NULL,

                status TEXT CHECK (status IN ('new', 'in_progress', 'completed', 'canceled', 'overdue')) DEFAULT 'new',

                user_id INTEGER NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE tasks ERROR: {e}")
        raise
