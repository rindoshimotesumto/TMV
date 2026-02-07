import time

from handlers.utils.config import CACHE_TTL
from handlers.utils.data_type import CacheUser

# Кэш в памяти процесса
USER_CACHE: dict[int, CacheUser] = {}


def get_user_in_cache(tg_id: int) -> CacheUser | None:
    # берём запись из кэша
    user = USER_CACHE.get(tg_id)
    
    # берём запись из кэша
    if not user:
        return None
    
    # TTL истёк — удаляем и возвращаем None
    if user["expire_at"] < time.time():
        delete_user_in_cache(tg_id)
        return None
    
    # sliding TTL: если пользователь активен — продлеваем срок жизни
    USER_CACHE[tg_id]["expire_at"] = time.time() + CACHE_TTL
    
    # возвращаем данные
    return user


def save_user_in_cache(tg_id: int, db_id: int, lang: str, role: str) -> CacheUser:
    # формируем объект кэша пользователя
    user_cache: CacheUser = {
        "db_id": db_id,
        "lang": lang,
        "role": role,
        "expire_at": time.time() + CACHE_TTL,
    }
    
    # кладём в общий dict
    USER_CACHE[tg_id] = user_cache
    return user_cache


def delete_user_in_cache(tg_id: int) -> None:
    # безопасное удаление
    USER_CACHE.pop(tg_id, None)
