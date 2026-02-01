import aiosqlite

from logger.logger import write_logs


async def create_organizations_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS organizations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE organizations ERROR: {e}")
        raise
