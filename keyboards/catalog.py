from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class CategoryCBData(CallbackData, prefix="category"):
    category_id: int


class BookCBData(CallbackData, prefix="book"):
    id: int

class BuyBookCBData(CallbackData, prefix="buy-book"):
    id: int


def generate_catalog_kb(categories):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category in categories:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category.name,
                    callback_data=CategoryCBData(category_id=category.id).pack(),
                )
            ]
        )
    return keyboard


def generate_books_kb(books):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for book in books:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=book.name.format(book.id),
                    callback_data=BookCBData(id=book.id).pack(),
                )
            ]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=" << Назад", callback_data="catalog")]
    )
    return keyboard


def back_to_category_catalog_kb(book_id, category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=BuyBookCBData(id=book_id).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text=" << Назад",
                    callback_data=CategoryCBData(category_id=category_id).pack(),
                )
            ]
        ]
    )
