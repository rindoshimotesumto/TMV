import aiosqlite


class DataBase:
    def __init__(self, db_path="database.db") -> None:
        self.db_path = db_path  # путь к файлу SQLite базы данных

    async def execute(
        self,
        query: str,
        params: tuple = (),
        fetchone: bool = False,
        fetchall: bool = False,
        commit: bool = False,
    ):
        # открываем новое асинхронное соединение с БД на каждый вызов
        async with aiosqlite.connect(self.db_path) as db:

            # включаем возврат строк как dict-подобных объектов (Row),
            # чтобы можно было обращаться по имени колонки: row["id"]
            db.row_factory = aiosqlite.Row

            # выполняем SQL-запрос с параметрами (защита от SQL-инъекций)
            async with db.execute(query, params) as cursor:

                # если указано — фиксируем изменения (INSERT/UPDATE/DELETE)
                if commit:
                    await db.commit()

                # если запрошена одна строка — возвращаем cursor.fetchone()
                if fetchone:
                    return await cursor.fetchone()

                # если запрошены все строки — возвращаем cursor.fetchall()
                if fetchall:
                    return await cursor.fetchall()

                # если ни fetchone, ни fetchall — ничего не возвращаем
                # (подходит для CREATE TABLE, PRAGMA, простых INSERT без чтения)
