from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, TelegramObject

from database.database import DataBase
from handlers.services.anti_brute_force import is_locked
from handlers.services.cache import get_user_in_cache

db = DataBase()


class CacheUserMiddleware(BaseMiddleware):
    """
        Middleware для подгрузки пользователя из кэша
        и проброса его в data для хендлеров и других middleware.
    """
    async def __call__(self, handler, event: TelegramObject, data):
        from_user = getattr(event, "from_user", None)
        
        if from_user:
            tg_id = from_user.id
            # кладём пользователя из кеша в data
            # теперь в handler можно делать: data["cache_user"]
            data["cache_user"] = get_user_in_cache(tg_id)  # dict | None
            
        return await handler(event, data)


class AntiBruteMiddleware(BaseMiddleware):
    """
        Middleware защиты от брутфорса / спама.
        Проверяет — не заблокирован ли пользователь.
        Если заблокирован — отвечает и НЕ пускает дальше в handler.
    """
    async def __call__(self, handler, event: TelegramObject, data):
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)
            
        # берём пользователя из data (который положил CacheUserMiddleware)
        cache_user = data.get("cache_user")
        
        # определяем язык — если нет в кеше, дефолт uz
        lang = (cache_user or {}).get("lang", "uz")
        
        # проверяем lock статус
        msg = is_locked(event.from_user.id, lang)

        if msg:
            # отправляем сообщение о блокировке
            await event.answer(msg)
            return
        
        # если всё ок — пускаем дальше
        return await handler(event, data)


middlwares: list = [CacheUserMiddleware, AntiBruteMiddleware]


async def setup_middlewares(dp: Dispatcher):
    """
       Подключение middleware к Dispatcher.
       Вызывается при старте бота.
    """
    for mw_cls in middlwares:
        mw = mw_cls()
        dp.message.middleware(mw)
    
    dp.callback_query.middleware(CacheUserMiddleware())
