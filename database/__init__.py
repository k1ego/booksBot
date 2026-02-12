# Импортируем BaseModel из отдельного файла
from database.models import BaseModel

# Импортируем все модели, чтобы Alembic их видел
from database.models.user import User
from database.models.category import Category
from database.models.book import Book
from database.models.favorites import Favorite

__all__ = ['BaseModel', 'User', 'Category', 'Book', 'Favorite']