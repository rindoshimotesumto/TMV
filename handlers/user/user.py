from aiogram import Router
from aiogram.types import Message, CallbackQuery
from handlers.user.utils import words, error_cmd
from aiogram.filters.command import CommandObject, CommandStart, Command
from keyboards.callback_query.callback_query import build_kb

router = Router()

@router.message()
async def msg(message: Message):
    await message.answer(text=words["uz"]["message"])

@router.callback_query()
async def callback(call: CallbackQuery):
    await call.message.answer(text=call.data)