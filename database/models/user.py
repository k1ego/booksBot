from typing import Optional
from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger

class User(BaseModel):
		__tablename__ = 'users'

		id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
		tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
		username: Mapped[Optional[str]]
		fullname: Mapped[str]
		balance: Mapped[int] = mapped_column(default=0)

		@property
		def view_balance(self):
				return round(self.balance / 100, 4)
		
		favorites = relationship("Favorite", back_populates="user")