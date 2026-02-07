from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query()
async def cmd_start(call: CallbackQuery, state: FSMContext): ...
