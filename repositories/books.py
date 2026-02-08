from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.book import Book


class BookRepo:
		def __init__(self, session: AsyncSession):
				self.__session = session

		async def get_books_by_category_id(self, category_id: int):
				statement = select(Book).where(Book.category_id == category_id).order_by(Book.name)
				return await self.__session.scalars(statement)  
		
		async def get_book_by_id(self, book_id: int):
				statement = select(Book).where(Book.id == book_id)
				return await self.__session.scalar(statement)