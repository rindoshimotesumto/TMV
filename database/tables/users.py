import aiosqlite

from database.database import DataBase
from logger.logger import write_logs


async def create_users_table(db: aiosqlite.Connection) -> None:
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER NOT NULL UNIQUE,
                role TEXT CHECK (role IN ('admin', 'user', 'superadmin')) DEFAULT 'user',
                lang TEXT CHECK (lang IN ('uz', 'ru', 'en')) DEFAULT 'uz',

                pin_code TEXT NOT NULL UNIQUE,
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

                FOREIGN KEY (position_id) REFERENCES positions(id) ON DELETE RESTRICT ON UPDATE CASCADE);
            """)

    except Exception as e:
        write_logs(f"⚠️ TABLE users ERROR: {e}")
        raise


async def get_info_of_user(db: DataBase, tg_id: int) -> dict | None:
    try:
        user_info = await db.execute(
            query="""
                SELECT lang, role, password FROM users
                WHERE tg_id = ?;
            """,
            params=(tg_id,),
            fetchone=True,
        )

        write_logs("CALL: database/tables/users.py | get_info_of_user() | ✅")
        return user_info

    except Exception as e:
        write_logs(f"[ERROR]: database/tables/users.py | get_info_of_user() | {e}")
        return None


async def get_info_user_by_pin_code(db: DataBase, pin_code: str) -> dict | None:
    try:
        user_info = await db.execute(
            query="""
                SELECT lang, role, password FROM users
                WHERE pin_code = ?;
            """,
            params=(pin_code,),
            fetchone=True,
        )

        write_logs("CALL: /database/tables/users.py | get_info_user_by_pin() | ✅")
        return user_info

    except Exception as e:
        write_logs(f"[ERROR]: database/tables/users.py | get_info_user_by_pin() | {e}")
        return None
