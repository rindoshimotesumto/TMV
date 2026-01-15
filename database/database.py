import sqlite3

def get_db_cursor() -> sqlite3.Cursor:
    conn = sqlite3.connect("tmv_database.db")
    cursor = conn.cursor()
    return cursor