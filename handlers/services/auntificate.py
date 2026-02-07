from typing import Optional

from answers_template import ANSWERS

from database.database import DataBase
from database.tables.users import get_info_of_user, get_user_account_password

from handlers.utils.data_type import CacheUser
from handlers.services.cache import get_user_in_cache, save_user_in_cache

db = DataBase()


async def auntificate(tg_id: int, pin_code: Optional[int] = None) -> tuple[str, CacheUser | None]:
    """
        Проверка/получение пользователя:
        1) пробуем из кэша
        2) если нет — идём в БД (по tg_id или tg_id+pin_code)
        3) если нашли — сохраняем в кэш
        Возвращаем (текст_ответа_логина, user_cache|None)
    """
    user: CacheUser | None = get_user_in_cache(tg_id)
    login_answer: dict = ANSWERS["login"]
    lang: str = "uz"

    # cache -> db
    if user is None:
        # тянем пользователя из БД
        user_db = await get_info_of_user(db, tg_id, pin_code)
        
        # если в БД нет — логин провален
        if user_db is None:
            return login_answer["login_failed"][lang], user
            
        # кладём в кэш важные поля (db_id/lang/role)
        user = save_user_in_cache(
            tg_id, user_db["id"], user_db["lang"], user_db["role"]
        )
    
    # успех: текст на языке пользователя из кэша
    return login_answer["login_success"][user["lang"]], user


async def check_password(tg_id: int, input_password: str, pin_code: Optional[str] = None) -> bool | None:
    """
        Проверка пароля:
        - тянем пароль из БД
        - если пароль есть и не совпал → None (как "неверный")
        - если совпал или пароля нет → True
    """
    user_password = await get_user_account_password(db, tg_id, pin_code)
    
    if user_password:
        if input_password != user_password["password"]:
            return None

    return True
