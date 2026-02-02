from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class CategoryCBData(CallbackData, prefix="category"):
    category: str


class BookCBData(CallbackData, prefix="book"):
    id: int
    category: str


def generate_catalog_kb(catalog):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category_cb, category in catalog.items():
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category["text"],
                    callback_data=CategoryCBData(category=category_cb).pack(),
                )
            ]
        )
    return keyboard


def generate_books_kb(books, category):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for book in books:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=book["name"].format(book["id"]),
                    callback_data=BookCBData(id=book["id"], category=category).pack(),
                )
            ]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=" << Назад", callback_data="catalog")]
    )
    return keyboard


def back_to_category_catalog_kb(category_cb):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" << Назад",
                    callback_data=CategoryCBData(category=category_cb).pack(),
                )
            ]
        ]
    )
