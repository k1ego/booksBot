import asyncio
from aiogram import Bot, Dispatcher

from handlers import register_routes
from database.models import BaseModel
from middlewares import register_middlewares

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

TOKEN = "8574911316:AAE9f4NBhT2L7ewolOyvFVuQpHMiL7lH_W4"


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    engine = create_async_engine(url="sqlite+aiosqlite:///book_shop.db")
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    register_middlewares(dp, session_maker)
    register_routes(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
