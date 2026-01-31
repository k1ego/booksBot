from __future__ import annotations
from aiogram import F, Router, types

from keyboards.catalog import generate_catalog_kb

router = Router()

CATALOG = {
    "novels": {"text": "Романы", "description": "Книги романы"},
    "fantasy": {"text": "Фентези", "description": "Книги фентези"},
    "horror": {"text": "Хорроры", "description": "Книги хорроры"},
    "detectives": {"text": "Детективы", "description": "Книги детективы"},
    "documentaries": {"text": "Документалки", "description": "Книги документалки"}
}

@router.callback_query(F.data == "catalog")
@router.message(F.text == "Каталог")
async def catalog(update: types.Message | types.CallbackQuery):
    if isinstance(update, types.Message):
        await update.answer(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(CATALOG),
        )
    else:
        await update.message.edit_text(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(CATALOG),
        )


@router.callback_query(F.data.startswith("category:"))
async def category_info(callback: types.CallbackQuery):
    category_key = callback.data.split(":")[-1]
    category = CATALOG.get(category_key)

    await callback.message.edit_text(
        text=category["description"],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Назад", 
                        callback_data="catalog"
                    )
                ]
            ]
        )
    )