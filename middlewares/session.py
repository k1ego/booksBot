from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.books import BookRepo
from repositories.categories import CategoryRepo
from repositories.favorite import FavoriteRepo
from repositories.user import UserRepo


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any], 
    ) -> Any:
        async with self.session_maker() as session:
            data["user_repo"] = UserRepo(session=session)
            data["category_repo"] = CategoryRepo(session=session)
            data["book_repo"] = BookRepo(session=session)
            data["favorite_repo"] = FavoriteRepo(session=session)
            return await handler(event, data)