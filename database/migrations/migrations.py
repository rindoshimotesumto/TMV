import sqlite3
from database.database import get_db_cursor
from database.tables.organization import organization
from database.tables.branches import branches
from database.tables.departments import departments
from database.tables.positions import positions
from database.tables.users import users
from database.tables.tasks import tasks
from database.tables.task_assignees import task_assignees

cursor = get_db_cursor()

def create_all_tables(cursor: sqlite3.Cursor) -> None:
    organization.create_organization_table(cursor)
    branches.create_branches_table(cursor)
    departments.create_departments_table(cursor)
    positions.create_positions_table(cursor)
    users.create_users_table(cursor)
    tasks.create_tasks_table(cursor)
    task_assignees.create_task_assignees_table(cursor)