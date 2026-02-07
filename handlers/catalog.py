from __future__ import annotations
from aiogram import F, Router, types

from keyboards.catalog import (
    BookCBData,
    CategoryCBData,
    back_to_category_catalog_kb,
    generate_books_kb,
    generate_catalog_kb,
)
from repositories.categories import CategoryRepo

router = Router()


@router.callback_query(F.data == "catalog")
@router.message(F.text == "Каталог")
async def catalog(
    update: types.Message | types.CallbackQuery, category_repo: CategoryRepo
):
    categories = await category_repo.get_list()

    if isinstance(update, types.Message):
        await update.answer(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(categories),
        )
    else:
        await update.message.edit_text(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(categories),
        )


@router.callback_query(CategoryCBData.filter())
async def category_info(callback: types.CallbackQuery, callback_data: CategoryCBData, category_repo: CategoryRepo):

    category = await category_repo.get_by_id(callback_data.category_id)

    await callback.message.edit_text(
        text=category.description,
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
