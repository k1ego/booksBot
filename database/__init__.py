from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .models.user import User
from .models.category import Category
from .models.book import Book

engine = create_async_engine(
    url="sqlite+aiosqlite:///book_shop.db"
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)

__all__ = [
	User,
	Category,
    Book,
]
