from database.database import get_db_cursor
from database.migrations.migrations import create_all_tables

cursor = get_db_cursor()
create_all_tables(cursor)