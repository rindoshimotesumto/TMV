import time

from logger.logger import write_logs

USERS_CACHE: dict[int, tuple[dict, float]] = {}
# ------
SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
# ------

CACHE_TTL: int = 30 * MINUTE


def cache_set_user(tg_id: int, user: dict) -> None:
    """
    Добавляет пользователя в кэш с временем жизни (TTL).\n

    :param tg_id: Telegram ID пользователя.
    :param user: Словарь с данными пользователя.
    """

    USERS_CACHE[tg_id] = (dict(user), time.time() + CACHE_TTL)


def cache_delete_user(tg_id: int) -> None:
    """
    Удаляет пользователя из кэша по Telegram ID.\n

    :param tg_id: Telegram ID пользователя.
    """

    USERS_CACHE.pop(tg_id, None)


def cache_get_user(tg_id: int) -> dict | None:
    """
    Получает данные пользователя из кэша по Telegram ID.\n

    Проверяет срок жизни записи (TTL). Если запись устарела —
    возвращает None и стирает с памяти.

    :param tg_id: Telegram ID пользователя.
    :return: Словарь с данными пользователя или None, если записи нет
             или срок действия истёк.
    """

    cached: tuple[dict, float] | None = USERS_CACHE.get(tg_id)

    if cached:
        data: dict
        expire: float

        data, expire = cached
        now: float = time.time()

        if expire > now:
            return data

        cache_delete_user(tg_id)

    return None


def get_users_in_cache() -> None:
    result = "USERS in cache LIST" + "\n" + "-" * 100 + "\n"

    for key, value in USERS_CACHE.items():
        result += f"tg.id(key): {key}\ninfo(value): {value}" + "\n" + "-" * 100 + "\n"

    write_logs(
        f"CALL: handlers/start/login_user.py | get_users_in_cache() | ✅\n\nResult: {result}"
    )
