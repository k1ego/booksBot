from typing import Optional
from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BigInteger

class User(BaseModel):
		__tablename__ = 'users'

		id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
		tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
		username: Mapped[Optional[str]]
		fullname: Mapped[str]