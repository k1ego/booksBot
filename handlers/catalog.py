from __future__ import annotations
from aiogram import F, Router, types

from filters.check_buy_item import FilterUserCanBuyBook
from keyboards.catalog import (
    BookCBData,
    BuyBookCBData,
    CategoryCBData,
    back_to_category_catalog_kb,
    generate_books_kb,
    generate_catalog_kb,
)
from repositories.books import BookRepo
from repositories.categories import CategoryRepo
from repositories.user import UserRepo

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
async def category_info(
    callback: types.CallbackQuery,
    callback_data: CategoryCBData,
    category_repo: CategoryRepo,
    book_repo: BookRepo,
):

    category = await category_repo.get_by_id(callback_data.category_id)
    books = await book_repo.get_books_by_category_id(callback_data.category_id)

    await callback.message.edit_text(
        text=category.description,
        reply_markup=generate_books_kb(books),
    )


@router.callback_query(BookCBData.filter())
async def book_info(
    callback: types.CallbackQuery,
    callback_data: BookCBData,
    book_repo: BookRepo,
    user_repo: UserRepo,
):
    book = await book_repo.get_book_by_id(callback_data.id)
    user = await user_repo.get_user_by_tg_id(callback.from_user.id)

    await callback.message.edit_text(
        text=(
            f"Название - {book.name.format(book.id)}\n"
            f"Описание - {book.description.format(book.id)}\n"
            f"Цена: {round(book.price / 100, 2)}руб.\n"
            f"Ваш баланс: {user.view_balance} руб.\n\n"
            "Хотите купить эту книгу?"
        ),
        reply_markup=back_to_category_catalog_kb(book.id, book.category_id),
    )


@router.callback_query(FilterUserCanBuyBook(), BuyBookCBData.filter())
async def buy_book_action(
    callback: types.CallbackQuery,
    callback_data: BookCBData,
    book_repo: BookRepo,
    user_repo: UserRepo,
):

    book = await book_repo.get_book_by_id(callback_data.id)

    await user_repo.update_balance(callback.from_user.id, -book.price)

    await callback.message.answer(
        text=(
            f"Вы купили книгу - {book.name.format(book.id)}\n"
            f"Описание - {book.description.format(book.id)}\n"
            f"Цена: {round(book.price / 100, 2)}руб.\n\n"
            "Спасибо за покупку!"
        )
    )
    await callback.answer()
