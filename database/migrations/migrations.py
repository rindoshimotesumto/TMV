import aiosqlite

from database.database import DataBase
from database.tables import (
    branches,
    departments,
    organizations,
    positions,
    task_assignees,
    tasks,
    users,
)
from logger.logger import write_logs

db = DataBase()


async def create_all_tables() -> None:
    async with aiosqlite.connect(db.db_path) as connect:
        TABLE_CREATORS = [
            organizations.create_organizations_table,
            branches.create_branches_table,
            departments.create_departments_table,
            positions.create_positions_table,
            task_assignees.create_task_assignees_tables,
            tasks.create_tasks_table,
            users.create_users_table,
        ]

        for table in TABLE_CREATORS:
            await table(connect)

        await connect.execute("PRAGMA foreign_keys = ON")

        await connect.commit()
        write_logs("ALL TABLES CREATED ✅")
