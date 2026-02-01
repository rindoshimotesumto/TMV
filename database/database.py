import aiosqlite


class DataBase:
    def __init__(self, db_path="database.db") -> None:
        self.db_path = db_path

    async def execute(
        self,
        query: str,
        params: tuple = (),
        fetchone: bool = False,
        fetchall: bool = False,
        commit: bool = False,
    ):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute(query, params) as cursor:
                if commit:
                    await db.commit()

                if fetchone:
                    return await cursor.fetchone()

                if fetchall:
                    return await cursor.fetchall()
