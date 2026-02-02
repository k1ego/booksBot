from __future__ import annotations
from aiogram import F, Router, types

from keyboards.catalog import BookCBData, CategoryCBData, back_to_category_catalog_kb, generate_books_kb, generate_catalog_kb

router = Router()

CATALOG = {
    "novels": {
        "text": "Романы",
        "description": "Книги романы",
        "books": [
            {
                "id": 1,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 100,
            },
            {
                "id": 2,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 200,
            },
            {
                "id": 3,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 300,
            },
        ],
    },
    "fantasy": {
        "text": "Фентези",
        "description": "Книги фентези",
        "books": [
            {
                "id": 4,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 100,
            },
            {
                "id": 5,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 200,
            },
            {
                "id": 6,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 300,
            },
        ],
    },
    "horror": {
        "text": "Хорроры",
        "description": "Книги хорроры",
        "books": [
            {
                "id": 7,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 100,
            },
            {
                "id": 8,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 200,
            },
            {
                "id": 9,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 300,
            },
        ],
    },
    "detectives": {
        "text": "Детективы",
        "description": "Книги детективы",
        "books": [
            {
                "id": 10,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 100,
            },
            {
                "id": 11,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 200,
            },
            {
                "id": 12,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 300,
            },
        ],
    },
    "documentaries": {
        "text": "Документалки",
        "description": "Книги документалки",
        "books": [
            {
                "id": 13,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 100,
            },
            {
                "id": 14,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 200,
            },
            {
                "id": 15,
                "name": "Книга {}",
                "description": "Описание книги {}",
                "price": 300,
            },
        ],
    },
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


@router.callback_query(CategoryCBData.filter())
async def category_info(callback: types.CallbackQuery, callback_data: CategoryCBData):

    category = CATALOG.get(callback_data.category)

    await callback.message.edit_text(
        text=category["description"],
        reply_markup=generate_books_kb(category["books"], callback_data.category),
    )


@router.callback_query(BookCBData.filter())
async def book_info(callback: types.CallbackQuery, callback_data: BookCBData):
    book_id = callback_data.id
    category = CATALOG.get(callback_data.category)
    
    book = None

    for bk in category["books"]:
        if bk["id"] == book_id:
            book = bk
            break
    
    if not book:
        return await callback.answer("Книга не найдена.")

    await callback.message.edit_text(
        text=(
            f"Название - {book['name'].format(book['id'])}\n"
            f"Описание - {book['description'].format(book['id'])}\n"
            f"Цена: {book['price']}руб.\n\n"
            "Хотите купить эту книгу?"
        ),
        reply_markup=back_to_category_catalog_kb(callback_data.category),
    )