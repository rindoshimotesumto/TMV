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

db = DataBase()  # экземпляр класса БД (берём путь к файлу базы и настройки)


async def create_all_tables() -> None:
    # соединение с SQLite по пути db.db_path
    async with aiosqlite.connect(db.db_path) as connect:

        # список функций-создателей таблиц (каждая создаёт свою таблицу)
        # порядок важен — сначала справочники, потом зависимые таблицы
        TABLE_CREATORS = [
            organizations.create_organizations_table,       # организации
            branches.create_branches_table,                 # филиалы (зависят от организаций)
            departments.create_departments_table,           # отделы
            positions.create_positions_table,               # должности
            task_assignees.create_task_assignees_tables,    # связка задачи ↔ исполнители
            tasks.create_tasks_table,                       # задачи
            users.create_users_table,                       # пользователи
        ]

        # последовательно вызываем каждую функцию создания таблицы
        for table in TABLE_CREATORS:
            await table(connect)

        # включаем поддержку FOREIGN KEY в SQLite (по умолчанию выключена!)
        await connect.execute("PRAGMA foreign_keys = ON")

        # фиксируем все CREATE TABLE в базе
        await connect.commit()

        # пишем лог об успешном создании всех таблиц
        write_logs("ALL TABLES CREATED ✅")
