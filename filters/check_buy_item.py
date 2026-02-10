from aiogram.filters import Filter
from aiogram import types

from keyboards.catalog import BuyBookCBData
from repositories.books import BookRepo
from repositories.user import UserRepo

class FilterUserCanBuyBook(Filter):
		async def __call__(
				self, 
				callback: types.CallbackQuery, 
				book_repo: BookRepo, 
				user_repo: UserRepo
			):
				book_id = callback.data.split(":")[1]  # Предполагается, что callback_data имеет формат "buy_book:{book_id}"

				book = await book_repo.get_book_by_id(book_id)
				user = await user_repo.get_user_by_tg_id(callback.from_user.id)

				if user.balance < book.price:
						await callback.answer("Недостаточно средств для покупки книги.", show_alert=True)
						return
						
				return True