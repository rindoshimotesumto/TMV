from aiogram import Router
from aiogram.types import Message, CallbackQuery
from handlers.user.utils import words, error_cmd
from aiogram.filters.command import CommandObject, CommandStart, Command
from keyboards.callback_query.callback_query import build_kb
from handlers.utils.login_user import login_user_with_tg_id
from handlers.start.only_start_text import START_ANSWER

router = Router()

@router.message(CommandStart())
async def login_user(message: Message):
    role_and_lang = login_user_with_tg_id(message.from_user.id)

    if role_and_lang:
        lang = role_and_lang[-1]
        role = role_and_lang[0]
        
        await message.answer(f"{START_ANSWER[lang][True]}!", reply_markup=build_kb(role=role, lang=lang))
    
    else:
        await message.answer(f"{START_ANSWER["uz"][False]}!")