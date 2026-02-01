import aiosqlite

from logger.logger import write_logs


async def create_task_assignees_tables(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS task_assignees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,

                status TEXT CHECK (status IN ('not_started', 'started', 'in_progress', 'completed', 'failed', 'canceled')) DEFAULT 'not_started',
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(task_id, user_id),

                FOREIGN KEY (task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE task_assignees ERROR: {e}")
        raise
