from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models.book import Book
from database.models.favorites import Favorite


class FavoriteRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session
        
    async def add_book_to_favorites(self, user_id: int, book_id: int) -> None:
        favorite = Favorite(user_id=user_id, book_id=book_id)
        self.__session.add(favorite)
        await self.__session.commit()


    async def remove_book_from_favorites(self, user_id: int, book_id: int) -> bool:
        stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.book_id == book_id )
        result = await self.__session.execute(stmt)
        favorite = result.scalar_one_or_none()
        if favorite:
            await self.__session.delete(favorite)
            await self.__session.commit()
            return True
        return False
    

    async def get_user_favorites(self, user_id: int) -> list[Favorite]:
        stmt = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(selectinload(Favorite.book))
            .order_by(Favorite.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    

    async def get_all_user_books(self, user_id: int) -> list[Book]:
        favorites = await self.get_user_favorites(user_id)
        return [fav.book for fav in favorites]


    async def is_favorite(self, user_id: int, book_id: int) -> bool:
        # Проверить, есть ли книга в избранном
        stmt = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.book_id == book_id
        )
        favorite = await self.session.scalar(stmt)
        return favorite is not None


    async def count_favorite_books(self, user_id: int) -> int:
        stmt = select(Favorite).where(Favorite.user_id == user_id)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())


    async def clear_favorite_books(self, user_id: int) -> int:
        stmt = delete(Favorite).where(Favorite.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount