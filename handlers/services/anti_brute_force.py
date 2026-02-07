import math
import time
from answers_template import LOCKS
from handlers.utils.config import LOCK_TIME, MAX_FAILS

# хранилище попыток в памяти процесса
FAILS_COUNT: dict[int, dict] = {}

def seconds_to_minutes(locked_until: float, now: float) -> int:
    # (locked_until - now) / 60 → сколько минут осталось
    # ceil → округление вверх, чтобы не показать "0 минут"
    # max(1, ...) → минимум 1 минута
    return max(1, math.ceil((locked_until - now) / 60))

def is_locked(tg_id: int, lang: str = "uz") -> str | None:
    # защита от lang=None
    if not isinstance(lang, str):
        lang = "uz"

    # берём инфу по юзеру (fails + locked_until)
    info = FAILS_COUNT.get(tg_id)
    
    # если попыток ещё не было — значит не заблокирован
    if not info:
        return None

    now = time.time()
    
    # если lock ещё активен — отдаём текст с оставшимися минутами
    if info["locked_until"] > now:
        minutes = seconds_to_minutes(info["locked_until"], now)
        return LOCKS["too_many_attempts"][lang].format(minutes=minutes)
    
    # если lock уже прошёл — заблокированным не считаем
    return None

def register_fail(tg_id: int) -> None:
    """
        Регистрируем неудачную попытку (неверный пароль/пин и т.п.)
    """
    now = time.time()
    info = FAILS_COUNT.get(tg_id)
    
    # первая ошибка — создаём запись
    if not info:
        FAILS_COUNT[tg_id] = {"fails": 1, "locked_until": 0}
        return

    # если был лок, но он уже прошёл — начинаем считать заново
    # (по факту: продолжаем считать fails, если лок уже не активен)
    if info["locked_until"] <= now:
        info["fails"] += 1
    
    # достигли лимита — ставим lock и сбрасываем счётчик
    if info["fails"] >= MAX_FAILS:
        info["fails"] = 0
        info["locked_until"] = now + LOCK_TIME

def reset_fails(tg_id: int) -> None:
    # сбрасываем инфу по ошибкам (например, после успешного логина)
    FAILS_COUNT.pop(tg_id, None)