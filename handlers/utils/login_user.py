from database.database import get_db_cursor
from database.tables.users.users import get_info_of_user_by_tg_id

cursor = get_db_cursor()

def login_user_with_tg_id(tg_id: int) -> str:
    result = get_info_of_user_by_tg_id(cursor, tg_id)
    if result:
        return result[2], result[3]
    
    return False