from answers_template import ANSWERS
from database.database import DataBase
from database.tables.users import get_info_of_user, get_info_user_by_pin_code
from handlers.utils.cache import cache_get_user, cache_set_user
from logger.logger import write_logs

db = DataBase()


async def login_user(tg_id: int, pin_code: str = "") -> tuple:
    """
    Пытается выполнить вход пользователя по Telegram ID (tg_id) или по ЖШШИР(pin_code).

    Сначала проверяет кэш. Если в кэше нет — запрашивает БД.\n
    Возвращает кортеж: (status, text, lang, role, password)

    :return: tuple[bool, str, str, str, str] — (успех, сообщение, язык, роль, пароль)
    """

    in_cache: dict | None = cache_get_user(tg_id)
    status: bool = True
    lang: str = "uz"
    role: str = "user"
    password: str = ""
    result: str = ""

    # если юзера нет в кешах, ищим в бд
    if not in_cache:
        # если мы передали pin_code то ищеи по pin_code в ином случае по tg.id
        if pin_code != "":
            user_info = await get_info_user_by_pin_code(db, pin_code)
        else:
            user_info = await get_info_of_user(db, tg_id)

        # если найдем то сохраняем в кеш и логируем
        if user_info:
            cache_set_user(tg_id, user_info)
            write_logs(f"tg.id: {tg_id} added in USER_CACHE")

            lang = user_info["lang"]
            role = user_info["role"]
            password = user_info["password"]
            result = ANSWERS["login"]["login_success"][lang]

        # если нет в бд то просим обратится к админу
        else:
            status = False

            # если проверка с помощю pin_code говорим что не сможем помочь, в ином случае просим писать pin_cod
            if pin_code == "":
                result = ANSWERS["login"]["input_pin"]["uz"]

            else:
                result = ANSWERS["login"]["login_failed"]["uz"]

    # если юзер в кешах то возвращаем ответ
    else:
        lang = in_cache["lang"]
        role = in_cache["role"]
        password = in_cache["password"]
        result = ANSWERS["login"]["login_success"][lang]

    return (status, result, lang, role, password)
