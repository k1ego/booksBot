from aiogram.filters import Filter
from aiogram import types

from keyboards.catalog import BuyBookCBData
from repositories.books import BookRepo
from repositories.user import UserRepo


class FilterUserCanBuyBook(Filter):
    async def __call__(
        self, callback: types.CallbackQuery, book_repo: BookRepo, user_repo: UserRepo
    ):
        # Проверяем, что это callback data для покупки книги
        if not callback.data or not callback.data.startswith("buy-book:"):
            return False  # Пропускаем все остальные callback data
        
        try:
            # Парсим callback data с помощью CallbackData
            callback_data = BuyBookCBData.unpack(callback.data)

            book_id = callback_data.id

            book = await book_repo.get_book_by_id(book_id)
            user = await user_repo.get_user_by_tg_id(callback.from_user.id)

            if user.balance < book.price:
                await callback.answer(
                    "Недостаточно средств для покупки книги.", show_alert=True
                )
                return False

            return True
            
        except (ValueError, TypeError, AttributeError) as e:
            # Логирование ошибки для отладки
            print(f"DEBUG: Error unpacking callback data: {e}")
            return False