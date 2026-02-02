from aiogram import Router, types
from aiogram.filters import Command

from keyboards.menu import main_menu_kb

router = Router()


@router.message(Command("start"))
async def start_bot(message: types.Message, session):
    await message.answer(
        f"Привет, {message.from_user.full_name}!\nЯ магазин книг, выбери нужно меню снизу:",
        reply_markup=main_menu_kb(),
    )
