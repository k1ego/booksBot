from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import datetime

class Favorite(BaseModel):
    __tablename__ = 'favorites'
    
    # Первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Внешний ключ на пользователя
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Внешний ключ на книгу
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Дата добавления
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Запрещаем дубликаты (одна и та же книга у одного пользователя)
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='unique_favorite'),
    )
    
    # Связи для ORM
    user = relationship("User", back_populates="Favorites")
    book = relationship("Book", back_populates="Favorites")