import sqlite3
from database.database import get_db_cursor
from database.migrations.migrations import create_all_tables
from database.tables.organization.organization import add_organization
from database.tables.branches.branches import add_branch
from database.tables.departments.departments import add_department
from database.tables.positions.positions import add_position
from database.tables.users.users import add_user
from database.tables.tasks.tasks import add_task
from database.tables.task_assignees.task_assignees import add_task_assignee

cursor = get_db_cursor()
create_all_tables(cursor)

add_organization(cursor, "Murod Biznes")
add_branch(cursor, 1, "Toshkent")
add_department(cursor, 1, "IT Department")
add_position(cursor, 1, "Backend Developer")
add_position(cursor, 1, "Fronted Developer")
add_position(cursor, 1, "Fullstack Developer")

add_user(
    cursor=cursor,
    tg_id=809673082,
    pin_code="12345678901234",
    role="superadmin",
    lang="ru",
    password="password123",
    position_id=1,
    surname="Murodjon",
    last_name="X",
    middle_name="X",
    date_of_birth="2007-07-10",
    phone_number="+998999999999",
    work=1
)

add_user(
    cursor=cursor,
    tg_id=6036442860,
    pin_code="12445378901934",
    role="user",
    lang="uz",
    password="password1234",
    position_id=3,
    surname="Lazizbek",
    last_name="X",
    middle_name="X",
    date_of_birth="2000-07-10",
    phone_number="+998909999999",
    work=1
)

add_user(
    cursor=cursor,
    tg_id=5031965443,
    pin_code="15445378191934",
    role="user",
    lang="uz",
    password="password12345",
    position_id=2,
    surname="Kamron",
    last_name="X",
    middle_name="X",
    date_of_birth="1990-07-10",
    phone_number="+998939999999",
    work=1
)

add_task(cursor, "file_id_1", "Текст первого нового задание", "new", 3)
add_task(cursor, "file_id_1", "Текст первого нового задание", "new", 2)
add_task(cursor, "file_id_2", "Текст второго просроченного задание", "overdue", 2)
add_task(cursor, "file_id_3", "Текст третьего задание", "completed", 2)
add_task(cursor, "file_id_3", "Текст первого нового задание", "completed", 3)
add_task(cursor, "file_id_4", "Текст четвертого задание", "in_progress", 2)
add_task(cursor, "file_id_5", "Текст пятого задание", "canceled", 2)

add_task_assignee(cursor, 1, 3)
add_task_assignee(cursor, 1, 2)
add_task_assignee(cursor, 2, 2)
add_task_assignee(cursor, 3, 2)
add_task_assignee(cursor, 3, 3)
add_task_assignee(cursor, 4, 2)
add_task_assignee(cursor, 5, 2)

cursor.connection.commit()